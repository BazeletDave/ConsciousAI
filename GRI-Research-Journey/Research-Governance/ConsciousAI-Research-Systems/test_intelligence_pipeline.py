import unittest
from intelligence_pipeline import build
class IntelligencePipelineTests(unittest.TestCase):
 def test_review_queue(self):
  data={"records":[{"document_number":"2026-1","official_source_url":"https://www.federalregister.gov/documents/1","title":"Autonomous vehicle safety","abstract":"","publication_date":"2026-10-24"}]}
  r=build(data,now="fixed")
  self.assertEqual(r["matched_records"],1)
  self.assertEqual(r["queue"][0]["priority"],"review")
  self.assertFalse(r["queue"][0]["publication_authorized"])
 def test_dedup(self):
  x={"document_number":"1","official_source_url":"https://www.federalregister.gov/x","title":"AI automated systems"}
  self.assertEqual(build({"records":[x,x]})["matched_records"],1)
 def test_rejects_untrusted_url(self):
  self.assertEqual(build({"records":[{"document_number":"1","official_source_url":"https://example.com","title":"AI"}]})["matched_records"],0)
 def test_invalid(self):
  with self.assertRaises(ValueError):build({"records":"wrong"})
if __name__=="__main__":unittest.main()
