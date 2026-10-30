"""Controlled integration trial using only generic synthetic applications."""
import unittest
from synthetic_adapter import SyntheticAdapter
from synthetic_identity import SyntheticIdentity
from tiger_legacy import TigerLegacy

class ControlledIntegrationTrial(unittest.TestCase):
    def setUp(self):
        self.engine = TigerLegacy(b"synthetic-evidence-key-0000000000000000000000")
        self.identity = SyntheticIdentity(b"synthetic-identity-key-000000000000000000000")
        self.storefront = SyntheticAdapter(self.engine, self.identity, {"read"})
        self.archive = SyntheticAdapter(self.engine, self.identity, {"read"})
        self.engine.add_resource("event-1", "storefront", "record", "owner-a", "test-order")
        self.engine.add_resource("event-2", "archive", "record", "owner-b", "test-record")

    def token(self, tenant, subject, expiry=100):
        return self.identity.issue(tenant, subject, 10, expiry)

    def test_isolated_owner_access_in_two_profiles(self):
        self.assertEqual(self.storefront.read(self.token("storefront", "owner-a"), "record", "read", 20), "test-order")
        self.assertEqual(self.archive.read(self.token("archive", "owner-b"), "record", "read", 20), "test-record")

    def test_cross_tenant_resource_collision_fails_closed(self):
        with self.assertRaises(PermissionError):
            self.archive.read(self.token("storefront", "owner-b"), "record", "read", 20)

    def test_grant_and_revocation_lifecycle(self):
        token = self.token("storefront", "reviewer")
        with self.assertRaises(PermissionError):
            self.storefront.read(token, "record", "read", 20)
        self.engine.grant("event-3", "storefront", "record", "owner-a", "reviewer", "read", 50)
        self.assertEqual(self.storefront.read(token, "record", "read", 20), "test-order")
        self.engine.revoke("event-4", "storefront", "record", "owner-a", "reviewer", "read")
        with self.assertRaises(PermissionError):
            self.storefront.read(token, "record", "read", 20)
        self.assertTrue(self.engine.verify())

    def test_grant_expiry_fails_closed(self):
        self.engine.grant("event-3", "storefront", "record", "owner-a", "reviewer", "read", 30)
        with self.assertRaises(PermissionError):
            self.storefront.read(self.token("storefront", "reviewer"), "record", "read", 30)

    def test_tampered_token_fails_closed(self):
        token = self.token("storefront", "owner-a")
        tampered = ("A" if token[0] != "A" else "B") + token[1:]
        with self.assertRaises(PermissionError):
            self.storefront.read(tampered, "record", "read", 20)

    def test_cross_profile_principal_not_authorized(self):
        with self.assertRaises(PermissionError):
            self.storefront.read(self.token("storefront", "owner-b"), "record", "read", 20)

    def test_evidence_integrity_after_two_profiles(self):
        self.assertTrue(self.engine.verify())
        self.assertEqual(self.engine.summary()["tenant_count"], 2)
        self.assertEqual(self.engine.summary()["production_security"], "unmeasured")

if __name__ == "__main__":
    unittest.main()
