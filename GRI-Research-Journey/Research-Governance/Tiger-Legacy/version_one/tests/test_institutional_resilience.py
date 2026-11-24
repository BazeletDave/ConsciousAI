"""Deterministic synthetic comparisons; not production assurance."""
import tempfile
import unittest
from pathlib import Path
from tiger_legacy import TigerLegacy
from evidence_ledger import EvidenceLedger

KEY = b"synthetic-resilience-fixture-key-000"

class InstitutionalResilienceTests(unittest.TestCase):
    def test_paired_authority(self):
        engine = TigerLegacy(KEY)
        engine.add_resource("r", "a", "record", "owner", "synthetic")
        engine.grant("g", "a", "record", "owner", "reader", "analysis", 10)
        valid = engine.authorize("a", "record", "reader", "analysis", 1)
        expired = engine.authorize("a", "record", "reader", "analysis", 10)
        wrong_purpose = engine.authorize("a", "record", "reader", "other", 1)
        wrong_tenant = engine.authorize("b", "record", "reader", "analysis", 1)
        engine.revoke("v", "a", "record", "owner", "reader", "analysis")
        revoked = engine.authorize("a", "record", "reader", "analysis", 2)
        comparator = [True] * 5  # deliberately permissive cached approval
        governed = [valid, expired, revoked, wrong_purpose, wrong_tenant]
        self.assertEqual(comparator, [True, True, True, True, True])
        self.assertEqual(governed, [True, False, False, False, False])
        self.assertTrue(engine.verify())

    def test_ledger_integrity_and_recovery(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "ledger.sqlite"
            ledger = EvidenceLedger(path, KEY)
            ledger.append("one", {"value": 7})
            checkpoint = ledger.checkpoint()
            self.assertTrue(ledger.verify(checkpoint))
            backup = Path(tmp) / "backup.sqlite"
            ledger.backup(backup)
            with ledger._db() as db:
                db.execute("DROP TRIGGER prevent_event_update")
                db.execute("UPDATE events SET payload='{}' WHERE seq=0")
            self.assertFalse(ledger.verify())
            with ledger._db() as db:
                db.execute("DROP TRIGGER prevent_event_delete")
                db.execute("DELETE FROM events")
            self.assertTrue(ledger.verify())
            self.assertFalse(ledger.verify(checkpoint))
            restored = EvidenceLedger(backup, KEY)
            self.assertTrue(restored.verify(checkpoint))
            import json
            self.assertEqual(json.loads(restored.rows()[0][2]), {"value": 7})

    def test_authentic_false_information(self):
        with tempfile.TemporaryDirectory() as tmp:
            ledger = EvidenceLedger(Path(tmp) / "false.sqlite", KEY)
            ledger.append("one", {"value": 99})
            self.assertTrue(ledger.verify(ledger.checkpoint()))
            import json
            self.assertNotEqual(json.loads(ledger.rows()[0][2]), {"value": 7})

if __name__ == "__main__":
    unittest.main()
