"""Tools for the campus assistant agent (Bedrock action group, function schema).

Bedrock sends: {"actionGroup", "function", "parameters": [{"name", "type", "value"}], ...}
and expects the reply wrapped in the same actionGroup and function names.
The unit data is fictional sample data bundled with the function.
"""
import json
import os
import re
import uuid

with open(os.path.join(os.path.dirname(__file__), "units.json"), encoding="utf-8") as f:
    UNITS = {k: v for k, v in json.load(f).items() if not k.startswith("_")}

CATEGORIES = {"enrolment", "fees", "it", "accessibility", "other"}


def get_unit_outline(unit_code: str = "") -> dict:
    code = unit_code.strip().upper().replace(" ", "")
    if not re.fullmatch(r"[A-Z]{4}\d{4}", code):
        return {"error": "Unit codes are four letters and four digits, for example DEMO1001."}
    unit = UNITS.get(code)
    if unit is None:
        return {"error": f"No unit found with code {code}.", "known_codes": sorted(UNITS)}
    return {"unit_code": code, **unit}


def create_support_request(category: str = "", summary: str = "") -> dict:
    category = category.strip().lower()
    if category not in CATEGORIES:
        return {"error": f"Category must be one of: {', '.join(sorted(CATEGORIES))}."}
    if len(summary.strip()) < 10:
        return {"error": "Please give a one-sentence summary of the request."}
    # A real system would call a ticketing API here. The demo only returns
    # a reference, and logs the category but never the summary text.
    reference = f"REQ-{uuid.uuid4().hex[:8].upper()}"
    print(json.dumps({"event": "support_request", "reference": reference, "category": category}))
    return {
        "reference": reference,
        "category": category,
        "status": "received",
        "next_step": "A team member replies within two business days.",
    }


FUNCTIONS = {
    "get_unit_outline": get_unit_outline,
    "create_support_request": create_support_request,
}


def lambda_handler(event, context):
    name = event.get("function", "")
    params = {p["name"]: p.get("value", "") for p in event.get("parameters", [])}
    fn = FUNCTIONS.get(name)
    try:
        result = fn(**params) if fn else {"error": f"Unknown function {name}."}
    except TypeError as exc:
        result = {"error": f"Bad parameters: {exc}"}
    return {
        "messageVersion": event.get("messageVersion", "1.0"),
        "response": {
            "actionGroup": event.get("actionGroup", ""),
            "function": name,
            "functionResponse": {"responseBody": {"TEXT": {"body": json.dumps(result)}}},
        },
    }
