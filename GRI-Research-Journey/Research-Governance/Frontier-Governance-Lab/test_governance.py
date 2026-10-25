import unittest
from dataclasses import replace
from governance import Metrics, Policy, Request, Decision, assess


class GovernanceTests(unittest.TestCase):
    def setUp(self):
        self.policy = Policy()
        self.frontier = Metrics(0.12, 0.04, 0.18, 4)

    def test_frontier_routes_review(self):
        self.assertEqual(self.policy.evaluate(self.frontier), Decision.REVIEW)

    def test_hard_limit_denies_even_with_human_approval(self):
        req = Request("r1", "agent", "write", True, replace(self.frontier, escalation=0.21))
        self.assertEqual(assess(req, self.policy, True)["decision"], "DENY")

    def test_missing_authorization_denies(self):
        req = Request("r2", "agent", "read", False, self.frontier)
        self.assertEqual(assess(req, self.policy, True)["decision"], "DENY")

    def test_review_requires_approval(self):
        req = Request("r3", "agent", "read", True, self.frontier)
        self.assertEqual(assess(req, self.policy)["decision"], "REVIEW")
        self.assertEqual(assess(req, self.policy, True)["decision"], "ALLOW")

    def test_standard_allowed(self):
        req = Request("r4", "agent", "read", True, Metrics(0.1, 0.03, 0.05, 2))
        self.assertEqual(assess(req, self.policy)["decision"], "ALLOW")

    def test_invalid_values_rejected(self):
        for value in (float("nan"), float("inf"), -0.1, 1.1):
            with self.assertRaises(ValueError):
                Metrics(value, 0.01, 0.02, 2)

    def test_deterministic_audit_digest(self):
        req = Request("r5", "agent", "read", True, self.frontier)
        self.assertEqual(assess(req, self.policy), assess(req, self.policy))
        self.assertEqual(len(assess(req, self.policy)["record_sha256"]), 64)


if __name__ == "__main__":
    unittest.main()
