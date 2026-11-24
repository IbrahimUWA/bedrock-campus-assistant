"""Shared helpers: Terraform outputs, boto3 clients, and one function that
calls an agent and turns its event stream into a plain dictionary."""
import json
import subprocess
import time
import uuid
from pathlib import Path

import boto3

ROOT = Path(__file__).resolve().parent.parent
INFRA = ROOT / "infra"
RESULTS = ROOT / "results"


def outputs() -> dict:
    """Terraform outputs as {name: value}. deploy.ps1 writes infra/outputs.json."""
    path = INFRA / "outputs.json"
    if path.exists():
        raw = json.loads(path.read_text(encoding="utf-8-sig"))
    else:
        raw = json.loads(subprocess.check_output(["terraform", "output", "-json"], cwd=INFRA))
    if not raw:
        raise SystemExit("No Terraform outputs found. Deploy first: see README, step 3.")
    return {k: v["value"] for k, v in raw.items()}


def client(service: str, region: str | None = None):
    return boto3.Session(region_name=region or outputs()["region"]).client(service)


def prices() -> dict:
    return json.loads((ROOT / "data" / "prices.json").read_text(encoding="utf-8"))["usd_per_million_tokens"]


def cost_usd(model: str, input_tokens: int, output_tokens: int) -> float | None:
    """Cost from the price table, matched on a substring of the model id."""
    for key, p in prices().items():
        if key in model:
            return (input_tokens * p["input"] + output_tokens * p["output"]) / 1_000_000
    return None


def ask(model_key: str, question: str, session_id: str | None = None) -> dict:
    """Send one question to the agent built on `model_key` and collect the
    answer, citations, tool calls, searches, guardrail action, tokens and timing."""
    out = outputs()
    agent = out["agents"][model_key]
    runtime = client("bedrock-agent-runtime", out["region"])
    result = {
        "model_key": model_key, "model": agent["model"], "question": question,
        "answer": "", "citations": [], "tool_calls": [], "searches": [],
        "guardrail": "NONE", "guardrail_detail": [],
        "input_tokens": 0, "output_tokens": 0, "model_calls": 0,
        "first_chunk_s": None, "error": None,
    }
    start = time.perf_counter()
    try:
        response = runtime.invoke_agent(
            agentId=agent["agent_id"], agentAliasId=agent["alias_id"],
            sessionId=session_id or uuid.uuid4().hex, inputText=question, enableTrace=True,
        )
        for event in response["completion"]:
            if "chunk" in event:
                chunk = event["chunk"]
                if result["first_chunk_s"] is None:
                    result["first_chunk_s"] = round(time.perf_counter() - start, 2)
                result["answer"] += chunk.get("bytes", b"").decode("utf-8")
                for cit in chunk.get("attribution", {}).get("citations", []):
                    for ref in cit.get("retrievedReferences", []):
                        _add_citation(result, ref)
            elif "trace" in event:
                _read_trace(result, event["trace"].get("trace", {}))
    except Exception as exc:  # throttling, access denied, validation
        result["error"] = f"{type(exc).__name__}: {exc}"
    result["latency_s"] = round(time.perf_counter() - start, 2)
    result["cost_usd"] = cost_usd(result["model"], result["input_tokens"], result["output_tokens"])
    return result


def _add_citation(result: dict, ref: dict) -> None:
    meta = ref.get("metadata", {})
    url = meta.get("source_url") or ref.get("location", {}).get("s3Location", {}).get("uri", "")
    if url and url not in [c["url"] for c in result["citations"]]:
        result["citations"].append({"url": url, "title": meta.get("title", ""),
                                    "snippet": ref.get("content", {}).get("text", "")[:240]})


def _read_trace(result: dict, trace: dict) -> None:
    if "guardrailTrace" in trace:
        g = trace["guardrailTrace"]
        if g.get("action") == "INTERVENED":
            result["guardrail"] = "INTERVENED"
            result["guardrail_detail"].extend(g.get("inputAssessments", []) + g.get("outputAssessments", []))
    for stage in ("preProcessingTrace", "orchestrationTrace", "postProcessingTrace"):
        t = trace.get(stage)
        if not t:
            continue
        usage = t.get("modelInvocationOutput", {}).get("metadata", {}).get("usage")
        if usage:
            result["input_tokens"] += usage.get("inputTokens", 0)
            result["output_tokens"] += usage.get("outputTokens", 0)
            result["model_calls"] += 1
        inv = t.get("invocationInput", {})
        if "actionGroupInvocationInput" in inv:
            a = inv["actionGroupInvocationInput"]
            result["tool_calls"].append({
                "function": a.get("function", ""),
                "parameters": {p["name"]: p.get("value") for p in a.get("parameters", [])},
            })
        if "knowledgeBaseLookupInput" in inv:
            result["searches"].append(inv["knowledgeBaseLookupInput"].get("text", ""))
        for ref in t.get("observation", {}).get("knowledgeBaseLookupOutput", {}).get("retrievedReferences", []):
            _add_citation(result, ref)
    if "failureTrace" in trace:
        result["error"] = trace["failureTrace"].get("failureReason", "agent failure")
