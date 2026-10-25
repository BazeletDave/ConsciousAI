import tempfile
import unittest
from datetime import datetime,timezone,timedelta
from evidence_store import EvidenceStore
from observability import assess_collector
from release_gate import assess_release,REQUIRED
class PhaseFourTests(unittest.TestCase):
    def record(self):
        return {"source_id":"synthetic","source_url":"https://example.org/case",
                "claim":"synthetic","captured_at":"2026-10-25T12:00:00Z","jurisdiction":"US"}
    def test_persistent_deduplicated(self):
        with tempfile.TemporaryDirectory() as folder:
            path=folder+"/evidence.db"
            store=EvidenceStore(path)
            digest=store.append(self.record())
            store.append(self.record())
            self.assertEqual(store.count(),1)
            store.close()
            store=EvidenceStore(path)
            self.assertEqual(store.get(digest)["claim"],"synthetic")
            store.close()
    def test_tamper_detected(self):
        with tempfile.TemporaryDirectory() as folder:
            store=EvidenceStore(folder+"/evidence.db")
            digest=store.append(self.record())
            with store.db:
                store.db.execute("UPDATE evidence SET payload=? WHERE digest=?",('{"claim":"tampered"}',digest))
            with self.assertRaises((ValueError,KeyError)):
                store.get(digest)
            store.close()
    def test_freshness(self):
        now=datetime(2026,10,25,16,tzinfo=timezone.utc)
        run={"status":"success","finished_at":"2026-10-25T15:00:00Z","records_processed":2}
        self.assertEqual(assess_collector(run,now=now)["status"],"HEALTHY")
        self.assertEqual(assess_collector(run,now=now+timedelta(days=1))["status"],"ALERT")
    def test_fail_closed_release(self):
        self.assertFalse(assess_release({"ci_passed":True})["deployment_authorized"])
        full=assess_release({key:True for key in REQUIRED})
        self.assertTrue(full["checklist_complete"])
        self.assertFalse(full["deployment_authorized"])
if __name__=="__main__":
    unittest.main()
