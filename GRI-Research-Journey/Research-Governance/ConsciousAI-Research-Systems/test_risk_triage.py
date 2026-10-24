"""Tests for the GRI v1.3 evidence triage baseline."""
import unittest
from risk_triage import triage


class TriageTests(unittest.TestCase):
    def test_missing_evidence_is_high_priority(self):
        result = triage({"id": "example"})
        self.assertEqual(result["review_priority_score"], 100)
        self.assertEqual(result["review_priority"], "high")
        self.assertTrue(result["requires_human_review"])
        self.assertFalse(result["model_trained"])

    def test_complete_record_still_requires_review(self):
        result = triage({"id": "complete", "primary_source_url": "https://example.org/record",
                         "verification_status": "independently_verified",
                         "observed_at": "2026-10-24T12:00:00Z",
                         "review_owner": "analyst", "jurisdiction": "US"})
        self.assertEqual(result["review_priority_score"], 0)
        self.assertEqual(result["review_priority"], "low")
        self.assertTrue(result["requires_human_review"])

    def test_partial_record_has_explainable_reasons(self):
        result = triage({"verification_status": "unreviewed",
                         "primary_source_url": "https://example.org"})
        self.assertEqual(result["review_priority_score"], 65)
        self.assertNotIn("missing_primary_source", result["reasons"])

    def test_invalid_input_rejected(self):
        with self.assertRaises(TypeError):
            triage(None)


if __name__ == "__main__":
    unittest.main()
