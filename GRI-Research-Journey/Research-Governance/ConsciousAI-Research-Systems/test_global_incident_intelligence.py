"""Regression tests for the existing GRI international incident intelligence extension."""
import unittest
from datetime import date
from global_incident_intelligence import snapshot, validate, assurance_snapshot

class InternationalIntelligenceTests(unittest.TestCase):
    def sample(self):
        return {
            "id": "EXAMPLE-1", "title": "Synthetic incident",
            "event_date": "2026-11-18", "jurisdiction": "Singapore",
            "organization": "Synthetic Organization", "summary": "Test data only",
            "evidence_status": "reported", "resolution_status": "investigating",
            "sources": [{"name": "Official", "url": "https://www.csa.gov.sg/"}],
            "relationships": [{"relation": "reported_by", "source_url": "https://www.csa.gov.sg/"}],
        }
    def test_coverage_does_not_imply_active_monitoring(self):
        result = assurance_snapshot([], date(2026, 11, 18))
        self.assertEqual(result["country_coverage"]["Singapore"]["curated_records_in_window"], 0)
        self.assertFalse(result["country_coverage"]["Singapore"]["verified_source_polling"])
        self.assertEqual(result["country_coverage"]["Brazil"]["coverage_status"], "source_discovery_only")

    def test_evidence_review_identifies_unverified_remediation(self):
        result = assurance_snapshot([self.sample()], date(2026, 11, 18))
        gaps = result["evidence_review_queue"][0]["gaps"]
        self.assertIn("remediation_not_independently_verified", gaps)

    def test_valid_synthetic_record(self):
        self.assertEqual(validate(self.sample()), [])
    def test_invalid_source_rejected(self):
        r = self.sample()
        r["sources"][0]["url"] = "javascript:alert(1)"
        self.assertIn("invalid_source", validate(r))
    def test_unsupported_relationship_rejected(self):
        r = self.sample()
        r["relationships"][0]["relation"] = "caused_by"
        self.assertIn("unsupported_relationship", validate(r))
    def test_rolling_window(self):
        r = self.sample()
        self.assertEqual(len(snapshot([r], date(2026, 11, 18))["records"]), 1)
        self.assertEqual(len(snapshot([r], date(2027, 1, 18))["records"]), 0)
    def test_invalid_records_are_quarantined(self):
        r = self.sample()
        r["event_date"] = "not-a-date"
        s = snapshot([r], date(2026, 11, 18))
        self.assertEqual(len(s["records"]), 0)
        self.assertEqual(len(s["rejected"]), 1)

if __name__ == "__main__":
    unittest.main()
