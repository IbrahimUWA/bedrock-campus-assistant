"""Step 0: check the AWS account can run the demo before deploying anything.

Confirms who you are signed in as, that the embedding model exists in the
region, and that each agent model answers a one-line request. Costs a
fraction of a cent.

    python scripts/00_preflight.py [--region ap-southeast-2]
"""
import argparse
import re
import sys
from pathlib import Path

import boto3

ROOT = Path(__file__).resolve().parent.parent


def tf_default(name: str) -> str:
    """Read a variable block's default from infra/variables.tf."""
    text = (ROOT / "infra" / "variables.tf").read_text(encoding="utf-8")
    block = re.search(r'variable "%s" \{(.*?)\n\}' % name, text, re.S).group(1)
    return block


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--region", default=re.search(r'default\s*=\s*"([^"]+)"', tf_default("region")).group(1))
    args = ap.parse_args()
    session = boto3.Session(region_name=args.region)
    ok = True

    try:
        ident = session.client("sts").get_caller_identity()
    except Exception as exc:
        print(f"FAIL  not signed in to AWS: {exc}\n      Run: aws configure")
        return 1
    print(f"ok    signed in as {ident['Arn'].split('/')[-1]} in account ...{ident['Account'][-4:]}, region {args.region}")

    bedrock = session.client("bedrock")
    embed = re.search(r'default\s*=\s*"([^"]+)"', tf_default("embedding_model_id")).group(1)
    models = {m["modelId"] for m in bedrock.list_foundation_models()["modelSummaries"]}
    if embed in models:
        print(f"ok    embedding model {embed} is offered here")
    else:
        ok = False
        print(f"FAIL  embedding model {embed} is not offered in {args.region}")

    profiles = {}
    for page in bedrock.get_paginator("list_inference_profiles").paginate():
        for p in page["inferenceProfileSummaries"]:
            profiles[p["inferenceProfileId"]] = p["inferenceProfileName"]

    runtime = session.client("bedrock-runtime")
    wanted = dict(re.findall(r'(\w+)\s*=\s*"([^"]+)"', re.search(r"default = \{(.*?)\}", tf_default("agent_models"), re.S).group(1)))
    for key, model_id in wanted.items():
        try:
            r = runtime.converse(modelId=model_id, messages=[{"role": "user", "content": [{"text": "Reply with the word ok."}]}],
                                 inferenceConfig={"maxTokens": 5})
            print(f"ok    {key}: {model_id} answered ({r['usage']['inputTokens']} in / {r['usage']['outputTokens']} out tokens)")
        except Exception as exc:
            ok = False
            print(f"FAIL  {key}: {model_id} -> {type(exc).__name__}: {str(exc)[:200]}")
            family = model_id.split(".", 1)[-1].rsplit("-v", 1)[0]
            close = [p for p in profiles if family.split("-2025")[0] in p]
            if close:
                print(f"      profiles here that look similar: {', '.join(sorted(close))}")
                print("      put one of these in infra/variables.tf (agent_models) or a terraform.tfvars file")
            elif "AccessDenied" in type(exc).__name__ or "access" in str(exc).lower():
                print("      open the Bedrock console > Model catalog, pick the model and request access")

    try:
        session.client("s3vectors").list_vector_buckets(maxResults=1)
        print("ok    S3 Vectors is available here")
    except Exception as exc:
        ok = False
        print(f"FAIL  S3 Vectors: {type(exc).__name__}: {str(exc)[:160]}")

    print("\nReady to deploy." if ok else "\nFix the FAIL lines above before deploying.")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
