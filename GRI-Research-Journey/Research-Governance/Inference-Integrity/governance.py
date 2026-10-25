"""GRI inference integrity research prototype. Synthetic/offline use only."""
from __future__ import annotations
from dataclasses import dataclass, field
from datetime import datetime, timezone
from hashlib import sha256
from copy import deepcopy
import json
import math
from typing import Any, Callable

def canonical(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), allow_nan=False)

def digest(value: Any) -> str:
    return sha256(canonical(value).encode("utf-8")).hexdigest()

@dataclass(frozen=True)
class AuditRecord:
    index: int
    timestamp: str
    prediction_id: str
    model_version: str
    features: dict
    raw_score: float
    policy_version: str
    decision: str
    reasons: tuple[str, ...]
    previous_hash: str
    record_hash: str

class GovernanceLedger:
    """In-memory hash chain: detects edits if checked against trusted anchors.
    Not immutable storage, a blockchain, or regulatory certification.
    """
    def __init__(self):
        self._records: list[AuditRecord] = []

    def append(self, prediction_id: str, model_version: str, features: dict,
               raw_score: float, policy_version: str, decision: str,
               reasons: list[str]) -> AuditRecord:
        if not math.isfinite(raw_score) or not 0 <= raw_score <= 1:
            raise ValueError("score must be a finite probability")
        previous = self._records[-1].record_hash if self._records else "GENESIS"
        body = dict(index=len(self._records),
                    timestamp=datetime.now(timezone.utc).isoformat(),
                    prediction_id=prediction_id, model_version=model_version,
                    features=deepcopy(features), raw_score=raw_score,
                    policy_version=policy_version, decision=decision,
                    reasons=tuple(reasons), previous_hash=previous)
        hashed = digest(body)
        record = AuditRecord(**body, record_hash=hashed)
        self._records.append(record)
        return record

    def verify(self, trusted_tip: str | None = None) -> bool:
        previous = "GENESIS"
        for index, record in enumerate(self._records):
            body = {k: deepcopy(getattr(record, k)) for k in record.__dataclass_fields__
                    if k != "record_hash"}
            if record.index != index or record.previous_hash != previous:
                return False
            if digest(body) != record.record_hash:
                return False
            previous = record.record_hash
        return trusted_tip is None or (bool(self._records) and previous == trusted_tip)

    def snapshot(self) -> tuple[AuditRecord, ...]:
        return tuple(deepcopy(self._records))

@dataclass(frozen=True)
class GovernanceResult:
    prediction_id: str
    raw_score: float
    decision: str
    reasons: tuple[str, ...]
    proxy_review_flags: tuple[str, ...]
    recourse_status: str
    ledger_hash: str
    replay_status: str = "NOT_TESTED"

class GRIGovernanceMLPlatform:
    """A research policy gate, not a validated fairness or credit decision system."""
    POLICY_VERSION = "synthetic-credit-policy-v0.2"

    def __init__(self, proxy_candidates: dict[str, list[str]] | None = None):
        self.ledger = GovernanceLedger()
        self.proxy_candidates = proxy_candidates or {}

    def evaluate(self, prediction_id: str, features: dict,
                 model: Callable[[dict], float], model_version: str,
                 attributions: dict[str, float] | None = None) -> GovernanceResult:
        # Fail closed on missing/invalid values and never mutate caller input.
        snapshot = deepcopy(features)
        score = float(model(deepcopy(snapshot)))
        if not math.isfinite(score) or not 0 <= score <= 1:
            raise ValueError("invalid model score")
        dti = snapshot.get("debt_to_income")
        if not isinstance(dti, (float, int)) or isinstance(dti, bool) or not 0 <= dti <= 1:
            raise ValueError("invalid or missing debt_to_income")
        reasons = []
        if dti > 0.50 and score > 0.85:
            reasons.append("Synthetic credit risk policy threshold triggered")
        decision = "BLOCKED_BY_POLICY" if reasons else "POLICY_PASSED"
        attrs = attributions or {}
        flags = []
        for protected, candidates in self.proxy_candidates.items():
            for name in candidates:
                weight = attrs.get(name)
                if name in snapshot and isinstance(weight, (int, float)) and math.isfinite(weight) and abs(weight) > 0.25:
                    flags.append(f"{name}: candidate proxy for {protected}; empirical validation required")
        record = self.ledger.append(prediction_id, model_version, snapshot, score,
                                    self.POLICY_VERSION, decision, reasons)
        return GovernanceResult(prediction_id, score, decision, tuple(reasons),
                                tuple(flags), "NOT_VALIDATED_NO_ACTIONABLE_RECOURSE",
                                record.record_hash)

def replay(record: AuditRecord, historical_model: Callable[[dict], float],
           expected_model_version: str, tolerance: float = 1e-9) -> str:
    """Only score replay; model artifact provenance and environment require separate evidence."""
    if record.model_version != expected_model_version:
        return "INSUFFICIENT_EVIDENCE_VERSION_MISMATCH"
    try:
        score = float(historical_model(deepcopy(record.features)))
        if not math.isfinite(score):
            return "FAIL_INVALID_SCORE"
        return "PASS_SCORE_REPLAY_ONLY" if abs(score-record.raw_score) <= tolerance else "FAIL_SCORE_MISMATCH"
    except Exception:
        return "INSUFFICIENT_EVIDENCE_REPLAY_ERROR"

if __name__ == "__main__":
    p = GRIGovernanceMLPlatform({"race_ethnicity": ["zip_code"]})
    model = lambda x: 0.88
    result = p.evaluate("SYNTHETIC-001", {"income": 50000, "debt_to_income": 0.55,
                       "zip_code": "90210"}, model, "mock-v1", {"zip_code": -0.30})
    print(json.dumps(result.__dict__, indent=2))
    print("chain_valid:", p.ledger.verify(result.ledger_hash))
    print("replay:", replay(p.ledger.snapshot()[-1], model, "mock-v1"))
