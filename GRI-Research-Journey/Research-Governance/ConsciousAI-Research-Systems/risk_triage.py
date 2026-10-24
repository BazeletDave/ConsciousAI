"""GRI v1.3 evidence triage. Deterministic baseline, not a trained ML model.

Scores prioritize human review; they do not establish compliance or wrongdoing.
"""
from __future__ import annotations
from collections.abc import Mapping

SCHEMA_VERSION = "1.3"
WEIGHTS = {"missing_primary_source": 35, "unreviewed": 30,
           "missing_timestamp": 15, "missing_owner": 10,
           "missing_jurisdiction": 10}


def triage(record: Mapping) -> dict:
    if not isinstance(record, Mapping):
        raise TypeError("record must be a mapping")
    reasons = []
    if not record.get("primary_source_url"):
        reasons.append("missing_primary_source")
    if record.get("verification_status") not in ("verified", "independently_verified"):
        reasons.append("unreviewed")
    if not record.get("observed_at"):
        reasons.append("missing_timestamp")
    if not record.get("review_owner"):
        reasons.append("missing_owner")
    if not record.get("jurisdiction"):
        reasons.append("missing_jurisdiction")
    score = sum(WEIGHTS[k] for k in reasons)
    return {
        "schema_version": SCHEMA_VERSION,
        "record_id": str(record.get("id", "")),
        "review_priority_score": score,
        "review_priority": "high" if score >= 60 else "medium" if score >= 30 else "low",
        "reasons": reasons,
        "requires_human_review": True,
        "method": "deterministic_missing_evidence_heuristic",
        "model_trained": False,
        "calibrated_probability": None,
        "notice": "Triage priority is not a finding of legal compliance, safety, or misconduct.",
    }
