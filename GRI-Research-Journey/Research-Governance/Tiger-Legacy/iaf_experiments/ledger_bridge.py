"""Synthetic-only bridge to existing Tiger Legacy SQLite evidence ledger.

Does not modify original research or production paths.
"""
import hashlib
import json
import sys
from pathlib import Path

LEGACY_ROOT=Path(__file__).resolve().parents[1]/"version_one"
if str(LEGACY_ROOT) not in sys.path:
    sys.path.insert(0,str(LEGACY_ROOT))
from evidence_ledger import EvidenceLedger
from stateful_agent import run_trajectory, replay_verify

def record_trajectory(db_path, key, trajectory):
    if trajectory.get("synthetic_only") is not True:
        raise ValueError("Synthetic-only evidence required")
    result=run_trajectory(trajectory)
    if not replay_verify(result):
        raise ValueError("Invalid synthetic trajectory")
    ledger=EvidenceLedger(db_path,key)
    for event in result["events"]:
        ledger.append("iaf-"+result["trajectory_id"]+"-"+str(event["step"]),
                      {"schema":"gri.iaf.synthetic_trajectory.v1",
                       "synthetic_only":True,"trajectory_id":result["trajectory_id"],
                       "event":event})
    checkpoint=ledger.checkpoint()
    if not ledger.verify(checkpoint):
        raise ValueError("Checkpoint verification failed")
    return {"checkpoint":checkpoint,"event_count":len(result["events"]),
            "trajectory_head":result["head_digest"],"ledger_verified":True,
            "custody":"local_only_no_external_anchor"}

def verify_export(db_path,key,checkpoint):
    return EvidenceLedger(db_path,key).verify(checkpoint)
