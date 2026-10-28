import hashlib
import sqlite3
import tempfile
import unittest
from pathlib import Path
from evidence_ledger import EvidenceLedger

KEYS = {"collector": ("collector", b"a"*32), "reviewer": ("reviewer", b"b"*32), "auditor": ("auditor", b"c"*32)}
ARTIFACT = b"authorized non-sensitive test evidence"
def record():
    return {"record_id": "r1", "scenario_type": "real", "consent_or_authority": "controlled lab", "source_sha256": hashlib.sha256(ARTIFACT).hexdigest()}

class LedgerTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.ledger = EvidenceLedger(Path(self.tmp.name)/"ledger.db", KEYS)
    def tearDown(self):
        self.ledger.close()
        self.tmp.cleanup()
    def test_chain_and_approval(self):
        self.ledger.collect("collector", record(), ARTIFACT)
        self.assertEqual(self.ledger.approved_records("auditor"), [])
        self.ledger.review("reviewer", "r1", "approve", "hash and authority independently checked")
        self.assertEqual(len(self.ledger.approved_records("auditor")), 1)
        self.assertEqual(self.ledger.verify()["events"], 2)
    def test_wrong_digest(self):
        with self.assertRaises(ValueError): self.ledger.collect("collector", record(), b"wrong")
    def test_synthetic_rejected(self):
        with self.assertRaises(ValueError): self.ledger.collect("collector", {**record(), "scenario_type":"synthetic"}, ARTIFACT)
    def test_role_denied(self):
        with self.assertRaises(PermissionError): self.ledger.collect("reviewer", record(), ARTIFACT)
    def test_duplicate_rejected(self):
        self.ledger.collect("collector", record(), ARTIFACT)
        with self.assertRaises(ValueError): self.ledger.collect("collector", record(), ARTIFACT)
    def test_unreviewed_not_published(self):
        self.ledger.collect("collector", record(), ARTIFACT)
        self.assertFalse(self.ledger.approved_records("auditor"))
    def test_append_only(self):
        self.ledger.collect("collector", record(), ARTIFACT)
        with self.assertRaises(sqlite3.DatabaseError): self.ledger.db.execute("DELETE FROM events")
    def test_reject_not_approved(self):
        self.ledger.collect("collector", record(), ARTIFACT)
        self.ledger.review("reviewer", "r1", "reject", "not independently corroborated")
        self.assertFalse(self.ledger.approved_records("auditor"))
    def test_invalid_signature_detected(self):
        self.ledger.collect("collector", record(), ARTIFACT)
        self.ledger.db.execute("DROP TRIGGER no_event_update")
        self.ledger.db.execute("UPDATE events SET signature='bad'")
        self.assertFalse(self.ledger.verify()["valid"])

if __name__ == "__main__":
    unittest.main()
