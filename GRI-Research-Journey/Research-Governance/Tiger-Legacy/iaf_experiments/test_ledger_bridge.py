"""Tests of IAF adapter against the original synthetic SQLite ledger."""
import copy
import json
import sqlite3
import tempfile
import unittest
from pathlib import Path
from ledger_bridge import record_trajectory,verify_export

T=json.loads((Path(__file__).resolve().parent/"trajectory.json").read_text())
KEY=b"gri-iaf-synthetic-research-key-not-for-production-2026"

class LedgerBridgeTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory()
        self.path=str(Path(self.tmp.name)/"research.sqlite")
    def tearDown(self):
        self.tmp.cleanup()
    def test_append_verify_checkpoint(self):
        report=record_trajectory(self.path,KEY,T)
        self.assertEqual(report["event_count"],5)
        self.assertEqual(report["checkpoint"]["count"],5)
        self.assertTrue(verify_export(self.path,KEY,report["checkpoint"]))
    def test_wrong_key_fails(self):
        report=record_trajectory(self.path,KEY,T)
        self.assertFalse(verify_export(self.path,b"x"*32,report["checkpoint"]))
    def test_tamper_fails(self):
        report=record_trajectory(self.path,KEY,T)
        with sqlite3.connect(self.path) as db:
            db.execute("DROP TRIGGER prevent_event_update")
            db.execute("UPDATE events SET payload=? WHERE seq=0",('{"changed":true}',))
        self.assertFalse(verify_export(self.path,KEY,report["checkpoint"]))
    def test_checkpoint_mismatch_fails(self):
        report=record_trajectory(self.path,KEY,T)
        forged=dict(report["checkpoint"]);forged["head"]="0"*64
        self.assertFalse(verify_export(self.path,KEY,forged))
    def test_reject_non_synthetic(self):
        bad=copy.deepcopy(T);bad["synthetic_only"]=False
        with self.assertRaises(ValueError):record_trajectory(self.path,KEY,bad)

if __name__=="__main__":
    unittest.main()
