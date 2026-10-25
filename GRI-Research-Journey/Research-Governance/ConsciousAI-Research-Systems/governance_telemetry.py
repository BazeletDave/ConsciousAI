"""Evidence-qualified ML governance telemetry for the public GRI dashboard.

Read-only, standard-library-only; no synthetic values are presented as production metrics.
"""
from __future__ import annotations
from datetime import datetime, timezone
import json
import math
import os
from pathlib import Path

VALID_REPLAY = {"PASS_SCORE_REPLAY_ONLY", "FAIL_SCORE_MISMATCH",
                "NOT_TESTED", "INSUFFICIENT_EVIDENCE"}
VALID_CHAIN = {"VERIFIED_LOCAL", "FAILED", "NOT_TESTED"}

def validate_snapshot(data):
    if not isinstance(data, dict) or data.get("schema_version") != "1.0":
        raise ValueError("invalid schema")
    if data.get("source") != "approved_operational_telemetry":
        raise ValueError("unapproved source")
    stamp = datetime.fromisoformat(data["observed_at"])
    if stamp.tzinfo is None or stamp.utcoffset() is None:
        raise ValueError("timestamp must be timezone aware")
    if stamp > datetime.now(timezone.utc):
        raise ValueError("future timestamp")
    count = data.get("inference_count")
    passed = data.get("score_replay_pass_count")
    blocked = data.get("policy_block_count")
    pending = data.get("pending_human_review_count")
    for n in (count, passed, blocked, pending):
        if type(n) is not int or n < 0:
            raise ValueError("invalid metric count")
    if passed > count or blocked > count:
        raise ValueError("counts exceed inferences")
    if data.get("replay_status") not in VALID_REPLAY or data.get("chain_status") not in VALID_CHAIN:
        raise ValueError("invalid evidence status")
    if type(data.get("block_index")) is not int or data["block_index"] < 0:
        raise ValueError("invalid block index")
    if data.get("chain_status") == "VERIFIED_LOCAL" and not data.get("chain_tip_sha256"):
        raise ValueError("chain tip required")
    tip = data.get("chain_tip_sha256")
    if tip is not None and (not isinstance(tip, str) or len(tip) != 64 or
                            any(c not in "0123456789abcdef" for c in tip)):
        raise ValueError("invalid chain tip")
    return data

def public_snapshot(path=None):
    """Only a pre-approved JSON artifact; never ingest from public requests."""
    path = Path(path or os.environ.get("GRI_GOVERNANCE_TELEMETRY_PATH", ""))
    if not str(path) or path.is_dir() or not path.is_file():
        return {"schema_version": "1.0", "status": "not_connected",
                "source": None, "metrics": None,
                "notice": "No approved operational telemetry snapshot configured. Synthetic research metrics are not live data."}
    try:
        if path.stat().st_size > 16_384:
            raise ValueError("snapshot too large")
        data = validate_snapshot(json.loads(path.read_text(encoding="utf-8")))
    except (ValueError, TypeError, KeyError, OSError, json.JSONDecodeError):
        return {"schema_version": "1.0", "status": "invalid_source",
                "source": None, "metrics": None,
                "notice": "Telemetry source failed validation; no metrics published."}
    age = (datetime.now(timezone.utc) - datetime.fromisoformat(data["observed_at"])).total_seconds()
    if age > 4 * 3600:
        return {"schema_version": "1.0", "status": "stale",
                "source": "approved_operational_telemetry", "metrics": None,
                "observed_at": data["observed_at"],
                "notice": "Telemetry older than four hours; stale measurements withheld."}
    count = data["inference_count"]
    return {"schema_version": "1.0", "status": "source_validated_not_independently_audited",
            "source": "approved_operational_telemetry",
            "observed_at": data["observed_at"],
            "metrics": {"inference_count": count,
                        "score_replay_pass_count": data["score_replay_pass_count"],
                        "score_replay_pass_rate": (data["score_replay_pass_count"] / count if count else None),
                        "policy_block_count": data["policy_block_count"],
                        "pending_human_review_count": data["pending_human_review_count"],
                        "replay_status": data["replay_status"],
                        "chain_status": data["chain_status"],
                        "block_index": data["block_index"]},
            "notice": "Schema validated only. Local chain status is source reported, not independently verified by this endpoint; score replay does not prove full model reproducibility."}
