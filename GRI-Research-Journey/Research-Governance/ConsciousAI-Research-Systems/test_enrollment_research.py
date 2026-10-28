import copy
import json
import unittest
from enrollment_research import ROOT, snapshot, validate, DocumentIndex
import test_server

class EnrollmentResearchTests(unittest.TestCase):
    def setUp(self):
        self.data = json.loads((ROOT / "enrollment_research.json").read_text())

    def test_attributed_report_excluded_from_fitted_corpus(self):
        index = DocumentIndex(validate(self.data)["records"])
        self.assertEqual(len(index.rows), 3)
        self.assertTrue(all(r["record_type"] == "institutional_reference" for r in index.rows))
        self.assertFalse(any("GRI-ENROLLMENT" in r["id"] for r in index.rows))

    def test_relevance_and_unknown_vocabulary(self):
        result = snapshot("identity confirmation overrides")
        self.assertEqual(result["retrieval"]["matches"][0]["id"], "FSA-APP-26-09")
        self.assertEqual(snapshot("xyzzzzq")["retrieval"]["matches"], [])
        for m in result["retrieval"]["matches"]:
            self.assertGreater(m["similarity"], 0)
            self.assertLessEqual(m["similarity"], 1)

    def test_corpus_digest_changes_and_is_stable(self):
        a = DocumentIndex(self.data["records"]).digest
        self.assertEqual(a, DocumentIndex(self.data["records"]).digest)
        self.data["records"][1]["summary"] += " Changed source summary."
        self.assertNotEqual(a, DocumentIndex(self.data["records"]).digest)

    def test_country_filter_does_not_invent_global_coverage(self):
        result = snapshot("identity", "BRA")
        self.assertEqual(result["records"], [])
        self.assertEqual(result["retrieval"]["matches"], [])
        self.assertEqual(result["coverage"]["countries"], ["USA"])

    def test_fail_closed_invalid_or_unreviewed_data(self):
        for change in ({"contains_personal_data": True}, {"training_eligible": True}, {"retrieval_eligible": True}, {"source_url": "javascript:alert(1)"}):
            d = copy.deepcopy(self.data); d["records"][0].update(change)
            with self.subTest(change=change), self.assertRaises(ValueError): validate(d)
        d=copy.deepcopy(self.data); d["records"].append(d["records"][0])
        with self.assertRaises(ValueError): validate(d)

    def test_query_limits(self):
        for args in (("a"*501, None), ("", "invalid")):
            with self.assertRaises(ValueError): snapshot(*args)

    def test_metrics_are_unmeasured_and_no_fraud_classification(self):
        d = snapshot()
        self.assertIsNone(d["retrieval"]["precision"])
        self.assertFalse(d["retrieval"]["fraud_classifier"])
        self.assertFalse(d["automated_actions"])

class EnrollmentHTTPTests(unittest.TestCase):
    setUpClass = classmethod(test_server.ResearchServiceTests.setUpClass.__func__)
    tearDownClass = classmethod(test_server.ResearchServiceTests.tearDownClass.__func__)
    fetch = test_server.ResearchServiceTests.fetch
    # Reuse only HTTP fixture helpers, not inherited unrelated test methods.
    def test_enrollment_endpoint_and_dashboard_assets(self):
        from urllib.request import urlopen
        from urllib.error import HTTPError
        d = self.fetch('/intelligence/enrollment-research?q=identity&country=USA')
        self.assertEqual(d['counts']['records'], 4)
        self.assertEqual(d['retrieval']['fitted_documents'], 3)
        with self.assertRaises(HTTPError) as error:
            self.fetch('/intelligence/enrollment-research?country=invalid')
        self.assertEqual(error.exception.code, 400)
        for path, expected in [('/dashboard', b'id="enrollment-search"'), ('/enrollment-research.js', b'textContent')]:
            with urlopen(f'http://127.0.0.1:{self.port}'+path) as response:
                self.assertIn(expected, response.read())
