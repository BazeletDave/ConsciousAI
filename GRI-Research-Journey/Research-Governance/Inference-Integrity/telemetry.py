"""GRI telemetry contract and isolated concurrency demonstration; no Render integration."""
from __future__ import annotations
from dataclasses import dataclass, asdict
from datetime import datetime, timezone
from copy import deepcopy
from math import isfinite
from threading import RLock, Event, Thread
from typing import Any
import json

VALID_EVIDENCE = {"NOT_TESTED", "PASS_SCORE_REPLAY_ONLY", "FAIL_SCORE_MISMATCH",
                  "INSUFFICIENT_EVIDENCE", "FAIL_CHAIN_VERIFICATION"}

@dataclass(frozen=True)
class GovernancePayload:
    timestamp: str
    inference_integrity_score: float
    active_policy_violations: int
    pending_human_reviews: int
    replay_status: str
    chain_status: str
    block_index: int
    source: str = "SYNTHETIC"

def validate_payload(p: GovernancePayload) -> bool:
    if not isinstance(p, GovernancePayload) or p.source != "SYNTHETIC":
        return False
    try:
        dt = datetime.fromisoformat(p.timestamp)
        if dt.tzinfo is None or dt.utcoffset() is None:
            return False
    except (ValueError, TypeError):
        return False
    score = p.inference_integrity_score
    if isinstance(score, bool) or not isinstance(score, (float, int)) or not isfinite(score) or not 0 <= score <= 1:
        return False
    if any(isinstance(n, bool) or not isinstance(n, int) or n < 0
           for n in (p.active_policy_violations, p.pending_human_reviews, p.block_index)):
        return False
    return p.replay_status in VALID_EVIDENCE and p.chain_status in {"VERIFIED_LOCAL", "FAILED", "NOT_TESTED"}

class InstitutionalDashboardState:
    """Thread-safe snapshots inside one process; not a distributed state store."""
    def __init__(self):
        self._lock = RLock()
        self._research: dict[str, Any] = {"status": "NOT_CONNECTED"}
        self._governance: GovernancePayload | None = None

    def update_research(self, data: dict[str, Any]) -> None:
        with self._lock:
            self._research = deepcopy(data)

    def ingest(self, payload: GovernancePayload) -> bool:
        if not validate_payload(payload):
            return False
        with self._lock:
            if self._governance is not None and payload.block_index <= self._governance.block_index:
                return False
            self._governance = payload
        return True

    def snapshot(self) -> dict[str, Any]:
        with self._lock:
            research = deepcopy(self._research)
            governance = asdict(self._governance) if self._governance else None
        return {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "research_intelligence": research,
            "governance_indicators": governance,
            "integration": {
                "research_scheduler_status": "NOT_VERIFIED",
                "telemetry_source": "SYNTHETIC" if governance else "NOT_CONNECTED",
                "scope": "SINGLE_PROCESS_DEMONSTRATION",
            },
        }

def demonstration() -> dict[str, Any]:
    state = InstitutionalDashboardState()
    stop = Event()
    def worker():
        if not stop.is_set():
            state.update_research({"last_update": datetime.now(timezone.utc).isoformat(),
                                   "research_cycle_status": "SYNTHETIC_DEMONSTRATION"})
    thread = Thread(target=worker, daemon=True)
    thread.start()
    thread.join(timeout=2)
    if thread.is_alive():
        raise RuntimeError("demonstration worker did not finish")
    payload = GovernancePayload(datetime.now(timezone.utc).isoformat(), 1.0, 1, 0,
                                "PASS_SCORE_REPLAY_ONLY", "VERIFIED_LOCAL", 1)
    assert state.ingest(payload)
    stop.set()
    return state.snapshot()

if __name__ == "__main__":
    print(json.dumps(demonstration(), indent=2))
