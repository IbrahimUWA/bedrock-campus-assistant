"""Step 5: run the same questions through each model's agent and compare
latency, tokens, cost and answer quality.

Per question it records wall-clock latency, tokens summed over every
model call the agent made (from the trace), cost from data/prices.json,
and a simple quality check (expected facts present, right tool used).
It also publishes the numbers as CloudWatch custom metrics so they
appear on the dashboard next to the built-in Bedrock metrics.

Writes results/comparison.json and results/comparison.md.
"""
import argparse
import json
import statistics
import sys
import time

from common import RESULTS, ROOT, ask, client, outputs


def passed(q: dict, r: dict) -> bool:
    if r["error"]:
        return False
    answer = r["answer"].lower()
    for item in q["expect"]:
        options = item if isinstance(item, list) else [item]
        if not any(o.lower() in answer for o in options):
            return False
    if q.get("tool") and q["tool"] not in [t["function"] for t in r["tool_calls"]]:
        return False
    return True


def main() -> int:
    sys.stdout.reconfigure(encoding="utf-8")
    ap = argparse.ArgumentParser()
    ap.add_argument("--repeats", type=int, default=1, help="runs per question (latency varies run to run)")
    ap.add_argument("--no-metrics", action="store_true", help="do not publish CloudWatch metrics")
    args = ap.parse_args()

    out = outputs()
    questions = json.loads((ROOT / "data" / "eval_questions.json").read_text(encoding="utf-8"))["questions"]
    cw = client("cloudwatch")
    runs = []
    for key in out["models"]:
        for q in questions:
            for _ in range(args.repeats):
                r = ask(key, q["question"])
                r.update(id=q["id"], kind=q["kind"], passed=passed(q, r))
                runs.append(r)
                print(f"{key:<6} {q['id']} {'pass' if r['passed'] else 'FAIL'}  {r['latency_s']:>5} s  "
                      f"{r['input_tokens']:>5} in {r['output_tokens']:>4} out  {r['answer'].strip()[:60]!r}")
                if not args.no_metrics and not r["error"]:
                    dims = [{"Name": "Model", "Value": key}]
                    data = [{"MetricName": "LatencySeconds", "Dimensions": dims, "Value": r["latency_s"], "Unit": "Seconds"},
                            {"MetricName": "InputTokens", "Dimensions": dims, "Value": r["input_tokens"], "Unit": "Count"},
                            {"MetricName": "OutputTokens", "Dimensions": dims, "Value": r["output_tokens"], "Unit": "Count"},
                            {"MetricName": "Passed", "Dimensions": dims, "Value": int(r["passed"]), "Unit": "Count"}]
                    if r["cost_usd"] is not None:
                        data.append({"MetricName": "CostUSD", "Dimensions": dims, "Value": r["cost_usd"], "Unit": "None"})
                    cw.put_metric_data(Namespace="CampusAssistant", MetricData=data)
                time.sleep(1)  # stay under on-demand rate limits

    summary = {}
    for key, model_id in out["models"].items():
        mine = [r for r in runs if r["model_key"] == key]
        good = [r for r in mine if not r["error"]]
        lat = sorted(r["latency_s"] for r in good)
        costs = [r["cost_usd"] for r in good if r["cost_usd"] is not None]
        summary[key] = {
            "model": model_id, "runs": len(mine), "errors": len(mine) - len(good),
            "passed": sum(r["passed"] for r in mine),
            "by_kind": {k: f"{sum(r['passed'] for r in mine if r['kind'] == k)}/{sum(1 for r in mine if r['kind'] == k)}"
                        for k in ("kb", "tool", "abstain")},
            "latency_median_s": round(statistics.median(lat), 2) if lat else None,
            "latency_max_s": lat[-1] if lat else None,
            "input_tokens_mean": round(statistics.mean(r["input_tokens"] for r in good)) if good else None,
            "output_tokens_mean": round(statistics.mean(r["output_tokens"] for r in good)) if good else None,
            "cost_per_question_usd": round(statistics.mean(costs), 6) if costs else None,
            "cost_per_1000_questions_usd": round(statistics.mean(costs) * 1000, 2) if costs else None,
        }

    RESULTS.mkdir(exist_ok=True)
    (RESULTS / "comparison.json").write_text(json.dumps({"summary": summary, "runs": [{k: v for k, v in r.items() if k != "messages"} for r in runs]}, indent=2, default=str), encoding="utf-8")
    md = ["# Model comparison", "",
          f"{len(questions)} questions, {args.repeats} run(s) each, through the full agent loop (guardrail, knowledge base, tools).",
          "Costs use the hand-entered table in `data/prices.json`; check it against the AWS pricing page.", "",
          "| | " + " | ".join(summary) + " |", "| --- |" + " --- |" * len(summary)]
    rows = [("Model", "model"), ("Questions passed", None), ("Knowledge base questions", "kb"), ("Tool questions", "tool"),
            ("Unanswerable question handled", "abstain"), ("Errors", "errors"),
            ("Median latency (s)", "latency_median_s"), ("Slowest (s)", "latency_max_s"),
            ("Mean input tokens", "input_tokens_mean"), ("Mean output tokens", "output_tokens_mean"),
            ("Cost per question (USD)", "cost_per_question_usd"), ("Cost per 1,000 questions (USD)", "cost_per_1000_questions_usd")]
    for label, field in rows:
        cells = []
        for s in summary.values():
            if field is None:
                cells.append(f"{s['passed']}/{s['runs']}")
            elif field in ("kb", "tool", "abstain"):
                cells.append(s["by_kind"][field])
            else:
                cells.append(str(s[field]))
        md.append(f"| {label} | " + " | ".join(cells) + " |")
    md += ["", "## Per question", "", "| Model | Id | Kind | Pass | Latency (s) | In | Out | Answer |", "| --- | --- | --- | --- | --- | --- | --- | --- |"]
    md += [f"| {r['model_key']} | {r['id']} | {r['kind']} | {'yes' if r['passed'] else 'no'} | {r['latency_s']} | {r['input_tokens']} | "
           f"{r['output_tokens']} | {(r['answer'].strip() or r['error'] or '').replace(chr(10), ' ').replace('|', '/')[:140]} |" for r in runs]
    (RESULTS / "comparison.md").write_text("\n".join(md) + "\n", encoding="utf-8")
    print("\n" + json.dumps(summary, indent=2))
    print(f"\nwrote {RESULTS / 'comparison.md'}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
