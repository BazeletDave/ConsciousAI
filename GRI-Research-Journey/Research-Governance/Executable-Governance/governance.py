"""Offline, nonpunitive research policy engine. No sensor or vehicle integrations."""
from dataclasses import dataclass, asdict
from hashlib import sha256
import json

POLICY_VERSION = "2026-10-21.1"
MIN_CONFIDENCE = 0.90  # research parameter, NOT a safety threshold

@dataclass(frozen=True)
class Event:
    event_id: str
    moving: bool
    handling_detected: bool
    driver_attribution_verified: bool
    confidence: float
    source_type: str = "synthetic"

def evaluate(event: Event):
    if not 0 <= event.confidence <= 1:
        raise ValueError("confidence must be in [0,1]")
    if event.source_type != "synthetic":
        raise ValueError("offline prototype accepts synthetic events only")
    if not event.driver_attribution_verified:
        action, reason = "NO_ACTION", "driver attribution unverified"
    elif not event.moving or not event.handling_detected:
        action, reason = "NO_ACTION", "no qualifying event"
    elif event.confidence < MIN_CONFIDENCE:
        action, reason = "REVIEW_EVIDENCE", "insufficient confidence"
    else:
        action, reason = "WARNING_PERMITTED", "synthetic policy criteria satisfied"
    record = {"event_id": event.event_id, "policy_version": POLICY_VERSION,
              "action": action, "reason": reason, "source_type": event.source_type,
              "intervention_level": 2 if action == "WARNING_PERMITTED" else 0}
    record["decision_hash"] = sha256(json.dumps(record,sort_keys=True).encode()).hexdigest()
    return record

if __name__ == "__main__":
    print(json.dumps(evaluate(Event("demo",True,True,True,0.95)),indent=2))
