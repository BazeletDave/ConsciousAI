"""GRI research knowledge intake: standard-library, offline, fail-closed, no chat access."""
from __future__ import annotations
import hashlib
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent
REGISTRY = ROOT / "research_knowledge" / "approved_records.json"
ID_PATTERN = re.compile(r"^GRI-[A-Z0-9][A-Z0-9-]{2,63}$")
CLAIM_TYPES = {"hypothesis", "observation", "source_report", "inference"}
DOMAINS = {"ai_governance", "algorithmic_management", "institutional_accountability",
           "mobility", "leadership", "financial_value_creation", "cybersecurity"}
REQUIRED = {"id", "title", "date", "domain", "claim_type", "summary", "source_type",
            "provenance", "limitations", "review_status", "publication_authorized"}

def validate(record):
    if not isinstance(record, dict):
        raise ValueError("record must be an object")
    missing = REQUIRED - record.keys()
    if missing:
        raise ValueError("missing required fields: " + ", ".join(sorted(missing)))
    if not isinstance(record["id"], str) or not ID_PATTERN.fullmatch(record["id"]):
        raise ValueError("invalid research ID")
    if record["domain"] not in DOMAINS or record["claim_type"] not in CLAIM_TYPES:
        raise ValueError("invalid domain or claim type")
    if not isinstance(record["date"], str) or not re.fullmatch(r"\d{4}-\d{2}-\d{2}", record["date"]):
        raise ValueError("invalid date")
    for key in ("title", "summary", "source_type", "provenance", "limitations"):
        if not isinstance(record[key], str) or not record[key].strip():
            raise ValueError("required nonempty text: " + key)
    if record["review_status"] not in {"draft", "approved", "rejected"}:
        raise ValueError("invalid review status")
    if not isinstance(record["publication_authorized"], bool):
        raise ValueError("publication authorization must be boolean")
    if record["publication_authorized"] and record["review_status"] != "approved":
        raise ValueError("publication requires approved review")
    if record["review_status"] == "approved" and not record.get("reviewer"):
        raise ValueError("approved record requires reviewer")
    return record

def build_knowledge_snapshot(records):
    if not isinstance(records, list):
        raise ValueError("records must be a list")
    seen = set()
    public = []
    for record in records:
        validate(record)
        if record["id"] in seen:
            raise ValueError("duplicate research ID")
        seen.add(record["id"])
        if record["review_status"] == "approved" and record["publication_authorized"]:
            public.append({key: record[key] for key in
                           ("id", "title", "date", "domain", "claim_type", "summary", "limitations")})
    public.sort(key=lambda item: item["id"])
    canonical = json.dumps(public, sort_keys=True, separators=(",", ":"), ensure_ascii=False)
    return {"schema_version": "1.0", "mode": "reviewed_research_knowledge",
            "record_count": len(public), "records": public,
            "sha256": hashlib.sha256(canonical.encode("utf-8")).hexdigest(),
            "notice": "Reviewed research contributions are not independently validated facts or evidence of model retraining."}

def load_snapshot(path=REGISTRY):
    payload = json.loads(Path(path).read_text(encoding="utf-8"))
    if not isinstance(payload, dict) or not isinstance(payload.get("records"), list):
        raise ValueError("invalid research registry")
    return build_knowledge_snapshot(payload["records"])

if __name__ == "__main__":
    print(json.dumps(load_snapshot(), indent=2))
