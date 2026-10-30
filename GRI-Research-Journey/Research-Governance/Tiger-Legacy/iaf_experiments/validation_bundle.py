"""Single-command synthetic validation bundle: fixtures, Q-learning, OOD and SQLite ledger."""
import hashlib
import json
import platform
import sys
import tempfile
import unittest
from pathlib import Path
from runner import evaluate
from stateful_agent import run_trajectory,replay_verify
from qlearning_governance import evaluate as evaluate_q
from ood_governance import evaluate_ood
from ledger_bridge import record_trajectory,verify_export

ROOT=Path(__file__).resolve().parent
KEY=b"synthetic-validation-only-not-a-production-key-2026"

def load(name):
    return json.loads((ROOT/name).read_text(encoding="utf-8"))

def validate():
    suite=unittest.defaultTestLoader.discover(str(ROOT),pattern="test_*.py",top_level_dir=str(ROOT))
    result=unittest.TextTestRunner(verbosity=2,stream=sys.stderr).run(suite)
    if not result.wasSuccessful():
        raise RuntimeError("Regression tests failed")
    fixtures=evaluate(load("fixtures.json"))
    trajectory=load("trajectory.json")
    trace=run_trajectory(trajectory)
    if not replay_verify(trace):
        raise RuntimeError("Trace replay failed")
    q=evaluate_q()
    ood=evaluate_ood()
    with tempfile.TemporaryDirectory() as directory:
        db=Path(directory)/"synthetic-ledger.sqlite3"
        ledger=record_trajectory(db,KEY,trajectory)
        if not verify_export(db,KEY,ledger["checkpoint"]):
            raise RuntimeError("Ledger verification failed")
    if fixtures["intervention"]["false_approvals"] or q["governed_false_approvals"] or ood["governed_false_approvals"]:
        raise RuntimeError("Unexpected false approval in synthetic test")
    files=("fixtures.json","trajectory.json","runner.py","stateful_agent.py","qlearning_governance.py",
           "ood_governance.py","ledger_bridge.py")
    return {"schema":"gri.iaf.validation_bundle.v1","synthetic_only":True,
            "python_version":platform.python_version(),
            "tests_run":result.testsRun,"test_failures":len(result.failures),
            "test_errors":len(result.errors),
            "inputs_sha256":{f:hashlib.sha256((ROOT/f).read_bytes()).hexdigest() for f in files},
            "fixture_results":fixtures,"stateful_trajectory":{"steps":len(trace["events"]),
                "head_digest":trace["head_digest"],"replay_verified":True},
            "qlearning_results":q,"ood_results":ood,"ledger_results":ledger,
            "review":{"academic_source_verification":"pending","independent_reproduction":"pending",
                      "external_checkpoint_custody":"not_implemented","production_ready":False},
            "limitations":"Author-designed synthetic tests; learned tabular Q values; no real clients, deep RL, externally held checkpoint, or independent validation."}

if __name__=="__main__":
    try:
        print(json.dumps(validate(),sort_keys=True,indent=2))
    except Exception as error:
        print("VALIDATION FAILED: "+str(error),file=sys.stderr)
        sys.exit(1)
