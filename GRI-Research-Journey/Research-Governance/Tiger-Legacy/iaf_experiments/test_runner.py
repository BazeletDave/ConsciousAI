"""Reproducible, offline tests for the GRI IAF synthetic experiment."""
import copy
import json
import unittest
from pathlib import Path
from runner import evaluate, institutional, technical_only

FIXTURES=json.loads((Path(__file__).resolve().parent/"fixtures.json").read_text())

class TestIAF(unittest.TestCase):
    def test_all_expected_institutional_decisions(self):
        report=evaluate(FIXTURES)
        self.assertEqual(report["intervention"]["false_approvals"],0)
        self.assertEqual(report["intervention"]["false_denials"],0)
        self.assertEqual(report["scenario_count"],8)

    def test_baseline_exposes_institutional_gaps(self):
        report=evaluate(FIXTURES)
        self.assertGreater(report["baseline"]["false_approvals"],0)

    def test_revocation_and_adaptive_agent(self):
        cases={c["id"]:c for c in FIXTURES["scenarios"]}
        self.assertTrue(technical_only(cases["revoked_consent"]))
        self.assertFalse(institutional(cases["revoked_consent"]))
        self.assertTrue(technical_only(cases["adaptive_agent_escalation"]))
        self.assertFalse(institutional(cases["adaptive_agent_escalation"]))

    def test_deterministic_digest_and_results(self):
        self.assertEqual(evaluate(FIXTURES),evaluate(copy.deepcopy(FIXTURES)))

    def test_rejects_non_synthetic_data(self):
        bad=copy.deepcopy(FIXTURES)
        bad["synthetic_only"]=False
        with self.assertRaises(ValueError):
            evaluate(bad)

    def test_rejects_undeclared_fields(self):
        bad=copy.deepcopy(FIXTURES)
        bad["scenarios"][0]["client_name"]="not permitted"
        with self.assertRaises(ValueError):
            evaluate(bad)

    def test_rejects_duplicate_ids(self):
        bad=copy.deepcopy(FIXTURES)
        bad["scenarios"][1]["id"]=bad["scenarios"][0]["id"]
        with self.assertRaises(ValueError):
            evaluate(bad)

if __name__=="__main__":
    unittest.main()
