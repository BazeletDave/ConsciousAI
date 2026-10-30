"""Synthetic adversarial recovery tests: rollback, unauthorized proof, damaged backup."""
import os
import sqlite3
import tempfile
import unittest
from evidence_ledger import EvidenceLedger
from synthetic_checkpoint import SyntheticCheckpointAuthority
from recovery import verified_recovery

KEY = b"synthetic-ledger-key-32-bytes-minimum"
CUSTODY = b"synthetic-independent-custody-key-32-bytes"

class RecoveryTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.path = os.path.join(self.tmp.name, "live.sqlite")
        self.backup = os.path.join(self.tmp.name, "backup.sqlite")
        self.restored = os.path.join(self.tmp.name, "restored.sqlite")
        self.ledger = EvidenceLedger(self.path, KEY)
        self.ledger.append("event1", {"synthetic": "record"})
        self.authority = SyntheticCheckpointAuthority({"custody1": CUSTODY}, "custody1")
        self.proof = self.authority.attest(self.ledger.checkpoint())
        self.ledger.backup(self.backup)

    def test_valid_restore(self):
        checkpoint = verified_recovery(self.backup, self.restored, KEY, self.proof, self.authority)
        self.assertEqual(checkpoint["count"], 1)

    def test_wrong_ledger_key_denied(self):
        with self.assertRaises(PermissionError):
            verified_recovery(self.backup, self.restored, b"other-ledger-key-of-32-bytes-minimum", self.proof, self.authority)

    def test_wrong_custodian_denied(self):
        other = SyntheticCheckpointAuthority({"custody1": b"different-custodian-secret-32-bytes"}, "custody1")
        with self.assertRaises(PermissionError):
            verified_recovery(self.backup, self.restored, KEY, self.proof, other)

    def test_backup_rollback_denied(self):
        self.ledger.append("event2", {"synthetic": "new"})
        current_proof = self.authority.attest(self.ledger.checkpoint())
        with self.assertRaises(PermissionError):
            verified_recovery(self.backup, self.restored, KEY, current_proof, self.authority)

    def test_backup_extension_denied(self):
        EvidenceLedger(self.backup, KEY).append("extra", {"synthetic": "unapproved"})
        with self.assertRaises(PermissionError):
            verified_recovery(self.backup, self.restored, KEY, self.proof, self.authority)

    def test_corrupt_backup_denied(self):
        with open(self.backup, "wb") as handle:
            handle.write(b"corrupt")
        with self.assertRaises(sqlite3.DatabaseError):
            verified_recovery(self.backup, self.restored, KEY, self.proof, self.authority)

    def test_destination_overwrite_denied(self):
        with open(self.restored, "w") as handle:
            handle.write("do not overwrite")
        with self.assertRaises(ValueError):
            verified_recovery(self.backup, self.restored, KEY, self.proof, self.authority)
        with open(self.restored) as handle:
            self.assertEqual(handle.read(), "do not overwrite")

    def test_same_path_denied(self):
        with self.assertRaises(ValueError):
            verified_recovery(self.backup, self.backup, KEY, self.proof, self.authority)

if __name__ == "__main__":
    unittest.main()
