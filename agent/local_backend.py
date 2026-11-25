"""Local stand-in for the two Bedrock calls that need model quota.

A new AWS account can deploy everything in this project and still be unable
to call a model: its Bedrock quotas start at 0 until AWS lifts them. This
module lets the same agent loop (agent/core.py, unchanged) run meanwhile:

  bedrock-runtime.converse        -> a local open model (Qwen3-8B or Qwen3-14B, transformers)
  bedrock-agent-runtime.retrieve  -> local embeddings over the same fetched pages

Still real and on AWS:
  * the guardrail: the deployed Bedrock Guardrail is applied to the user's
    words and to the model's answer with the ApplyGuardrail API, which exists
    for exactly this case (guarding a model that is not hosted on Bedrock)
  * the tools: the deployed Lambda function

Numbers from this backend describe a local model on one workstation. They are
not Bedrock latency, token or cost figures.

    from agent import local_backend
    local_backend.install(cfg)      # then call core.run(question, MODEL_ID, cfg)
"""
import json
import os
import re
import time
from pathlib import Path

import boto3

from . import core

MODELS = {"local/Qwen3-8B": "Qwen/Qwen3-8B", "local/Qwen3-14B": "Qwen/Qwen3-14B"}   # model id -> Hugging Face repo
MODEL_ID = "local/Qwen3-8B"
HF_EMBEDDER = "BAAI/bge-base-en-v1.5"
_DEMO = os.environ.get("CAMPUS_DATASET", "").lower() == "demo"      # fictional university pages, data/demo_site
PAGES = Path(__file__).resolve().parent.parent / "data" / ("demo_site" if _DEMO else "pages")
CHUNK_CHARS, OVERLAP_CHARS = 1200, 240      # about 300 tokens with 20% overlap, as in the Knowledge Base


def _chunks(page: str) -> list[str]:
    """Split at section headings first, so a table stays with its heading, then by size."""
    title = page.split("\n", 1)[0].lstrip("# ").strip()
    out = []
    for section in re.split(r"\n(?=#{1,4} )", page):
        heading = section.split("\n", 1)[0].lstrip("# ").strip()
        prefix = "" if heading == title else f"[{title}]\n"
        pieces = _by_size(section)
        out += [prefix + (p if i == 0 else f"## {heading} (continued)\n{p}") for i, p in enumerate(pieces)]
    return out


def _by_size(text: str) -> list[str]:
    out, start = [], 0
    while start < len(text):
        end = min(len(text), start + CHUNK_CHARS)
        if end < len(text):
            cut = text.rfind("\n", start + CHUNK_CHARS // 2, end)
            end = cut if cut > 0 else end
        out.append(text[start:end].strip())
        if end >= len(text):
            break
        start = end - OVERLAP_CHARS
    return [c for c in out if c]


class LocalKnowledgeBase:
    """Same request and response shape as the Knowledge Base Retrieve API."""

    def __init__(self):
        from sentence_transformers import SentenceTransformer
        self.model = SentenceTransformer(HF_EMBEDDER)
        self.rows = []
        for page in sorted(p for p in PAGES.glob("*.md") if p.name != "README.md"):
            meta = json.loads((PAGES / (page.name + ".metadata.json")).read_text(encoding="utf-8"))["metadataAttributes"]
            self.rows += [{"text": c, "meta": meta} for c in _chunks(page.read_text(encoding="utf-8"))]
        if not self.rows:
            raise RuntimeError("no pages found: run scripts/01_fetch_pages.py first")
        self.vectors = self.model.encode([r["text"] for r in self.rows], normalize_embeddings=True)

    def retrieve(self, knowledgeBaseId, retrievalQuery, retrievalConfiguration=None, **_):
        n = (retrievalConfiguration or {}).get("vectorSearchConfiguration", {}).get("numberOfResults", 4)
        q = self.model.encode(["Represent this sentence for searching relevant passages: " + retrievalQuery["text"]],
                              normalize_embeddings=True)[0]
        scores = self.vectors @ q
        best = sorted(range(len(self.rows)), key=lambda i: -scores[i])[:n]
        return {"retrievalResults": [{"content": {"text": self.rows[i]["text"]}, "score": float(scores[i]),
                                      "metadata": self.rows[i]["meta"]} for i in best]}


class LocalRuntime:
    """Same request and response shape as the Converse API, for the fields core.run uses."""

    def __init__(self, region: str):
        import torch
        from transformers import AutoModelForCausalLM, AutoTokenizer
        self.torch, self._tok_cls, self._model_cls, self.loaded = torch, AutoTokenizer, AutoModelForCausalLM, {}
        self.guard = boto3.client("bedrock-runtime", region_name=region)

    def _guard(self, cfg: dict, source: str, text: str):
        """Apply the deployed Bedrock Guardrail. Returns (replacement text or None, assessments)."""
        r = self.guard.apply_guardrail(guardrailIdentifier=cfg["guardrailIdentifier"], guardrailVersion=cfg["guardrailVersion"],
                                       source=source, content=[{"text": {"text": text}}])
        if r["action"] != "GUARDRAIL_INTERVENED":
            return None, r.get("assessments", [])
        return (r["outputs"][0]["text"] if r.get("outputs") else ""), r.get("assessments", [])

    def _load(self, model_id: str):
        if model_id not in self.loaded:
            repo = MODELS[model_id]
            self.loaded[model_id] = (self._tok_cls.from_pretrained(repo),
                                     self._model_cls.from_pretrained(repo, dtype=self.torch.bfloat16, device_map="cuda"))
        return self.loaded[model_id]

    @staticmethod
    def _chat(system, messages) -> list:
        chat = [{"role": "system", "content": " ".join(s["text"] for s in system)}]
        for m in messages:
            text = "".join(b.get("text", "") or b.get("guardContent", {}).get("text", {}).get("text", "") for b in m["content"])
            calls = [{"type": "function", "function": {"name": b["toolUse"]["name"], "arguments": b["toolUse"]["input"]}}
                     for b in m["content"] if "toolUse" in b]
            results = [b["toolResult"] for b in m["content"] if "toolResult" in b]
            if results:
                chat += [{"role": "tool", "content": json.dumps(r["content"][0]["json"], ensure_ascii=False)} for r in results]
            elif calls:
                chat.append({"role": "assistant", "content": text, "tool_calls": calls})
            else:
                chat.append({"role": m["role"], "content": text})
        return chat

    def converse(self, modelId, messages, system=(), toolConfig=None, inferenceConfig=None, guardrailConfig=None, **_):
        self.tok, self.model = self._load(modelId)      # loaded once, before the clock starts
        start = time.perf_counter()
        trace = {}
        last = messages[-1]["content"]
        guarded = [b["guardContent"]["text"]["text"] for b in last if "guardContent" in b]
        if guardrailConfig and guarded:
            replacement, assessments = self._guard(guardrailConfig, "INPUT", "\n".join(guarded))
            if assessments:
                trace["inputAssessment"] = {guardrailConfig["guardrailIdentifier"]: assessments[0]}
            if replacement is not None:      # blocked before the model is called
                return {"output": {"message": {"role": "assistant", "content": [{"text": replacement}]}},
                        "stopReason": "guardrail_intervened", "usage": {"inputTokens": 0, "outputTokens": 0},
                        "metrics": {"latencyMs": int((time.perf_counter() - start) * 1000)}, "trace": {"guardrail": trace}}

        tools = [{"type": "function", "function": {"name": t["toolSpec"]["name"], "description": t["toolSpec"]["description"],
                                                   "parameters": t["toolSpec"]["inputSchema"]["json"]}}
                 for t in (toolConfig or {}).get("tools", [])]
        prompt = self.tok.apply_chat_template(self._chat(system, messages), tools=tools or None, tokenize=False,
                                              add_generation_prompt=True, enable_thinking=False)
        ids = self.tok(prompt, return_tensors="pt").to(self.model.device)
        with self.torch.no_grad():
            out = self.model.generate(**ids, max_new_tokens=(inferenceConfig or {}).get("maxTokens", 700), do_sample=False)
        new = out[0][ids["input_ids"].shape[1]:]
        raw = self.tok.decode(new, skip_special_tokens=True)
        raw = re.sub(r"<think>.*?</think>", "", raw, flags=re.S).strip()

        content, stop = [], "end_turn"
        calls = re.findall(r"<tool_call>\s*(\{.*?\})\s*</tool_call>", raw, flags=re.S)
        text = re.sub(r"<tool_call>.*?</tool_call>", "", raw, flags=re.S).strip()
        if text:
            content.append({"text": text})
        for i, c in enumerate(calls):
            try:
                call = json.loads(c)
            except json.JSONDecodeError:
                continue
            content.append({"toolUse": {"toolUseId": f"local-{len(messages)}-{i}", "name": call.get("name", ""),
                                        "input": call.get("arguments", {}) or {}}})
            stop = "tool_use"

        if guardrailConfig and stop == "end_turn" and text:
            replacement, assessments = self._guard(guardrailConfig, "OUTPUT", text)
            if assessments:
                trace["outputAssessments"] = {guardrailConfig["guardrailIdentifier"]: assessments}
            if replacement is not None:      # masked or blocked on the way out
                content, stop = [{"text": replacement}], "guardrail_intervened"
        if not content:
            content = [{"text": ""}]
        return {"output": {"message": {"role": "assistant", "content": content}}, "stopReason": stop,
                "usage": {"inputTokens": int(ids["input_ids"].shape[1]), "outputTokens": int(len(new))},
                "metrics": {"latencyMs": int((time.perf_counter() - start) * 1000)},
                "trace": {"guardrail": trace} if trace else {}}


def install(cfg: dict) -> str:
    """Route core.run's model and retrieval calls to the local stand-ins. Returns the model id to pass."""
    region = cfg["region"]
    if ("bedrock-runtime", region) not in core._clients or not isinstance(core._clients[("bedrock-runtime", region)], LocalRuntime):
        core._clients[("bedrock-runtime", region)] = LocalRuntime(region)
        core._clients[("bedrock-agent-runtime", region)] = LocalKnowledgeBase()
    return MODEL_ID
