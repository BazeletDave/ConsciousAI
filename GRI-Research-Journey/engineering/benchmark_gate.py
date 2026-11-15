"""Research benchmark eligibility. Synthetic examples never authorize model promotion."""
import hashlib
import json
from datetime import datetime

def _digest(item):
    payload = {k: item[k] for k in ("record_id", "label", "split", "source_id")}
    return hashlib.sha256(json.dumps(payload, sort_keys=True, separators=(",", ":")).encode()).hexdigest()

def assess_benchmark(rows, *, synthetic=False):
    if not isinstance(rows, list) or not rows:
        raise ValueError("benchmark must contain records")
    seen_ids, seen_sources = set(), {}
    counts = {"train": 0, "validation": 0, "test": 0}
    findings = []
    for index, row in enumerate(rows):
        if not isinstance(row, dict):
            raise ValueError("row must be an object")
        for key in ("record_id", "source_id", "split", "observed_at"):
            if not isinstance(row.get(key), str) or not row[key].strip() or row[key] != row[key].strip():
                raise ValueError("invalid " + key)
        if type(row.get("label")) is not int or row["label"] not in (0, 1):
            raise ValueError("label must be binary integer")
        if row["split"] not in counts:
            raise ValueError("invalid split")
        dt = datetime.fromisoformat(row["observed_at"].replace("Z", "+00:00"))
        if dt.tzinfo is None:
            raise ValueError("observed_at must be timezone-aware")
        counts[row["split"]] += 1
        if row["record_id"] in seen_ids:
            findings.append("duplicate_record_id")
        seen_ids.add(row["record_id"])
        prior = seen_sources.setdefault(row["source_id"], row["split"])
        if prior != row["split"]:
            findings.append("source_leakage_across_splits")
        reviewers = row.get("reviews", [])
        if not isinstance(reviewers, list):
            raise ValueError("reviews must be an array")
        digest = _digest(row)
        reviewer_decisions = {}
        for review in reviewers:
            if not isinstance(review, dict) or review.get("record_digest") != digest:
                continue
            reviewer_id = review.get("reviewer_id")
            if (not isinstance(reviewer_id, str) or not reviewer_id.strip()
                    or reviewer_id != reviewer_id.strip()):
                continue
            reviewer_decisions.setdefault(reviewer_id, set()).add(review.get("decision"))
        if any(len(decisions) > 1 for decisions in reviewer_decisions.values()):
            findings.append("conflicting_reviewer_decisions")
        eligible_reviews = {
            reviewer_id for reviewer_id, decisions in reviewer_decisions.items()
            if decisions == {"approve_label"}
        }
        if len(eligible_reviews) < 2:
            findings.append("independent_label_review_pending")
    if not all(counts.values()):
        findings.append("missing_required_split")
    if synthetic:
        findings.append("synthetic_data_not_eligible")
    return {
        "records": len(rows), "splits": counts,
        "findings": sorted(set(findings)),
        "benchmark_eligible": not findings,
        "model_promotion_eligible": False,
        "publication_authorized": False,
        "notice": "Review identity and independence must be verified outside this prototype. Benchmark eligibility is not model approval."
    }
