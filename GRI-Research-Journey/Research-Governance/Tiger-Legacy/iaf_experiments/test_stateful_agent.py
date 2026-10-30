"""Stateful governance and digest-replay tests, Python standard library only."""
import copy
import json
import unittest
from pathlib import Path
from stateful_agent import run_trajectory, replay_verify
T=json.loads((Path(__file__).resolve().parent/"trajectory.json").read_text())

class StatefulTests(unittest.TestCase):
    def test_enforced_action_recheck(self):
        report=run_trajectory(T)
        self.assertEqual([x["actual_allow"] for x in report["events"]],[True,False,False,False,False])
        self.assertTrue(replay_verify(report))
    def test_baseline_false_approvals(self):
        report=run_trajectory(T,enforce=False)
        self.assertEqual([x["actual_allow"] for x in report["events"]],[True,True,True,True,True])
    def test_tamper_detected(self):
        report=run_trajectory(T)
        report["events"][1]["actual_allow"]=True
        self.assertFalse(replay_verify(report))
    def test_reorder_detected(self):
        report=run_trajectory(T)
        report["events"][0],report["events"][1]=report["events"][1],report["events"][0]
        self.assertFalse(replay_verify(report))
    def test_reproducibility(self):
        self.assertEqual(run_trajectory(T),run_trajectory(copy.deepcopy(T)))
    def test_rejects_extra_state_fields(self):
        bad=copy.deepcopy(T);bad["initial"]["client"]="not allowed"
        with self.assertRaises(ValueError):run_trajectory(bad)
    def test_rejects_non_synthetic(self):
        bad=copy.deepcopy(T);bad["synthetic_only"]=False
        with self.assertRaises(ValueError):run_trajectory(bad)

if __name__=="__main__":unittest.main()
