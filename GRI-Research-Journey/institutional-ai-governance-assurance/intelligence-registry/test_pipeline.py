import unittest, tempfile, json
from pathlib import Path
from pipeline import intake,check_source,export,fingerprint

EXAMPLE={'title':'Example','source_url':'https://github.com/waymo-research/waymax','domain':'mobility','governance_risk':'Risk','safeguard':'Human review','opportunity':'Research'}
class PipelineTests(unittest.TestCase):
    def test_intake_unverified(self):
        v=intake(EXAMPLE);self.assertEqual(v['verification'],'UNVERIFIED');self.assertFalse(v['automated_action'])
    def test_reject_local(self):
        for url in ('http://github.com/x','https://127.0.0.1','https://github.com.evil.org/x','file:///etc/passwd','https://user:pass@github.com/x'):
            with self.subTest(url=url),self.assertRaises(ValueError):check_source(url)
    def test_missing_field(self):
        with self.assertRaises(ValueError):intake({**EXAMPLE,'safeguard':''})
    def test_dedup(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/'out.json';self.assertEqual(export([EXAMPLE,EXAMPLE],p),1);self.assertTrue(json.loads(p.read_text())['human_review_required'])
    def test_fingerprint_stable(self):self.assertEqual(fingerprint(EXAMPLE),fingerprint(EXAMPLE))
if __name__=='__main__':unittest.main()
