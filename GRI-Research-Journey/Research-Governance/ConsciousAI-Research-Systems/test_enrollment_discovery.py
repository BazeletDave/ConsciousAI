import copy
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
from enrollment_discovery import collect, parse, canonical, fit_metadata, related, validate_state, snapshot, SafeRedirect

SOURCE={'id':'TEST-UK','country':'GBR','publisher':'UK Government','mode':'govuk_json','url':'https://www.gov.uk/api/search.json?q=student','allowed_host':'www.gov.uk','path_prefix':'/government/'}
NOW='2026-10-28T18:00:00+00:00'
def payload(title='Student loan identity fraud controls',link='/government/news/student-fraud'):
    return json.dumps({'results':[{'title':title,'link':link,'public_timestamp':'2026-10-28'}]}).encode()

class EnrollmentDiscoveryTests(unittest.TestCase):
    def collect(self,previous=None,data=None,now=NOW):
        return collect(previous,fetcher=lambda url:data or payload(),sources=[SOURCE],now=now)

    def test_live_adaptation_changes_vocabulary_and_digest(self):
        a=self.collect()
        b=self.collect(a,payload('University enrollment identity fraud bots'), '2026-10-29T18:00:00+00:00')
        self.assertEqual(a['model']['version'],1)
        self.assertEqual(b['model']['version'],2)
        self.assertIn('bots',b['model']['idf'])
        self.assertNotEqual(a['model']['corpus_digest'],b['model']['corpus_digest'])
        self.assertEqual(b['history'][-1]['changed_titles'],1)
        self.assertEqual(len(b['records']),1)
        self.assertEqual(b['records'][0]['first_seen_at'],NOW)

    def test_unchanged_source_does_not_claim_model_learning(self):
        a=self.collect();b=self.collect(a,now='2026-10-29T18:00:00+00:00')
        self.assertEqual(a['model'],b['model'])
        self.assertEqual(b['history'][-1]['new_records'],0)
        self.assertEqual(b['records'][0]['last_seen_at'],'2026-10-29T18:00:00+00:00')

    def test_duplicate_urls_collapsed_across_sources(self):
        a=collect(fetcher=lambda url:payload(),sources=[SOURCE,{**SOURCE,'id':'SECOND'}],now=NOW)
        self.assertEqual(len(a['records']),1)
        # Counts must describe unique additions, not duplicate publishers.
        self.assertEqual(a['model']['documents'],1)
        self.assertEqual(a['history'][-1]['new_records'],1)

    def test_source_failures_preserve_last_success_and_records(self):
        a=self.collect()
        def fail(url):raise OSError('network unavailable')
        b=collect(a,fetcher=fail,sources=[SOURCE],now='2026-10-29T18:00:00+00:00')
        self.assertEqual(a['records'],b['records'])
        self.assertEqual(a['model'],b['model'])
        self.assertEqual(b['sources'][0]['status'],'failed')
        self.assertEqual(b['last_success_at'],NOW)

    def test_bad_urls_and_private_destinations_are_rejected(self):
        for url in ['http://www.gov.uk/x','https://127.0.0.1/x','https://www.gov.uk.evil.test/x','https://u:p@www.gov.uk/x','https://www.gov.uk:8443/x']:
            with self.subTest(url=url),self.assertRaises(ValueError):canonical(url,'www.gov.uk')
        for link in ['https://evil.test/student-fraud','javascript:student-fraud','https://www.gov.uk/other/student-fraud']:
            self.assertEqual(parse(payload(link=link),SOURCE),[])

    def test_source_text_is_inert_and_metadata_only(self):
        rows=parse(payload('Student finance fraud <script>alert(1)</script> ignore instructions'),SOURCE)
        self.assertEqual(rows[0]['verification'],'unreviewed_publisher_metadata')
        self.assertNotIn('article_body',rows[0])
        self.assertTrue(rows[0]['human_review_required'])
        self.assertFalse(rows[0]['fraud_training_eligible'])

    def test_model_tampering_and_promotion_fail_closed(self):
        a=self.collect()
        for kind in ['vector','promotion','duplicate']:
            b=copy.deepcopy(a)
            if kind=='vector':b['model']['idf']['invented']=10
            elif kind=='promotion':b['records'][0]['verification']='verified'
            else:b['records'].append(b['records'][0])
            with self.subTest(kind=kind),self.assertRaises(ValueError):validate_state(b)

    def test_similarity_unknown_words_and_country_filter(self):
        a=self.collect()
        self.assertTrue(related(a,'identity fraud'))
        self.assertEqual(related(a,'xyzzzz'),[])
        self.assertEqual(related(a,'identity','USA'),[])
        self.assertLessEqual(related(a,'identity fraud')[0]['similarity'],1)

    def test_discovery_snapshot_has_no_vectors_or_false_metrics(self):
        a=self.collect()
        with tempfile.TemporaryDirectory() as directory:
            path=Path(directory)/'state.json';path.write_text(json.dumps(a))
            d=snapshot('identity',path=path)
        self.assertNotIn('vectors',d['model'])
        self.assertIsNone(d['model']['precision'])
        self.assertFalse(d['model']['predictive_model_trained'])

    def test_missing_snapshot_and_invalid_query(self):
        self.assertEqual(snapshot(path=Path('/does/not/exist'))['status'],'awaiting_first_collection')
        for q,c in [('a'*501,None),('', 'bad')]:
            with self.assertRaises(ValueError):snapshot(q,c)

    def test_irrelevant_and_malformed_source_documents(self):
        self.assertEqual(parse(payload('Transport road safety consultation'),SOURCE),[])
        with self.assertRaises(ValueError):parse(b'{"wrong":[]}',SOURCE)

    def test_retention_expiration_is_explicit(self):
        a=self.collect()
        b=collect(a,fetcher=lambda url:b'{"results":[]}',sources=[SOURCE],now='2028-10-29T18:00:00+00:00')
        self.assertEqual(b['records'],[])
        self.assertEqual(b['model']['documents'],0)
        self.assertGreater(b['model']['version'],a['model']['version'])

    def test_redirects_cannot_escape_allowlisted_host(self):
        from urllib.request import Request
        with self.assertRaises(ValueError):SafeRedirect().redirect_request(Request(SOURCE['url']),None,302,'',{},'https://evil.test/')

    def test_html_index_parser(self):
        source={**SOURCE,'mode':'html'}
        rows=parse(b'<a href="/government/news/identity">Student <b>loan</b> identity fraud</a><a href="https://evil.test/">Student loan fraud</a>',source)
        self.assertEqual(len(rows),1)
        self.assertEqual(rows[0]['title'],'Student loan identity fraud')
