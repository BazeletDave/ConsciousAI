import copy
import json
import tempfile
import unittest
from pathlib import Path
from hashlib import sha256
from persistent_bridge import build_linked_manifest, verify_persisted_snapshot, _canonical_source

ROOT = Path(__file__).resolve().parent.parent / "ConsciousAI-Research-Systems"

class PersistentBridgeTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.snapshot = Path(self.tmp.name) / "snapshot.json"
        self.original = json.loads((ROOT / "assurance_evidence_snapshot.json").read_text())
        self.write(self.original)
    def tearDown(self): self.tmp.cleanup()
    def write(self, value): self.snapshot.write_text(json.dumps(value))
    def resign(self, value):
        body = {k:v for k,v in value.items() if k!="content_sha256"}
        value["content_sha256"] = sha256(_canonical_source(body)).hexdigest()
        self.write(value)
    def test_real_checked_in_snapshot(self):
        result = build_linked_manifest(ROOT/"ai_intelligence.json",self.snapshot)
        self.assertEqual(result["evaluation_count"],len(self.original["results"]))
        self.assertTrue(all(not r["operational_authorization"] for r in result["records"]))
        self.assertIsNone(result["external_audit_anchor"])
    def test_repeatable_manifest(self):
        self.assertEqual(build_linked_manifest(ROOT/"ai_intelligence.json",self.snapshot),build_linked_manifest(ROOT/"ai_intelligence.json",self.snapshot))
    def test_tampered_digest_rejected(self):
        item=copy.deepcopy(self.original);item["results"][0]["decision"]="allow"
        self.write(item)
        with self.assertRaises(ValueError):verify_persisted_snapshot(self.snapshot)
    def test_duplicate_result_rejected_even_with_recomputed_digest(self):
        item=copy.deepcopy(self.original);item["results"][1]["record_id"]=item["results"][0]["record_id"]
        self.resign(item)
        with self.assertRaises(ValueError):verify_persisted_snapshot(self.snapshot)
    def test_mismatched_record_ids_rejected(self):
        item=copy.deepcopy(self.original);item["results"][0]["record_id"]="not-in-watchlist"
        self.resign(item)
        with self.assertRaises(ValueError):build_linked_manifest(ROOT/"ai_intelligence.json",self.snapshot)
    def test_review_flag_fail_closed(self):
        item=copy.deepcopy(self.original);item["results"][0]["review_required"]=False
        item["human_review_count"]-=1
        self.resign(item)
        with self.assertRaises(ValueError):build_linked_manifest(ROOT/"ai_intelligence.json",self.snapshot)
    def test_bad_count_rejected(self):
        item=copy.deepcopy(self.original);item["evaluation_count"]+=1
        self.resign(item)
        with self.assertRaises(ValueError):verify_persisted_snapshot(self.snapshot)
if __name__=="__main__":unittest.main()
