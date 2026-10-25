import unittest
from evidence_pipeline import normalize, deduplicate
from evaluation_gate import evaluate_binary, drift_alert

class EvidenceTests(unittest.TestCase):
    def setUp(self):
        self.record = dict(source_id="test-source", source_url="https://example.org/research",
                           claim="synthetic test", captured_at="2026-10-25T12:00:00-04:00",
                           jurisdiction="US")

    def test_deterministic_and_no_publication(self):
        a = normalize(self.record)
        self.assertEqual(a["evidence_digest"], normalize(self.record)["evidence_digest"])
        self.assertFalse(a["publication_authorized"])
        self.assertEqual(len(deduplicate([self.record, self.record])), 1)

    def test_reject_insecure_url(self):
        with self.assertRaises(ValueError):
            normalize({**self.record, "source_url": "http://example.org"})

    def test_reject_naive_timestamp(self):
        with self.assertRaises(ValueError):
            normalize({**self.record, "captured_at": "2026-10-25T12:00:00"})

    def test_reject_unsupported_verification(self):
        with self.assertRaises(ValueError):
            normalize({**self.record, "verification_status": "verified"})

class EvaluationTests(unittest.TestCase):
    def test_metrics_are_not_approval(self):
        result = evaluate_binary([0, 1], [0.1, 0.9])
        self.assertEqual(result["accuracy"], 1.0)
        self.assertAlmostEqual(result["brier_score"], 0.01)
        self.assertFalse(result["model_promotion_eligible"])

    def test_invalid_probabilities(self):
        with self.assertRaises(ValueError):
            evaluate_binary([1], [float("nan")])

    def test_drift_cannot_trigger_retraining(self):
        result = drift_alert([0, 0], [1, 1])
        self.assertTrue(result["alert"])
        self.assertFalse(result["automatic_retraining_allowed"])

if __name__ == "__main__":
    unittest.main()
