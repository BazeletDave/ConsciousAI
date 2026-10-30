"""Offline synthetic identity tests. No production authentication claims."""
import unittest
from synthetic_identity import SyntheticIdentity, authorized_read
from tiger_legacy import TigerLegacy

class SyntheticIdentityTests(unittest.TestCase):
    def setUp(self):
        self.identity = SyntheticIdentity(b"synthetic-identity-test-key-of-32-plus-bytes")
        self.lab = TigerLegacy(b"synthetic-ledger-test-key-of-32-plus-bytes")
        self.lab.add_resource("a", "alpha", "r", "alice", "private alpha")
        self.lab.add_resource("b", "beta", "r", "bob", "private beta")

    def test_valid_owner(self):
        token = self.identity.issue("alpha", "alice", 10, 100)
        self.assertEqual(authorized_read(self.lab, self.identity, token, "r", "view", 20), "private alpha")

    def test_cross_tenant_denied(self):
        token = self.identity.issue("alpha", "bob", 10, 100)
        with self.assertRaises(PermissionError):
            authorized_read(self.lab, self.identity, token, "r", "view", 20)

    def test_expiry_denied(self):
        token = self.identity.issue("alpha", "alice", 10, 20)
        with self.assertRaises(PermissionError):
            authorized_read(self.lab, self.identity, token, "r", "view", 20)

    def test_future_issue_denied(self):
        self.assertIsNone(self.identity.verify(self.identity.issue("alpha", "alice", 50, 100), 20))

    def test_tampered_token_denied(self):
        token = self.identity.issue("alpha", "alice", 10, 100)
        payload, signature = token.split(".")
        self.assertIsNone(self.identity.verify(payload + "A." + signature, 20))

    def test_wrong_key_denied(self):
        token = self.identity.issue("alpha", "alice", 10, 100)
        other = SyntheticIdentity(b"different-synthetic-test-key-of-32-bytes")
        self.assertIsNone(other.verify(token, 20))

    def test_wrong_audience_denied(self):
        token = self.identity.issue("alpha", "alice", 10, 100)
        other = SyntheticIdentity(b"synthetic-identity-test-key-of-32-plus-bytes", audience="other")
        self.assertIsNone(other.verify(token, 20))

    def test_malformed_denied(self):
        for token in ("", "abc", "a.b.c", "%%%%.%%%%", 42):
            self.assertIsNone(self.identity.verify(token, 20))

    def test_invalid_lifetime(self):
        with self.assertRaises(ValueError):
            self.identity.issue("alpha", "alice", 20, 20)

    def test_consent_still_required(self):
        token = self.identity.issue("alpha", "charlie", 10, 100)
        with self.assertRaises(PermissionError):
            authorized_read(self.lab, self.identity, token, "r", "view", 20)
        self.lab.grant("c", "alpha", "r", "alice", "charlie", "view", 90)
        self.assertEqual(authorized_read(self.lab, self.identity, token, "r", "view", 20), "private alpha")
        self.lab.revoke("d", "alpha", "r", "alice", "charlie", "view")
        with self.assertRaises(PermissionError):
            authorized_read(self.lab, self.identity, token, "r", "view", 20)

if __name__ == "__main__":
    unittest.main()
