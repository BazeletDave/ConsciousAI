"""Offline, non-enforcing governance intelligence registry validator."""
import json
from pathlib import Path
from urllib.parse import urlparse

ALLOWED_VERIFICATION = {"PRIMARY_DOCUMENT", "SECONDARY_SOURCE", "PARTICIPANT_REPORT", "DIRECT_OBSERVATION", "SYNTHETIC_TEST", "HYPOTHESIS", "UNVERIFIED"}
ALLOWED_REVIEW = {"RESEARCH_LEAD", "SOURCE_REVIEWED", "INDEPENDENTLY_CORROBORATED"}
REQUIRED = {"id", "title", "domain", "source_url", "source_type", "verification", "governance_risk", "safeguard", "opportunity", "review_status", "last_reviewed"}

def validate(record):
    if not isinstance(record, dict) or not REQUIRED.issubset(record):
        raise ValueError("Missing required signal fields")
    if any(not isinstance(record[k], str) or not record[k].strip() for k in REQUIRED):
        raise ValueError("Signal fields must be nonempty strings")
    if record["verification"] not in ALLOWED_VERIFICATION or record["review_status"] not in ALLOWED_REVIEW:
        raise ValueError("Invalid evidence or review state")
    u = urlparse(record["source_url"])
    if u.scheme != "https" or not u.netloc:
        raise ValueError("Source must be an HTTPS URL")
    if record["verification"] in {"HYPOTHESIS", "UNVERIFIED", "SYNTHETIC_TEST"} and record["review_status"] == "INDEPENDENTLY_CORROBORATED":
        raise ValueError("Unverified or synthetic evidence cannot be independently corroborated as a real-world event")
    return record

def load(path):
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    if not isinstance(data, list):
        raise ValueError("Expected list of signals")
    seen = set()
    for record in data:
        validate(record)
        if record["id"] in seen:
            raise ValueError("Duplicate signal ID")
        seen.add(record["id"])
    return data

if __name__ == "__main__":
    signals = load(Path(__file__).with_name("signals.json"))
    print(json.dumps({"records": len(signals), "reviewed": sum(s["review_status"] != "RESEARCH_LEAD" for s in signals), "live_monitoring": False, "external_actions": False}, indent=2))
