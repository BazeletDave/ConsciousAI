"""Audit JSONL data integrity and coverage. No external dependencies."""
import argparse
import collections
import hashlib
import json
import sys
from pathlib import Path

LABELS = {"authorized", "approval_required", "prohibited"}
SPLITS = {"train", "validation", "test"}
STYLES = {"formal", "plain"}
REQUIRED = {"record_id", "scenario_id", "policy", "request", "expected_label", "rationale", "style", "split", "source", "review_status"}


def audit(path):
    raw = Path(path).read_bytes()
    rows, errors = [], []
    for line_num, line in enumerate(raw.decode("utf-8").splitlines(), 1):
        if not line.strip():
            continue
        try:
            row = json.loads(line)
        except json.JSONDecodeError:
            errors.append(f"line {line_num}: invalid JSON")
            continue
        if not isinstance(row, dict):
            errors.append(f"line {line_num}: expected an object")
            continue
        missing = sorted(k for k in REQUIRED if not isinstance(row.get(k), str) or not row[k].strip())
        if missing:
            errors.append(f"line {line_num}: missing or invalid fields {missing}")
            continue
        for field, allowed in [("expected_label", LABELS), ("split", SPLITS), ("style", STYLES)]:
            if row[field] not in allowed:
                errors.append(f"line {line_num}: invalid {field}")
        if row["source"] != "synthetic_authored_fixture":
            errors.append(f"line {line_num}: unsupported source for this fixture audit")
        if row["review_status"] != "pending_human_review":
            errors.append(f"line {line_num}: fixture must retain pending human review status")
        rows.append(row)
    if not rows:
        errors.append("no valid records")
    ids = collections.Counter(r["record_id"] for r in rows)
    for key, count in ids.items():
        if count > 1:
            errors.append(f"duplicate record_id: {key}")
    scenarios = collections.defaultdict(list)
    content_splits = collections.defaultdict(set)
    for row in rows:
        scenarios[row["scenario_id"]].append(row)
        normalized = " ".join((row["policy"] + " " + row["request"]).casefold().split())
        content_splits[normalized].add(row["split"])
    for key, records in scenarios.items():
        if len({r["split"] for r in records}) > 1:
            errors.append(f"scenario split leakage: {key}")
        if len(records) != 2 or {r["style"] for r in records} != STYLES:
            errors.append(f"scenario requires one formal and one plain record: {key}")
        if len({r["expected_label"] for r in records}) != 1:
            errors.append(f"paired label inconsistency: {key}")
        if len({r["policy"] for r in records}) != 1:
            errors.append(f"paired policy inconsistency: {key}")
    if any(len(s) > 1 for s in content_splits.values()):
        errors.append("exact normalized policy and request overlap across splits")
    by_split = {}
    for split in sorted(SPLITS):
        subset = [r for r in rows if r["split"] == split]
        labels = collections.Counter(r["expected_label"] for r in subset)
        styles = collections.Counter(r["style"] for r in subset)
        by_split[split] = {"records": len(subset), "label_counts": dict(sorted(labels.items())), "style_counts": dict(sorted(styles.items()))}
        if set(labels) != LABELS:
            errors.append(f"missing label coverage in {split}")
        cells = collections.Counter((r["expected_label"], r["style"]) for r in subset)
        if any(cells[(label, style)] == 0 for label in LABELS for style in STYLES):
            errors.append(f"missing label and style cell in {split}")
    return {"audit_version": "0.1.0", "dataset_sha256": hashlib.sha256(raw).hexdigest(), "records": len(rows), "scenarios": len(scenarios), "by_split": by_split, "integrity_passed": not errors, "errors": errors, "human_review_complete": False, "training_release_approved": False, "interpretation": "Integrity and design coverage only. This audit does not establish fairness, model performance, demographic representation, or freedom from bias."}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("dataset", type=Path)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    try:
        result = audit(args.dataset)
    except (OSError, UnicodeDecodeError) as exc:
        parser.exit(2, f"Cannot read dataset: {exc}\n")
    text = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.write_text(text, encoding="utf-8")
    else:
        sys.stdout.write(text)
    return 0 if result["integrity_passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
