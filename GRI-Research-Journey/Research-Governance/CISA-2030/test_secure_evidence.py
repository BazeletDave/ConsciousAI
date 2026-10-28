import hashlib
import tempfile
import unittest
from pathlib import Path
from evidence_ledger import EvidenceLedger
from secure_evidence import intake, export_backup, restore_backup

KEYS = {"collector": ("collector", b"a"*32), "reviewer": ("reviewer", b"b"*32), "auditor": ("auditor", b"c"*32)}
BKEY = b"k"*32
DATA = b"public controlled evidence"
def record():
    return {"record_id": "r1", "scenario_type": "real", "consent_or_authority": "authorized test",
            "source_sha256": hashlib.sha256(DATA).hexdigest(), "domain": "defend",
            "observation_type": "controlled_experiment", "observed_at": "2026-10-28T12:00:00Z",
            "outcome": True, "source_url": "https://example.org/primary"}

class SecureEvidenceTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        self.ledger = EvidenceLedger(self.root/"live.db", KEYS)
    def tearDown(self):
        self.ledger.close()
        self.tmp.cleanup()
    def test_intake_and_recovery(self):
        intake(self.ledger, "collector", record(), DATA)
        self.ledger.review("reviewer", "r1", "approve", "reviewed")
        manifest = export_backup(self.ledger, self.root/"backup.db", BKEY)
        state = restore_backup(self.root/"backup.db", self.root/"restored.db", BKEY, KEYS)
        self.assertEqual(state["head_sha256"], manifest["ledger_head"])
        self.assertEqual(state["events"], 2)
    def test_tampered_backup_rejected(self):
        intake(self.ledger, "collector", record(), DATA)
        backup = self.root/"backup.db"
        export_backup(self.ledger, backup, BKEY)
        backup.write_bytes(backup.read_bytes()+b"corruption")
        with self.assertRaises(ValueError): restore_backup(backup, self.root/"restored.db", BKEY, KEYS)
    def test_wrong_key_rejected(self):
        export_backup(self.ledger, self.root/"backup.db", BKEY)
        with self.assertRaises(ValueError): restore_backup(self.root/"backup.db", self.root/"restored.db", b"x"*32, KEYS)
    def test_no_overwrite(self):
        export_backup(self.ledger, self.root/"backup.db", BKEY)
        with self.assertRaises(FileExistsError): export_backup(self.ledger, self.root/"backup.db", BKEY)
    def test_invalid_intake_rejected(self):
        with self.assertRaises(ValueError): intake(self.ledger, "collector", {**record(), "scenario_type":"synthetic"}, DATA)
    def test_wrong_role_rejected(self):
        with self.assertRaises(PermissionError): intake(self.ledger, "reviewer", record(), DATA)

if __name__ == "__main__":
    unittest.main()
