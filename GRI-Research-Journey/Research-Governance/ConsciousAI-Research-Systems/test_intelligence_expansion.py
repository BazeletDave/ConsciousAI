import unittest
from international_mobility_collector import parse_feed,parse_official_page,collect
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

 def test_official_page_host_boundary(self):
  src=dict(SRC,mode="official_html",allowed_host="example.org",path_prefix="/news/")
  page=b'<a href="/news/policy-update">Official policy update announced</a><a href="https://evil.example/news/fake">Fake outside host article</a>'
  rows=parse_official_page(page,src)
  self.assertEqual(len(rows),1)
  self.assertEqual(rows[0]["verification_status"],"official_publisher_index_link_unreviewed")
  self.assertFalse(rows[0]["publication_authorized"])
 def test_empty_index_is_not_healthy(self):
  src=dict(SRC,mode="official_html",allowed_host="example.org",path_prefix="/news/")
  result=collect(fetch=lambda _:b'<html><body>Nothing here</body></html>',sources=[src],now="fixed")
  self.assertEqual(result["sources"][0]["status"],"empty_unvalidated")

if __name__=="__main__":unittest.main()
