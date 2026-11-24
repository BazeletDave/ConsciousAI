import unittest
from official_incident_discovery import parse_candidates

class OfficialDiscoveryTests(unittest.TestCase):
    def test_candidates_are_unreviewed_and_deduplicated(self):
        item = b"<item><title>Advisory</title><link>https://www.cisa.gov/example</link></item>"
        bad = b"<item><title>Other</title><link>https://example.org/a</link></item>"
        records = parse_candidates(b"<rss><channel>"+item+item+bad+b"</channel></rss>")
        self.assertEqual(len(records), 1)
        self.assertEqual(records[0]["classification"], "unreviewed_advisory_candidate")
    def test_rejects_unsupported_xml(self):
        for raw in (b"<html/>", b"<!DOCTYPE rss><rss/>"):
            with self.assertRaises(ValueError):
                parse_candidates(raw)
