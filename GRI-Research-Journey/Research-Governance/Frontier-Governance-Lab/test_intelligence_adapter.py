import json
import tempfile
import unittest
from pathlib import Path
from governance import Metrics, Policy
from intelligence_adapter import load_watchlist, evaluate_intake
from evidence import digest

class AdapterTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.path = Path(self.tmp.name) / "watchlist.json"
        self.path.write_text(json.dumps({"schema_version":"1.0","records":[{"id":"example","summary":"unverified scenario","verification_status":"pending","sources":[{"url":"https://example.org/source"}]}]}))
    def tearDown(self):
        self.tmp.cleanup()
    def test_read_only_intake(self):
        rows = load_watchlist(self.path)
        self.assertEqual(rows[0].record_id, "example")
        self.assertEqual(rows[0].source_urls, ("https://example.org/source",))
    def test_no_operational_allow_even_with_approval(self):
        record = load_watchlist(self.path)[0]
        result = evaluate_intake(record, metrics=Metrics(.01,.01,.01,1), reviewer_approved=True)
        self.assertEqual(result["policy_decision"]["decision"], "DENY")
        self.assertFalse(result["operational_authorization"])
        self.assertTrue(result["requires_human_review"])
        body = {k:v for k,v in result.items() if k!="assessment_sha256"}
        self.assertEqual(digest(body), result["assessment_sha256"])
    def test_duplicate_ids_fail_closed(self):
        data = json.loads(self.path.read_text())
        data["records"].append(data["records"][0])
        self.path.write_text(json.dumps(data))
        with self.assertRaises(ValueError): load_watchlist(self.path)
    def test_invalid_schema_fails(self):
        self.path.write_text('{"records":[]}')
        with self.assertRaises(ValueError): load_watchlist(self.path)
    def test_metrics_required(self):
        with self.assertRaises(TypeError): evaluate_intake(load_watchlist(self.path)[0], metrics=None)
    def test_reject_forged_approval_type(self):
        with self.assertRaises(TypeError): evaluate_intake(load_watchlist(self.path)[0], metrics=Metrics(.1,.01,.01,2), reviewer_approved="yes")
    def test_snapshot_mutation_changes_digest(self):
        before = load_watchlist(self.path)[0].snapshot_digest
        self.path.write_text(self.path.read_text()+" ")
        self.assertNotEqual(before,load_watchlist(self.path)[0].snapshot_digest)
if __name__ == "__main__":
    unittest.main()
