"""Offline IAF reproduction runner; stdlib only, synthetic data only."""
import hashlib
import json
import platform
import sys
import unittest
from pathlib import Path
from runner import evaluate
from stateful_agent import run_trajectory, replay_verify

ROOT=Path(__file__).resolve().parent

def load(name):
    return json.loads((ROOT/name).read_text(encoding="utf-8"))

def digest(name):
    return hashlib.sha256((ROOT/name).read_bytes()).hexdigest()

def reproduce():
    fixtures=evaluate(load("fixtures.json"))
    trajectory=load("trajectory.json")
    controlled=run_trajectory(trajectory,enforce=True)
    comparator=run_trajectory(trajectory,enforce=False)
    if not replay_verify(controlled) or not replay_verify(comparator):
        raise AssertionError("Replay verification failed")
    assert [x["actual_allow"] for x in controlled["events"]]==[True,False,False,False,False]
    assert [x["actual_allow"] for x in comparator["events"]]==[True]*5
    assert fixtures["intervention"]["false_approvals"]==0
    return {"schema_version":"1.0","synthetic_only":True,"python_version":platform.python_version(),
        "fixture_sha256":digest("fixtures.json"),"trajectory_sha256":digest("trajectory.json"),
        "fixture_evaluation":fixtures,"controlled_trajectory":controlled,
        "baseline_trajectory":comparator,"independent_review_completed":False,
        "limitations":"Deterministic synthetic examples; no actual ML/RL training, independent audit, or production security certification."}

if __name__=="__main__":
    suite=unittest.defaultTestLoader.discover(str(ROOT),pattern="test_*.py",top_level_dir=str(ROOT))
    result=unittest.TextTestRunner(verbosity=2,stream=sys.stderr).run(suite)
    if not result.wasSuccessful():
        sys.exit(1)
    print(json.dumps(reproduce(),sort_keys=True,indent=2))
