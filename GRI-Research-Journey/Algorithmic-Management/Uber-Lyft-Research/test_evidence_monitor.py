import unittest
from evidence_monitor import ingest
class MonitorTests(unittest.TestCase):
 def setUp(self):
  self.row={"source_url":"https://example.org/source","source_platform":"public_report","source_date":"2026-10-24","claim_text_paraphrase":"Reported policy change","verification_status":"CORPORATE_CLAIM"}
 def test_deduplicates(self):self.assertEqual(ingest([self.row,self.row])["unique_records"],1)
 def test_requires_review(self):
  r=ingest([self.row])["findings"][0]
  self.assertEqual(r["review_state"],"PENDING_HUMAN_REVIEW")
  self.assertFalse(r["publication_authorized"])
 def test_rejects_unknown_status(self):
  r=ingest([dict(self.row,verification_status="VERIFIED")])
  self.assertEqual(r["unique_records"],0)
 def test_rejects_bad_url(self):self.assertEqual(ingest([dict(self.row,source_url="private")])["unique_records"],0)
 def test_stable_id(self):self.assertEqual(ingest([self.row])["findings"][0]["evidence_id"],ingest([self.row])["findings"][0]["evidence_id"])
if __name__=="__main__":unittest.main()
