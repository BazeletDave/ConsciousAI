import unittest
from unittest.mock import patch
from urllib.error import HTTPError
from urllib.request import Request
from international_mobility_collector import parse_feed,parse_official_page,collect,approved_url,public_fetch,NoRedirect
from driver_evidence import assess
SRC={"id":"TEST","publisher":"Test","category":"mobility_industry","jurisdiction":"US","feed":"https://example.org/feed"}
class ExpansionTests(unittest.TestCase):
 def test_source_url_restrictions(self):
  self.assertTrue(approved_url("https://example.org/feed",SRC))
  for url in ("http://example.org/feed","https://evil.example/feed","https://user:pass@example.org/feed","https://example.org:8443/feed"):
   with self.subTest(url=url):self.assertFalse(approved_url(url,SRC))
 def test_disallowed_source_never_invokes_fetch(self):
  x=collect(fetch=lambda _:self.fail("network request should be blocked"),sources=[{**SRC,"feed":"https://evil.example/feed","allowed_host":"example.org"}],now="fixed")
  self.assertEqual(x["sources"][0]["status"],"failed")
 def test_public_fetch_allows_public_feed_when_robots_permits(self):
  class Reply:
   def __init__(self,url,data):self.url=url;self.data=data
   def __enter__(self):return self
   def __exit__(self,*args):return False
   def read(self,n):return self.data[:n]
  class Opener:
   calls=[]
   def open(self,request,timeout):
    self.calls.append(request.full_url)
    if request.full_url.endswith("/robots.txt"):
     return Reply(request.full_url,b"User-agent: *\nAllow: /\n")
    return Reply(request.full_url,b"<rss><channel></channel></rss>")
  opener=Opener()
  with patch("international_mobility_collector.build_opener",return_value=opener):
   data=public_fetch(SRC["feed"],SRC)
  self.assertEqual(data,b"<rss><channel></channel></rss>")
  self.assertEqual(opener.calls,["https://example.org/robots.txt",SRC["feed"]])
 def test_public_fetch_respects_robots_disallow(self):
  class Reply:
   url="https://example.org/robots.txt"
   def __enter__(self):return self
   def __exit__(self,*args):return False
   def read(self,n):return b"User-agent: *\nDisallow: /feed\n"
  class Opener:
   calls=[]
   def open(self,request,timeout):
    self.calls.append(request.full_url)
    if len(self.calls)>1:raise AssertionError("blocked feed was requested")
    return Reply()
  opener=Opener()
  with patch("international_mobility_collector.build_opener",return_value=opener):
   with self.assertRaisesRegex(ValueError,"robots policy"):public_fetch(SRC["feed"],SRC)
  self.assertEqual(opener.calls,["https://example.org/robots.txt"])
 def test_public_fetch_stops_on_restricted_robots(self):
  class Opener:
   calls=[]
   def open(self,request,timeout):
    self.calls.append(request.full_url)
    raise HTTPError(request.full_url,403,"Forbidden",{},None)
  opener=Opener()
  with patch("international_mobility_collector.build_opener",return_value=opener):
   with self.assertRaises(HTTPError):public_fetch(SRC["feed"],SRC)
  self.assertEqual(opener.calls,["https://example.org/robots.txt"])
 def test_unapproved_redirect_is_refused(self):
  with self.assertRaisesRegex(ValueError,"redirect requires manual approval"):
   NoRedirect().redirect_request(Request(SRC["feed"]),None,302,"Found",{},"https://evil.example/private")
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
