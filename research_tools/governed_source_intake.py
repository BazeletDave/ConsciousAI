"""GRI governed public-source intake. Standard library only; no scraping or external calls.

Input: JSON Lines of manually supplied or appropriately licensed source metadata.
Output: JSON Lines of classified evidence candidates, not model-training data.
No automatic publication, ingestion into production, or promotion to verified status.
"""
import argparse
import hashlib
import json
import re
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlparse

SOURCE_DOMAINS = {
    "reddit": ("reddit.com",),
    "youtube": ("youtube.com", "youtu.be"),
    "government": (".gov", ".gouv.fr"),
    "academic": (".edu", ".ac.uk"),
}
ALLOWED_RIGHTS = {"public_metadata", "licensed", "participant_consented", "permission_pending"}
ALLOWED_SOURCE_TYPES = {"reddit", "youtube", "government", "academic", "journalism", "participant", "other"}
REQUIRED = {"source_type", "url", "title", "observed_at", "rights_basis", "summary"}
MAX_SUMMARY = 2000

def domain_matches(host, suffix):
    return host == suffix.lstrip(".") or host.endswith(suffix) if suffix.startswith(".") else (host == suffix or host.endswith("." + suffix))

def validate(record):
    errors = []
    if not isinstance(record, dict):
        return ["record must be an object"]
    for field in REQUIRED:
        if not isinstance(record.get(field), str) or not record[field].strip():
            errors.append("missing " + field)
    source_type = record.get("source_type")
    if source_type not in ALLOWED_SOURCE_TYPES:
        errors.append("invalid source_type")
    if record.get("rights_basis") not in ALLOWED_RIGHTS:
        errors.append("invalid rights_basis")
    url = record.get("url", "")
    parsed = urlparse(url) if isinstance(url, str) else urlparse("")
    if parsed.scheme != "https" or not parsed.hostname or parsed.username or parsed.password:
        errors.append("source URL must be an HTTPS public URL without credentials")
    elif source_type in SOURCE_DOMAINS and not any(domain_matches(parsed.hostname.lower(), d) for d in SOURCE_DOMAINS[source_type]):
        errors.append("source_type does not match URL domain")
    if isinstance(record.get("summary"), str) and len(record["summary"]) > MAX_SUMMARY:
        errors.append("summary too long")
    try:
        stamp = datetime.fromisoformat(record.get("observed_at", "").replace("Z", "+00:00"))
        if stamp.tzinfo is None:
            errors.append("observed_at must include timezone")
    except (ValueError, AttributeError):
        errors.append("invalid observed_at")
    if record.get("contains_personal_data") is not False:
        errors.append("contains_personal_data must explicitly be false for this public intake")
    if record.get("rights_basis") == "participant_consented":
        errors.append("participant records require a separate restricted consent workflow")
    if record.get("rights_basis") == "permission_pending":
        errors.append("permission pending; do not ingest")
    return errors

def classify(record):
    errors = validate(record)
    if errors:
        return {"accepted": False, "errors": errors}
    stable = {k: record[k] for k in sorted(REQUIRED)}
    digest = hashlib.sha256(json.dumps(stable, sort_keys=True, ensure_ascii=False).encode("utf-8")).hexdigest()
    return {
        "accepted": True, "intake_id": "GRI-" + digest[:16],
        "sha256": digest, "source_type": record["source_type"],
        "url": record["url"], "title": record["title"],
        "observed_at": record["observed_at"], "summary": record["summary"],
        "rights_basis": record["rights_basis"], "contains_personal_data": False,
        "evidence_class": "UNVERIFIED_SOURCE_CANDIDATE",
        "review_status": "HUMAN_REVIEW_REQUIRED",
        "training_eligible": False, "publication_approved": False,
        "automated_promotion_allowed": False,
        "processed_at": datetime.now(timezone.utc).isoformat(),
    }

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", type=Path)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    if args.input.resolve() == args.output.resolve():
        parser.error("input and output must differ")
    with args.input.open(encoding="utf-8") as source, args.output.open("w", encoding="utf-8") as target:
        for line in source:
            if not line.strip():
                continue
            try:
                record = classify(json.loads(line))
            except json.JSONDecodeError:
                record = {"accepted": False, "errors": ["invalid JSON"]}
            target.write(json.dumps(record, ensure_ascii=False) + "\n")

if __name__ == "__main__":
    main()
