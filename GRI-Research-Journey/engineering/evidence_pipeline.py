"""Research-only evidence intake. No external I/O or publication authority."""
import hashlib
import json
from datetime import datetime, timezone
from urllib.parse import urlsplit

REQUIRED = ("source_id", "source_url", "claim", "captured_at", "jurisdiction")
STATUSES = {"unverified", "corroboration_pending", "human_reviewed"}

def normalize(record):
    if not isinstance(record, dict):
        raise ValueError("record must be an object")
    for key in REQUIRED:
        if not isinstance(record.get(key), str) or not record[key].strip():
            raise ValueError("missing or invalid " + key)
    parts = urlsplit(record["source_url"])
    if parts.scheme != "https" or not parts.hostname or parts.username or parts.password:
        raise ValueError("source_url must be an HTTPS URL without credentials")
    try:
        timestamp = datetime.fromisoformat(record["captured_at"].replace("Z", "+00:00"))
    except ValueError as exc:
        raise ValueError("invalid captured_at") from exc
    if timestamp.tzinfo is None:
        raise ValueError("captured_at must include timezone")
    status = record.get("verification_status", "unverified")
    if status not in STATUSES:
        raise ValueError("unknown verification status")
    canonical = {key: record[key].strip() for key in REQUIRED}
    canonical["captured_at"] = timestamp.astimezone(timezone.utc).isoformat()
    canonical["verification_status"] = status
    canonical["publication_authorized"] = False
    digest = hashlib.sha256(json.dumps(canonical, sort_keys=True, separators=(",", ":")).encode()).hexdigest()
    return {**canonical, "evidence_digest": digest}

def deduplicate(records):
    output, seen = [], set()
    for record in records:
        item = normalize(record)
        if item["evidence_digest"] not in seen:
            seen.add(item["evidence_digest"])
            output.append(item)
    return output
