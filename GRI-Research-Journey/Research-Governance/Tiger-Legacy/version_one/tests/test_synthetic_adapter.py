"""Multiple synthetic application profiles; no customer data or live integration."""
import unittest
from synthetic_adapter import SyntheticAdapter
from synthetic_identity import SyntheticIdentity
from tiger_legacy import TigerLegacy

class AdapterTests(unittest.TestCase):
    def setUp(self):
        self.identity = SyntheticIdentity(b"synthetic-identity-test-key-of-32-plus-bytes")
        self.lab = TigerLegacy(b"synthetic-ledger-test-key-of-32-plus-bytes")
        self.lab.add_resource("one", "commerce", "invoice", "owner1", "synthetic commerce")
        self.lab.add_resource("two", "research", "invoice", "owner2", "synthetic research")
        self.commerce = SyntheticAdapter(self.lab, self.identity, {"view"})
        self.research = SyntheticAdapter(self.lab, self.identity, {"view", "audit"})

    def token(self, tenant, principal):
        return self.identity.issue(tenant, principal, 10, 100)

    def test_generic_commerce_profile(self):
        self.assertEqual(self.commerce.read(self.token("commerce", "owner1"), "invoice", "view", 20), "synthetic commerce")

    def test_generic_research_profile(self):
        self.assertEqual(self.research.read(self.token("research", "owner2"), "invoice", "view", 20), "synthetic research")

    def test_tenant_mismatch_denied(self):
        with self.assertRaises(PermissionError):
            self.commerce.read(self.token("commerce", "owner2"), "invoice", "view", 20)

    def test_disabled_purpose_denied(self):
        with self.assertRaises(PermissionError):
            self.commerce.read(self.token("commerce", "owner1"), "invoice", "audit", 20)

    def test_expired_identity_denied(self):
        with self.assertRaises(PermissionError):
            self.commerce.read(self.token("commerce", "owner1"), "invoice", "view", 100)

    def test_unauthenticated_denied(self):
        with self.assertRaises(PermissionError):
            self.commerce.read("invalid", "invoice", "view", 20)

    def test_missing_resource_denied(self):
        with self.assertRaises(PermissionError):
            self.commerce.read(self.token("commerce", "owner1"), "missing", "view", 20)

    def test_empty_profile_rejected(self):
        with self.assertRaises(ValueError):
            SyntheticAdapter(self.lab, self.identity, set())

if __name__ == "__main__":
    unittest.main()
