"""Regression tests for conservative GRI record classifications."""
import unittest
from analytical_integrity import assess_record, audit_inventory

class AnalyticalIntegrityTests(unittest.TestCase):
    def test_verified_label_without_provenance_is_blocked(self):
        r = assess_record({"id":"a", "verification_status":"independently_verified", "source":"https://example.org"}, "cases")
        self.assertEqual(r["classification"], "verified_claim_blocked_pending_evidence")
        self.assertFalse(r["certified"])
        self.assertIsNone(r["academic_framework"])
    def test_official_listing_does_not_verify_event_claim(self):
        r = assess_record({"id":"b","verification_status":"official_event_listing_verified",
                           "primary_source_url":"https://example.org","event_date":"2026-10-16"}, "events")
        self.assertEqual(r["classification"], "verified_claim_blocked_pending_evidence")
    def test_complete_record_can_be_eligible_but_not_certified(self):
        r = assess_record({"id":"c","verification_status":"independently_verified",
            "source":"https://example.org/report","publication_date":"2026-10-01",
            "retrieved_at":"2026-10-30","document_locator":"page 2",
            "independent_verification":True,
            "academic_framework":{"id":"nelson","attribution":"Roy C. Nelson"},
            "claim_type":"reported_claim","limitations":"Small sample",
            "review_status":"approved","reviewer_id":"reviewer-1","reviewed_at":"2026-10-30"}, "cases")
        self.assertEqual(r["classification"], "eligible_for_verified_claim")
        self.assertFalse(r["certified"])
    def test_unreviewed_hypothesis_is_not_empirical_finding(self):
        r = assess_record({"id":"d","claim_type":"hypothesis","verification_status":"unreviewed"}, "cases")
        self.assertEqual(r["classification"], "not_verified")
        self.assertEqual(r["claim_type"], "hypothesis")
    def test_inventory_covers_all_families(self):
        result = audit_inventory([{"id":"1"}],[{"id":"2"}],[{"id":"3"}])
        self.assertEqual(result["total_records"],3)
        self.assertEqual(len(result["records"]),3)
        self.assertTrue(result["certification"].startswith("withheld"))

if __name__ == "__main__":
    unittest.main()
