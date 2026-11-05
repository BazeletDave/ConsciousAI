import json
import sqlite3
import tempfile
import unittest
from pathlib import Path
from storage_portability import export_evidence, telemetry

class PortabilityTests(unittest.TestCase):
    def test_export_restricted_and_cost(self):
        with tempfile.TemporaryDirectory() as d:
            db=Path(d)/"evidence.sqlite"
            out=Path(d)/"restricted.json"
            with sqlite3.connect(db) as conn:
                conn.execute("CREATE TABLE evidence(digest TEXT,payload TEXT,status TEXT,inserted_at TEXT)")
                record={"digest":"a"*64,"publication_approved":False,"training_eligible":False}
                conn.execute("INSERT INTO evidence VALUES (?,?,?,?)",("a"*64,json.dumps(record),"HUMAN_REVIEW_REQUIRED","2026-10-26"))
            result=export_evidence(db,out)
            self.assertEqual(result["record_count"],1)
            self.assertEqual(json.loads(out.read_text())["classification"],"RESTRICTED_STAGING_NOT_PUBLIC")
            self.assertGreaterEqual(telemetry(db,storage_cost_per_gb_month=.30)["estimated_storage_usd_month"],0)
            with self.assertRaises(ValueError):
                export_evidence(db,out)
    def test_fail_closed(self):
        with tempfile.TemporaryDirectory() as d:
            db=Path(d)/"evidence.sqlite"
            with sqlite3.connect(db) as conn:
                conn.execute("CREATE TABLE evidence(digest TEXT,payload TEXT,status TEXT,inserted_at TEXT)")
                conn.execute("INSERT INTO evidence VALUES (?,?,?,?)",("a"*64,'{"digest":"'+("a"*64)+'","publication_approved":true,"training_eligible":false}',"HUMAN_REVIEW_REQUIRED","now"))
            with self.assertRaises(ValueError):
                export_evidence(db,Path(d)/"out.json")

if __name__=="__main__":
    unittest.main()
