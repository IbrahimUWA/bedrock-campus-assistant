"""Shared helpers: Terraform outputs, boto3 clients, prices, and ask()."""
import json
import os
import subprocess
import sys
from pathlib import Path

import boto3

ROOT = Path(__file__).resolve().parent.parent
INFRA = ROOT / "infra"
RESULTS = ROOT / "results"
sys.path.insert(0, str(ROOT))

from agent import core  # noqa: E402

# CAMPUS_BACKEND=local swaps the model and the retrieval for local stand-ins
# (agent/local_backend.py). The guardrail and the Lambda tools stay on AWS.
LOCAL = os.environ.get("CAMPUS_BACKEND", "").lower() == "local"
LOCAL_MODELS = {"qwen3-8b": "local/Qwen3-8B", "qwen3-14b": "local/Qwen3-14B"}


def outputs() -> dict:
    """Terraform outputs as {name: value}. deploy.ps1 writes infra/outputs.json."""
    path = INFRA / "outputs.json"
    if path.exists():
        raw = json.loads(path.read_text(encoding="utf-8-sig"))
    else:
        raw = json.loads(subprocess.check_output(["terraform", "output", "-json"], cwd=INFRA))
    if not raw:
        raise SystemExit("No Terraform outputs found. Deploy first: see README.")
    out = {k: v["value"] for k, v in raw.items()}
    if LOCAL:
        out["models"] = dict(LOCAL_MODELS)
    return out


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


def agent_config(guardrail: bool = True) -> dict:
    out = outputs()
    return {
        "region": out["region"],
        "knowledge_base_id": out["knowledge_base_id"],
        "guardrail_id": out["guardrail_id"] if guardrail else "",
        "guardrail_version": out["guardrail_version"],
        "tools_function": out["tools_function"],
    }


def ask(model_key: str, question: str, history: list | None = None, guardrail: bool = True) -> dict:
    """Run the agent on the model named `model_key` and add the cost."""
    model_id = outputs()["models"][model_key]
    cfg = agent_config(guardrail)
    if LOCAL:
        from agent import local_backend
        local_backend.install(cfg)
    r = core.run(question, model_id, cfg, history)
    r["model_key"] = model_key
    r["cost_usd"] = cost_usd(model_id, r["input_tokens"], r["output_tokens"])
    return r
