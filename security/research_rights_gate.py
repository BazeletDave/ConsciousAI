"""Fail-closed rights validation for GRI research metadata. Python standard library only."""
import json
import sys
from pathlib import Path

REQUIRED = ("source_id", "author", "publisher", "url", "rights_basis", "license",
            "visibility", "ingestion_permission", "training_permission",
            "citation_locator", "content_hash", "reviewer", "review_status")
RESTRICTED = {"restricted", "private", "confidential"}
APPROVED = {"approved", "adjudicated", "release_approved"}

def validate(record):
    errors = []
    if not isinstance(record, dict):
        return ["record must be an object"]
    for field in REQUIRED:
        if field not in record:
            errors.append(f"missing {field}")
    if errors:
        return errors
    if type(record["ingestion_permission"]) is not bool or type(record["training_permission"]) is not bool:
        errors.append("permissions must be booleans")
        return errors
    if record["visibility"] in RESTRICTED and (record["ingestion_permission"] or record["training_permission"]):
        errors.append("restricted records cannot be ingested or trained by the public pipeline")
    if record["training_permission"] and not record["ingestion_permission"]:
        errors.append("training requires ingestion permission")
    if (record["ingestion_permission"] or record["training_permission"]) and record["review_status"] not in APPROVED:
        errors.append("permission requires approved human review")
    if (record["ingestion_permission"] or record["training_permission"]) and not str(record["rights_basis"]).strip():
        errors.append("permission requires a documented rights basis")
    if record["training_permission"] and not str(record["license"]).strip():
        errors.append("training requires a recorded license or authorization")
    if record["ingestion_permission"] and not str(record["reviewer"]).strip():
        errors.append("ingestion requires a reviewer")
    if record["ingestion_permission"] and not str(record["citation_locator"]).strip():
        errors.append("ingestion requires a citation locator")
    if record["ingestion_permission"] and not str(record["content_hash"]).strip():
        errors.append("ingestion requires a content hash")
    return errors

def main(paths):
    failures = 0
    for name in paths:
        try:
            data = json.loads(Path(name).read_text(encoding="utf-8"))
            records = data if isinstance(data, list) else [data]
            for i, record in enumerate(records):
                for issue in validate(record):
                    print(f"{name}[{i}]: {issue}", file=sys.stderr)
                    failures += 1
        except (OSError, ValueError) as exc:
            print(f"{name}: {exc}", file=sys.stderr)
            failures += 1
    return 1 if failures else 0

if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
