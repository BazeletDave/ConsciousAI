"""Offline GRI evidence validation; no network or storage access."""
import hashlib
import json
from datetime import datetime, timezone
from urllib.parse import urlsplit

DOMAINS = ("defend", "harden", "prevail", "human_authority", "evidence_integrity", "institutional_legitimacy")
TYPES = ("controlled_experiment", "documented_observation")
FIELDS = ("record_id", "case_id", "domain", "observation_type", "observed_at", "source_url", "source_sha256", "outcome", "reviewer_id", "reviewed_at", "independent_review", "consent_or_authority")

def timestamp(value):
    if not isinstance(value, str):
        raise ValueError("timestamp must be text")
    try:
        result = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError as exc:
        raise ValueError("invalid timestamp") from exc
    if result.tzinfo is None:
        raise ValueError("timezone required")
    return result.astimezone(timezone.utc)

def validate(record):
    if not isinstance(record, dict) or any(key not in record for key in FIELDS):
        raise ValueError("missing evidence fields")
    for key in ("record_id", "case_id", "reviewer_id", "consent_or_authority"):
        if not isinstance(record[key], str) or not record[key].strip() or len(record[key]) > 200:
            raise ValueError("invalid " + key)
    if record["domain"] not in DOMAINS or record["observation_type"] not in TYPES:
        raise ValueError("invalid domain or observation type")
    observed, reviewed = timestamp(record["observed_at"]), timestamp(record["reviewed_at"])
    if reviewed < observed:
        raise ValueError("review precedes observation")
    url = record["source_url"]
    if not isinstance(url, str) or len(url) > 2048:
        raise ValueError("invalid source URL")
    parts = urlsplit(url)
    if parts.scheme != "https" or not parts.hostname or parts.username or parts.password or parts.fragment:
        raise ValueError("source must be HTTPS without credentials or fragment")
    digest = record["source_sha256"]
    if not isinstance(digest, str) or len(digest) != 64 or any(c not in "0123456789abcdef" for c in digest):
        raise ValueError("invalid source digest")
    if type(record["outcome"]) is not bool or record["independent_review"] is not True:
        raise ValueError("boolean outcome and independent review required")
    if record.get("source_verified") is not True:
        raise ValueError("source verification required")
    if record.get("scenario_type") == "synthetic":
        raise ValueError("synthetic evidence is excluded")
    normalized = {key: record[key] for key in FIELDS}
    normalized.update(observed_at=observed.isoformat(), reviewed_at=reviewed.isoformat(), source_verified=True)
    payload = json.dumps(normalized, sort_keys=True, separators=(",", ":"))
    return {"record": normalized, "evidence_sha256": hashlib.sha256(payload.encode()).hexdigest()}

def summarize(records):
    if not isinstance(records, list) or len(records) > 1000:
        raise ValueError("invalid collection")
    buckets = {domain: [] for domain in DOMAINS}
    seen, rejected = set(), []
    for index, record in enumerate(records):
        try:
            item = validate(record)
            rid = item["record"]["record_id"]
            if rid in seen:
                raise ValueError("duplicate record ID")
            seen.add(rid)
            buckets[item["record"]["domain"]].append(item)
        except (ValueError, TypeError, AttributeError) as exc:
            rejected.append({"index": index, "reason": str(exc)})
    domains = []
    for domain, items in buckets.items():
        n = len(items)
        passed = sum(item["record"]["outcome"] for item in items)
        domains.append({"id": domain, "status": "observed_not_generalizable" if n else "unmeasured",
                        "validated_records": n, "passed": passed, "failed": n-passed,
                        "observed_pass_fraction": round(passed/n, 4) if n else None,
                        "evidence_sha256": [item["evidence_sha256"] for item in items]})
    return {"schema_version": "1.0", "mode": "research_evidence_summary",
            "domains": domains, "rejected_count": len(rejected), "rejections": rejected,
            "notice": "Review and source verification are declared, not independently proven by this program. Fractions are descriptive, not effectiveness estimates or CISA certification."}
