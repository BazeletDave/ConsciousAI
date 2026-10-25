"""GRI Frontier Governance Lab: deterministic, offline research policy engine.

Synthetic metrics are NOT validated safety measurements or regulatory determinations.
"""
from dataclasses import dataclass
from enum import Enum
from hashlib import sha256
import json
import math
from typing import Optional


class Decision(str, Enum):
    ALLOW = "ALLOW"
    REVIEW = "REVIEW"
    DENY = "DENY"


@dataclass(frozen=True)
class Metrics:
    bias: float
    hallucination: float
    escalation: float
    autonomy: int

    def __post_init__(self):
        for name in ("bias", "hallucination", "escalation"):
            value = getattr(self, name)
            if isinstance(value, bool) or not isinstance(value, (int, float)) or not math.isfinite(value) or not 0 <= value <= 1:
                raise ValueError(f"{name} must be finite and in [0,1]")
        if type(self.autonomy) is not int or not 1 <= self.autonomy <= 5:
            raise ValueError("autonomy must be integer 1..5")


@dataclass(frozen=True)
class Policy:
    version: str = "research-v0.1"
    max_bias: float = 0.15
    max_hallucination: float = 0.05
    max_escalation: float = 0.20
    review_fraction: float = 0.80

    def __post_init__(self):
        if not self.version.strip():
            raise ValueError("policy version required")
        for name in ("max_bias", "max_hallucination", "max_escalation", "review_fraction"):
            v = getattr(self, name)
            if isinstance(v, bool) or not isinstance(v, (int, float)) or not math.isfinite(v) or not 0 < v <= 1:
                raise ValueError(f"{name} must be finite and in (0,1]")

    def evaluate(self, m: Metrics) -> Decision:
        # Hard limits are never waived by sandbox review.
        if m.bias > self.max_bias or m.hallucination > self.max_hallucination or m.escalation > self.max_escalation:
            return Decision.DENY
        if m.autonomy >= 4 and m.escalation >= self.review_fraction * self.max_escalation:
            return Decision.REVIEW
        return Decision.ALLOW


@dataclass(frozen=True)
class Request:
    request_id: str
    agent_id: str
    action: str
    authorized: bool
    metrics: Metrics


def assess(req: Request, policy: Policy, human_approved: bool = False) -> dict:
    """Decision only: does not invoke tools or execute actions."""
    if not all((req.request_id.strip(), req.agent_id.strip(), req.action.strip())):
        raise ValueError("request_id, agent_id and action required")
    outcome = policy.evaluate(req.metrics)
    if not req.authorized:
        outcome = Decision.DENY
    elif outcome == Decision.REVIEW and human_approved:
        outcome = Decision.ALLOW
    record = {
        "request_id": req.request_id, "agent_id": req.agent_id,
        "action": req.action, "policy_version": policy.version,
        "metrics": vars(req.metrics), "authorized": req.authorized,
        "human_approved": human_approved, "decision": outcome.value,
        "mode": "SIMULATION_ONLY",
    }
    canonical = json.dumps(record, sort_keys=True, separators=(",", ":"), allow_nan=False)
    record["record_sha256"] = sha256(canonical.encode()).hexdigest()
    return record
