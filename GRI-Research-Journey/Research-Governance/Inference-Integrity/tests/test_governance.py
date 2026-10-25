import sys
import unittest
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from governance import GRIGovernanceMLPlatform, replay

class GovernanceTests(unittest.TestCase):
    def setUp(self):
        self.p = GRIGovernanceMLPlatform({"race_ethnicity": ["zip_code"]})
        self.f = {"debt_to_income": 0.55, "zip_code": "90210"}
        self.r = self.p.evaluate("synthetic-1", self.f, lambda _: 0.88, "mock-v1",
                                 {"zip_code": -0.30})

    def test_policy_and_proxy_screen(self):
        self.assertEqual(self.r.decision, "BLOCKED_BY_POLICY")
        self.assertEqual(len(self.r.proxy_review_flags), 1)

    def test_chain_and_anchor(self):
        self.assertTrue(self.p.ledger.verify(self.r.ledger_hash))
        self.assertFalse(self.p.ledger.verify("incorrect-anchor"))

    def test_snapshot_protects_caller_mutation(self):
        self.f["zip_code"] = "changed"
        self.assertTrue(self.p.ledger.verify())

    def test_replay(self):
        record = self.p.ledger.snapshot()[-1]
        self.assertEqual(replay(record, lambda _: 0.88, "mock-v1"), "PASS_SCORE_REPLAY_ONLY")
        self.assertEqual(replay(record, lambda _: 0.7, "mock-v1"), "FAIL_SCORE_MISMATCH")
        self.assertEqual(replay(record, lambda _: 0.88, "wrong"), "INSUFFICIENT_EVIDENCE_VERSION_MISMATCH")

    def test_invalid_input(self):
        with self.assertRaises(ValueError):
            self.p.evaluate("bad", {"debt_to_income": None}, lambda _: 0.9, "mock-v1")

if __name__ == "__main__":
    unittest.main()
