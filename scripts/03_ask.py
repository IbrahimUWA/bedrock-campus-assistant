"""Step 3: ask the agent a question from the command line.

    python scripts/03_ask.py "When are exam results released?"
    python scripts/03_ask.py --model haiku "What are the assessments for DEMO2002?"
    python scripts/03_ask.py            (interactive; the session keeps context)
"""
import argparse
import sys
import uuid

from common import ask, outputs


def show(r: dict) -> None:
    for q in r["searches"]:
        print(f"  [search]    {q}")
    for t in r["tool_calls"]:
        print(f"  [tool]      {t['function']}({t['parameters']})")
    if r["guardrail"] == "INTERVENED":
        print("  [guardrail] intervened")
    if r["error"]:
        print(f"  [error]     {r['error']}")
    print(f"\n{r['answer'].strip()}\n")
    for i, c in enumerate(r["citations"], 1):
        print(f"  [{i}] {c['url']}")
    cost = f"${r['cost_usd']:.5f}" if r["cost_usd"] is not None else "n/a"
    print(f"  {r['model']} | {r['latency_s']} s | {r['input_tokens']} in + {r['output_tokens']} out tokens "
          f"over {r['model_calls']} model calls | {cost}\n")


def main() -> None:
    sys.stdout.reconfigure(encoding="utf-8")
    keys = list(outputs()["agents"])
    ap = argparse.ArgumentParser()
    ap.add_argument("question", nargs="?")
    ap.add_argument("--model", choices=keys, default=keys[0])
    args = ap.parse_args()
    if args.question:
        show(ask(args.model, args.question))
        return
    session = uuid.uuid4().hex
    print(f"Campus assistant on '{args.model}'. Empty line to quit.")
    while True:
        q = input("> ").strip()
        if not q:
            break
        show(ask(args.model, q, session))


if __name__ == "__main__":
    main()
