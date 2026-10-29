import json
import sqlite3
import tempfile
import threading
import unittest
from pathlib import Path
from evidence_ledger import EvidenceLedger

KEY=b"synthetic-test-key-at-least-thirty-two-bytes"

class LedgerAdversarialTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory()
        self.path=Path(self.tmp.name)/"ledger.sqlite"
        self.ledger=EvidenceLedger(self.path, KEY)
    def tearDown(self):
        self.tmp.cleanup()
    def test_empty_genesis(self):
        self.assertTrue(self.ledger.verify())
        self.assertEqual(self.ledger.checkpoint()["count"],0)
    def test_durable_reopen(self):
        self.ledger.append("e1",{"tenant":"synthetic-alpha"})
        self.assertTrue(EvidenceLedger(self.path,KEY).verify(self.ledger.checkpoint()))
    def test_replay_event_rejected(self):
        self.ledger.append("e1",{"x":1})
        with self.assertRaises(sqlite3.IntegrityError):
            self.ledger.append("e1",{"x":2})
        self.assertTrue(self.ledger.verify())
    def test_update_delete_fail_closed(self):
        self.ledger.append("e1",{"x":1})
        with self.ledger._db() as db:
            with self.assertRaises(sqlite3.IntegrityError):
                db.execute("UPDATE events SET payload='{}' WHERE seq=0")
            with self.assertRaises(sqlite3.IntegrityError):
                db.execute("DELETE FROM events WHERE seq=0")
    def test_truncation_detected_by_external_checkpoint(self):
        self.ledger.append("e1",{"x":1})
        external=self.ledger.checkpoint()
        with self.ledger._db() as db:
            db.execute("DROP TRIGGER prevent_event_delete")
            db.execute("DELETE FROM events")
        self.assertTrue(self.ledger.verify())
        self.assertFalse(self.ledger.verify(external))
    def test_wrong_key_fails(self):
        self.ledger.append("e1",{"x":1})
        self.assertFalse(EvidenceLedger(self.path,b"another-test-key-at-least-32-bytes").verify())
    def test_backup_restore(self):
        self.ledger.append("e1",{"x":1})
        external=self.ledger.checkpoint()
        backup=Path(self.tmp.name)/"backup.sqlite"
        self.ledger.backup(backup)
        self.assertTrue(EvidenceLedger(backup,KEY).verify(external))
    def test_mutated_payload_detected(self):
        self.ledger.append("e1",{"x":1})
        with self.ledger._db() as db:
            db.execute("DROP TRIGGER prevent_event_update")
            db.execute("UPDATE events SET payload='{\"x\":99}' WHERE seq=0")
        self.assertFalse(self.ledger.verify())
    def test_concurrent_unique_sequence(self):
        errors=[]
        def writer(i):
            try:
                EvidenceLedger(self.path,KEY).append(f"e{i}",{"i":i})
            except Exception as e:
                errors.append(str(e))
        threads=[threading.Thread(target=writer,args=(i,)) for i in range(12)]
        for t in threads:t.start()
        for t in threads:t.join()
        self.assertFalse(errors,errors)
        self.assertEqual(self.ledger.checkpoint()["count"],12)
        self.assertTrue(self.ledger.verify())
    def test_invalid_event_and_backup_target(self):
        with self.assertRaises(ValueError):
            self.ledger.append("",{"x":1})
        with self.assertRaises(ValueError):
            self.ledger.backup(self.path)
    def test_checkpoint_mismatch(self):
        self.ledger.append("e1",{"x":1})
        self.assertFalse(self.ledger.verify({"count":1,"head":"0"*64}))
    def test_append_after_duplicate_rolls_back(self):
        self.ledger.append("e1",{"x":1})
        with self.assertRaises(sqlite3.IntegrityError):
            self.ledger.append("e1",{"x":2})
        self.ledger.append("e2",{"x":3})
        self.assertEqual(self.ledger.checkpoint()["count"],2)
