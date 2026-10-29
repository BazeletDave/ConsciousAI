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

if __name__ == "__main__":
    unittest.main()
