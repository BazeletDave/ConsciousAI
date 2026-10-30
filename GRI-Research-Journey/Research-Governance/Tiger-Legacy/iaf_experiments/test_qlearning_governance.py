"""Held-out learning and governance regression tests."""
import unittest
from qlearning_governance import qtrain,evaluate,permitted,ACTIONS,STATES

class QLearningGovernanceTests(unittest.TestCase):
    def test_reproducible_learning(self):
        self.assertEqual(qtrain(),qtrain())
    def test_seed_separation(self):
        with self.assertRaises(ValueError):evaluate(seed=17,heldout_seed=17)
    def test_heldout_governance(self):
        r=evaluate()
        self.assertEqual(r["heldout_decisions"],400)
        self.assertGreater(r["unsafe_proposals"],0)
        self.assertEqual(r["governed_false_approvals"],0)
        self.assertGreater(r["baseline_false_approvals"],0)
    def test_policy_matrix(self):
        for state in STATES:
            for action in ACTIONS:
                self.assertEqual(permitted(state,action),state=="authorized" and action=="read")
    def test_seeded_result_repeat(self):
        self.assertEqual(evaluate(),evaluate())
    def test_alternate_heldout_seed(self):
        r=evaluate(heldout_seed=1234)
        self.assertEqual(r["governed_false_approvals"],0)
        self.assertNotEqual(r["heldout_trace_sha256"],evaluate()["heldout_trace_sha256"])

if __name__=="__main__":
    unittest.main()
