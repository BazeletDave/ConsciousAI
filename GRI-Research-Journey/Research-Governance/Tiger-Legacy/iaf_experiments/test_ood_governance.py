"""Regression tests for out-of-vocabulary synthetic agent requests."""
import unittest
from ood_governance import OOD_CASES,evaluate_ood,safe_gate
from qlearning_governance import STATES,ACTIONS,permitted

class OODTests(unittest.TestCase):
    def test_ood_rejected(self):
        for c in OOD_CASES:
            self.assertFalse(safe_gate(c["state"],c["action"]))
    def test_in_distribution_unchanged(self):
        for s in STATES:
            for a in ACTIONS:
                self.assertEqual(safe_gate(s,a),permitted(s,a))
    def test_all_ood_unknown(self):
        result=evaluate_ood()
        self.assertEqual(result["unknown_pairs"],len(OOD_CASES))
        self.assertEqual(result["governed_false_approvals"],0)
    def test_deterministic(self):
        self.assertEqual(evaluate_ood(),evaluate_ood())
    def test_unseen_export_variants(self):
        self.assertFalse(safe_gate("authorized","bulk_export"))
        self.assertFalse(safe_gate("authorized","delegate"))

if __name__=="__main__":
    unittest.main()
