"""Deterministic stateful agent-policy evaluation; synthetic research, no ML training."""
import hashlib
import json
from runner import institutional, technical_only

def canonical(obj):
    return json.dumps(obj,sort_keys=True,separators=(",",":")).encode("utf-8")

def run_trajectory(trajectory, enforce=True):
    """Evaluate each proposed action against current policy state, not initial approval."""
    if not trajectory.get("synthetic_only") is True:
        raise ValueError("Synthetic-only trajectories")
    state=dict(trajectory["initial"])
    required={"token","mandate","consent","revoked","conflict","operator","separated","action"}
    if set(state)!=required:
        raise ValueError("Unexpected state fields")
    decisions=[]
    previous="0"*64
    for i,event in enumerate(trajectory["events"]):
        if set(event)!={"update","propose"}:
            raise ValueError("Unexpected event fields")
        update=event["update"]
        if not isinstance(update,dict) or not set(update).issubset(required-{"action"}):
            raise ValueError("Unexpected policy update")
        state.update(update)
        case=dict(state)
        case["action"]=event["propose"]
        baseline=technical_only(case)
        controlled=institutional(case)
        allowed=controlled if enforce else baseline
        record={"step":i,"proposed_action":event["propose"],"baseline_allow":baseline,
                "institutional_allow":controlled,"actual_allow":allowed,
                "state_digest":hashlib.sha256(canonical(state)).hexdigest(),"previous_digest":previous}
        record["digest"]=hashlib.sha256(canonical(record)).hexdigest()
        previous=record["digest"]
        decisions.append(record)
    return {"trajectory_id":trajectory["id"],"enforced":enforce,
            "events":decisions,"head_digest":previous}

def replay_verify(report):
    prev="0"*64
    for i,record in enumerate(report["events"]):
        if record["step"]!=i or record["previous_digest"]!=prev:
            return False
        body={k:v for k,v in record.items() if k!="digest"}
        if hashlib.sha256(canonical(body)).hexdigest()!=record["digest"]:
            return False
        prev=record["digest"]
    return report["head_digest"]==prev
