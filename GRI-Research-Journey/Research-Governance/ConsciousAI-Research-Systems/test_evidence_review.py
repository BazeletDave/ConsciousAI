import unittest
from evidence_review import fingerprint,assess_review
class EvidenceReviewTests(unittest.TestCase):
 def setUp(self):
  self.record={"id":"x","source_id":"official","source_url":"https://example.org/a","title":"Policy","verification_status":"unreviewed"}
 def test_digest_changes_when_source_changes(self):
  a=fingerprint(self.record);b=dict(self.record,source_url="https://example.org/b")
  self.assertNotEqual(a,fingerprint(b))
 def test_no_self_certification(self):
  d=fingerprint(self.record)
  review={"record_digest":d,"reviewer_id":"one","reviewed_at":"2026-10-24","evidence_url":"https://example.org/a","decision":"source_and_claim_corrobated"}
  result=assess_review(self.record,[review,dict(review)])
  self.assertFalse(result["independent_review_threshold_met"])
  self.assertFalse(result["publication_authorized"])
 def test_two_reviewers_still_require_institutional_validation(self):
  d=fingerprint(self.record)
  reviews=[{"record_digest":d,"reviewer_id":who,"reviewed_at":"2026-10-24","evidence_url":"https://example.org/a","decision":"source_and_claim_corrobated"} for who in ("one","two")]
  result=assess_review(self.record,reviews)
  self.assertTrue(result["independent_review_threshold_met"])
  self.assertFalse(result["publication_authorized"])
if __name__=="__main__":unittest.main()
