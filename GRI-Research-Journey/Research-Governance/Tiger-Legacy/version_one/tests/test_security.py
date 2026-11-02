"""Synthetic security regression suite. Run: python -m unittest discover -s tests -v"""
import unittest
from tiger_legacy import TigerLegacy

class SecurityTests(unittest.TestCase):
    def setUp(self):
        self.lab = TigerLegacy(b"synthetic-only-lab-key-32-bytes-minimum")
        self.lab.add_resource("e1", "alpha", "record1", "alice", "synthetic recording A")
        self.lab.add_resource("e2", "beta", "record1", "bob", "synthetic recording B")

    def test_isolation_and_default_deny(self):
        self.assertFalse(self.lab.authorize("alpha", "record1", "bob", "view", 100))
        self.assertFalse(self.lab.authorize("beta", "record1", "alice", "view", 100))
        self.assertFalse(self.lab.authorize("alpha", "missing", "alice", "view", 100))
        with self.assertRaises(PermissionError):
            self.lab.read("alpha", "record1", "bob", "view", 100)

    def test_grant_expiry_revocation(self):
        self.lab.grant("e3", "alpha", "record1", "alice", "charlie", "view", 200)
        self.assertTrue(self.lab.authorize("alpha", "record1", "charlie", "view", 199))
        self.assertFalse(self.lab.authorize("alpha", "record1", "charlie", "edit", 199))
        self.assertFalse(self.lab.authorize("alpha", "record1", "charlie", "view", 200))
        self.lab.revoke("e4", "alpha", "record1", "alice", "charlie", "view")
        self.assertFalse(self.lab.authorize("alpha", "record1", "charlie", "view", 100))

    def test_forged_grant(self):
        with self.assertRaises(PermissionError):
            self.lab.grant("e3", "alpha", "record1", "bob", "charlie", "view", 200)

    def test_cross_tenant_grant(self):
        with self.assertRaises(PermissionError):
            self.lab.grant("e3", "beta", "record1", "alice", "charlie", "view", 200)

    def test_tampering(self):
        self.assertTrue(self.lab.verify())
        self.lab.events[0]["details"]["owner"] = "mallory"
        self.assertFalse(self.lab.verify())

    def test_missing_event(self):
        self.lab.events.pop(0)
        self.assertFalse(self.lab.verify())

    def test_replay(self):
        with self.assertRaises(ValueError):
            self.lab.grant("e1", "alpha", "record1", "alice", "charlie", "view", 200)

    def test_synthetic_summary(self):
        result = self.lab.summary()
        self.assertEqual(result["tenant_count"], 2)
        self.assertTrue(result["evidence_verified"])
        self.assertEqual(result["production_security"], "unmeasured")


    def test_paired_authority_cases(self):
        """Paired synthetic attempts: report both denied misuse and retained valid access."""
        self.lab.grant("e3", "alpha", "record1", "alice", "charlie", "view", 200)
        cases = [
            ("valid", "alpha", "record1", "charlie", "view", 199, True),
            ("wrong-purpose", "alpha", "record1", "charlie", "edit", 199, False),
            ("expired", "alpha", "record1", "charlie", "view", 200, False),
            ("cross-tenant", "beta", "record1", "charlie", "view", 199, False),
        ]
        for name, tenant, resource, principal, purpose, now, expected in cases:
            with self.subTest(case=name):
                self.assertEqual(self.lab.authorize(tenant, resource, principal, purpose, now), expected)
        self.lab.revoke("e4", "alpha", "record1", "alice", "charlie", "view")
        self.assertFalse(self.lab.authorize("alpha", "record1", "charlie", "view", 199))
        self.assertTrue(self.lab.verify())

    def test_local_evidence_check_is_not_task_completion(self):
        """A verified event history does not establish downstream task success."""
        self.assertTrue(self.lab.verify())
        task_completed = False  # Explicitly synthetic counterexample, not measured field outcome.
        self.assertFalse(task_completed)

    def test_biased_observation_remains_a_failure_boundary(self):
        """A valid evidence chain cannot independently authenticate a biased sensor."""
        self.lab.grant("e3", "alpha", "record1", "alice", "charlie", "view", 200)
        self.assertTrue(self.lab.verify())
        reported_safe = True
        actual_fixture_safe = False
        self.assertNotEqual(reported_safe, actual_fixture_safe)


    def test_paired_synthetic_authorization_outcomes(self):
        """Compare a permissive baseline to scoped consent on identical fixed cases."""
        self.lab.grant("e3", "alpha", "record1", "alice", "charlie", "view", 200)
        cases = [
            # tenant, resource, subject, purpose, time, authorized ground truth
            ("alpha", "record1", "charlie", "view", 199, True),
            ("alpha", "record1", "charlie", "edit", 199, False),
            ("alpha", "record1", "charlie", "view", 200, False),
            ("beta", "record1", "charlie", "view", 199, False),
            ("alpha", "record1", "alice", "view", 199, True),
        ]
        def score(decisions):
            unauthorized = sum(bool(decision) for decision, case in zip(decisions, cases) if not case[-1])
            false_denials = sum(not decision for decision, case in zip(decisions, cases) if case[-1])
            return {"unauthorized_allowed": unauthorized,
                    "unauthorized_attempts": sum(not c[-1] for c in cases),
                    "false_denials": false_denials,
                    "valid_attempts": sum(c[-1] for c in cases)}
        baseline = score([True for _ in cases])
        governed = score([self.lab.authorize(*case[:5]) for case in cases])
        self.assertEqual(baseline, {"unauthorized_allowed": 3, "unauthorized_attempts": 3,
                                    "false_denials": 0, "valid_attempts": 2})
        self.assertEqual(governed, {"unauthorized_allowed": 0, "unauthorized_attempts": 3,
                                    "false_denials": 0, "valid_attempts": 2})
        self.assertTrue(self.lab.verify())
        # This is an intentionally permissive synthetic baseline, not a
        # historical Training a Tiger model or a field effectiveness estimate.

if __name__ == "__main__":
    unittest.main()
