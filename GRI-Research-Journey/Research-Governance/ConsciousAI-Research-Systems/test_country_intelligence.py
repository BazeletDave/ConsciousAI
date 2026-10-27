"""Offline country collection, provenance, review, classification and HTTP tests."""
from copy import deepcopy
import json
import unittest
from unittest.mock import patch
from country_intelligence import collect, country_mentions, parse, permitted, snapshot, publication_time, TrustedRedirect
from country_topics import TopicModel, EXAMPLES, HOLDOUT

SOURCE = {"id": "TEST", "publisher": "Synthetic publisher", "url": "https://example.org/feed", "host": "example.org", "mode": "rss", "country": None}
COUNTRIES = [{"code": "BRA", "name": "Brazil", "aliases": ["brazil", "brasil"], "pilot": True},
             {"code": "ARG", "name": "Argentina", "aliases": ["argentina"], "pilot": True}]
NOW = "2026-10-27T20:00:00+00:00"
LATER = "2026-10-27T23:00:00+00:00"


def rss(title="Brazil trade tariffs investment", link="https://example.org/item"):
    return f'<rss><channel><item><title>{title}</title><link>{link}</link><pubDate>Tue, 27 Oct 2026 12:00:00 GMT</pubDate></item></channel></rss>'.encode()


class CountryIntelligenceTests(unittest.TestCase):
    def run_collection(self, raw=None, previous=None, now=NOW):
        return collect(previous, fetcher=lambda source: raw or rss(), sources=[SOURCE], countries=COUNTRIES, now=now)

    def test_real_ml_has_explicit_instructional_provenance(self):
        model = TopicModel()
        result = model.predict("Artificial intelligence neural networks")
        self.assertEqual(result["label"], "artificial_intelligence")
        self.assertTrue(result["human_review_required"])
        self.assertEqual(model.predict("zzzx qqqv rrrz")["label"], "needs_review")
        metrics = model.evaluation()
        self.assertFalse(metrics["production_validated"])
        self.assertFalse(metrics["independently_labeled"])
        self.assertEqual(metrics["training_examples"], 30)
        self.assertEqual(metrics["evaluation_examples"], 15)
        self.assertTrue(0 <= metrics["macro_f1"] <= 1)
        self.assertEqual(len(metrics["training_sha256"]), 64)
        self.assertFalse(set(sum(EXAMPLES.values(), [])) & set(sum(HOLDOUT.values(), [])))

    def test_multilingual_country_mentions_and_word_boundaries(self):
        self.assertEqual(country_mentions("Brasil e Argentina", COUNTRIES), ["BRA", "ARG"])
        self.assertEqual(country_mentions("Brazilwood", COUNTRIES), [])

    def test_collection_candidate_fields_and_provenance(self):
        data = self.run_collection()
        row = data["records"][0]
        self.assertEqual(row["country_codes"], ["BRA"])
        self.assertEqual(row["first_seen_at"], NOW)
        self.assertIsNone(row["political_direction"])
        self.assertIsNone(row["causal_impact"])
        self.assertFalse(row["publication_authorized"])
        self.assertEqual(row["review_status"], "unreviewed")
        self.assertEqual(data["changes"][0]["kind"], "newly_discovered")
        self.assertEqual(len(data["sources"][0]["response_sha256"]), 64)

    def test_same_record_then_revision(self):
        first = self.run_collection()
        second = self.run_collection(previous=first, now=LATER)
        self.assertEqual(second["changes"], [])
        self.assertEqual(second["records"][0]["first_seen_at"], NOW)
        self.assertEqual(second["records"][0]["last_seen_at"], LATER)
        third = self.run_collection(raw=rss("Brazil election coalition parliament"), previous=second, now=LATER)
        row = third["records"][0]
        self.assertEqual(row["change_count"], 1)
        self.assertEqual(third["changes"][0]["kind"], "metadata_changed")
        self.assertEqual(row["previous_content_sha256"], first["records"][0]["content_sha256"])

    def test_source_failure_retains_old_evidence_and_timestamp(self):
        first = self.run_collection()
        def fail(source):
            raise OSError("synthetic failure")
        second = collect(first, fetcher=fail, sources=[SOURCE], countries=COUNTRIES, now=LATER)
        self.assertEqual(second["records"], first["records"])
        self.assertEqual(second["sources"][0]["last_success_at"], NOW)
        self.assertEqual(second["sources"][0]["attempted_at"], LATER)
        self.assertEqual(second["collection_status"], "all_sources_failed")
        self.assertEqual(second["changes"], [])

    def test_malformed_response_is_failed_not_empty_success(self):
        for raw in [b'<html><body>Challenge</body></html>', b'not xml']:
            with self.subTest(raw=raw):
                data = self.run_collection(raw)
                self.assertEqual(data["sources"][0]["status"], "failed")

    def test_rdf_and_atom_parsing(self):
        rdf = b'<rdf:RDF xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#" xmlns="http://purl.org/rss/1.0/" xmlns:dc="http://purl.org/dc/elements/1.1/"><item><title>Brasil trade</title><link>https://example.org/item</link><dc:date>2026-10-27T10:00:00Z</dc:date></item></rdf:RDF>'
        atom = b'<feed xmlns="http://www.w3.org/2005/Atom"><entry><title>Brazil investment</title><link rel="self" href="https://example.org/api"/><link rel="alternate" href="https://example.org/item"/><published>2026-10-27T10:00:00Z</published></entry></feed>'
        self.assertEqual(len(parse(rdf, SOURCE)), 1)
        self.assertEqual(parse(atom, SOURCE)[0]["source_url"], "https://example.org/item")
        self.assertIsNotNone(parse(rdf, SOURCE)[0]["published_at"])

    def test_unsafe_links_and_redirects_rejected(self):
        for url in ['http://example.org/a', 'https://evil.org/a', 'https://example.org.evil.org/a', 'https://x@example.org/a', 'https://example.org:8000/a']:
            with self.subTest(url=url):
                self.assertFalse(permitted(url, 'example.org'))
                self.assertEqual(parse(rss(link=url), SOURCE), [])
        from urllib.request import Request
        with self.assertRaises(ValueError):
            TrustedRedirect().redirect_request(Request(SOURCE['url']), None, 302, 'redirect', {}, 'https://evil.org/')

    def test_proposal_cannot_become_enacted_law(self):
        source = dict(SOURCE, mode="camara", country="BRA")
        raw = json.dumps({"dados": [{"siglaTipo": "PL", "numero": 1, "ano": 2026, "ementa": "Inteligência artificial", "uri": "https://example.org/proposal"}]}).encode()
        rows = parse(raw, source)
        self.assertEqual(rows[0]["legal_status"], "proposal_record_not_evidence_of_enactment")
        self.assertIsNone(rows[0]["published_at"])

    def test_catalog_and_country_filter(self):
        from country_intelligence import load_catalog
        catalog = load_catalog()
        self.assertEqual(sum(c["pilot"] for c in catalog["countries"]), 12)
        self.assertEqual(len({c["code"] for c in catalog["countries"]}), len(catalog["countries"]))
        with patch('country_intelligence.read_feed', return_value=self.run_collection()):
            data = snapshot('ARG')
            self.assertEqual(data['records'], [])
            self.assertIn('limited', data['coverage'])
            with self.assertRaises(LookupError): snapshot('ZZZ')
            with self.assertRaises(ValueError): snapshot('BRA', 'invented')

    def test_naive_or_missing_publication_dates_remain_unknown(self):
        self.assertIsNone(publication_time(None))
        self.assertIsNone(publication_time('2026-10-27'))
        self.assertIsNone(publication_time('invalid'))
