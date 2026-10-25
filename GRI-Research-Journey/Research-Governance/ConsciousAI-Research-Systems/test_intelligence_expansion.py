import unittest
from international_mobility_collector import parse_feed,collect
from driver_evidence import assess
SRC={"id":"TEST","publisher":"Test","category":"mobility_industry","jurisdiction":"US","feed":"https://example.org/feed"}
class ExpansionTests(unittest.TestCase):
 def test_rss(self):
  x=parse_feed(b'<rss><channel><item><title>Mobility policy</title><link>https://example.org/article</link></item></channel></rss>',SRC)
  self.assertEqual(len(x),1);self.assertFalse(x[0]["publication_authorized"])
 def test_source_failure_visible(self):
  def fail(url):raise OSError("offline")
  x=collect(fetch=fail,sources=[SRC],now="fixed")
  self.assertEqual(x["sources"][0]["status"],"failed")
 def test_consent_required(self):
  x=assess({"record_id":"1","platform":"Uber","country":"US","observed_at":"2026","source_type":"interview","consent_status":"unknown"})
  self.assertFalse(x["accepted"])
 def test_claim_is_not_independent_verification(self):
  x=assess({"record_id":"1","platform":"Uber","country":"US","observed_at":"2026","source_type":"interview","consent_status":"explicit_research_consent","evidence_refs":[]})
  self.assertEqual(x["verification_status"],"firsthand_unverified")
if __name__=="__main__":unittest.main()
