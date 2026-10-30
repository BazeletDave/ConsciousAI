"""Offline reproducibility and boundary checks for the synthetic comparison."""
import unittest
from comparative_evaluation import evaluate

class ComparativeEvaluationTests(unittest.TestCase):
    def test_deterministic(self):
        self.assertEqual(evaluate(), evaluate())
    def test_declared_fixture_denominators(self):
        m = evaluate()["metrics"]
        self.assertEqual(m["synthetic_cases"], 9)
        self.assertEqual(m["unauthorized_allowances"], {"denominator": 4, "baseline": 4, "governed": 0})
        self.assertEqual(m["legitimate_task_allowances"], {"denominator": 2, "baseline": 2, "governed": 2})
        self.assertEqual(m["hidden_change_allowances"], {"denominator": 3, "baseline": 3, "governed": 1})
        self.assertTrue(m["evidence_chain_verified"])
    def test_biased_probe_is_not_solved(self):
        rows = {r["case"]: r for r in evaluate()["cases"]}
        self.assertTrue(rows["hidden_biased"]["governed_allow"])
        self.assertFalse(rows["hidden_missing"]["governed_allow"])
        self.assertFalse(rows["hidden_trustworthy"]["governed_allow"])
    def test_no_operational_claim(self):
        self.assertEqual(evaluate()["classification"], "synthetic_fixture_demonstration_only")

if __name__ == "__main__":
    unittest.main()
