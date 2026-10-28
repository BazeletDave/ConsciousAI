import unittest
from evidence_validation import validate, summarize

def sample(**changes):
    record = dict(record_id="r1", case_id="case1", domain="defend", observation_type="controlled_experiment",
        observed_at="2026-10-28T12:00:00Z", source_url="https://example.org/evidence/1",
        source_sha256="a"*64, outcome=True, reviewer_id="reviewer2",
        reviewed_at="2026-10-28T13:00:00Z", independent_review=True,
        consent_or_authority="authorized experiment", source_verified=True, scenario_type="real")
    record.update(changes)
    return record

class EvidenceValidationTests(unittest.TestCase):
    def test_deterministic(self):
        self.assertEqual(validate(sample()), validate(sample()))
    def test_synthetic_rejected(self):
        with self.assertRaises(ValueError): validate(sample(scenario_type="synthetic"))
    def test_unreviewed_rejected(self):
        with self.assertRaises(ValueError): validate(sample(independent_review=False))
    def test_unverified_source_rejected(self):
        with self.assertRaises(ValueError): validate(sample(source_verified=False))
    def test_http_rejected(self):
        with self.assertRaises(ValueError): validate(sample(source_url="http://example.org"))
    def test_review_before_capture_rejected(self):
        with self.assertRaises(ValueError): validate(sample(reviewed_at="2026-10-27T12:00:00Z"))
    def test_duplicate_excluded(self):
        result = summarize([sample(), sample()])
        self.assertEqual(result["domains"][0]["validated_records"], 1)
        self.assertEqual(result["rejected_count"], 1)
    def test_unmeasured_remains_unmeasured(self):
        result = summarize([sample(outcome=False)])
        self.assertEqual(result["domains"][0]["observed_pass_fraction"], 0)
        self.assertEqual(result["domains"][1]["status"], "unmeasured")
    def test_string_outcome_rejected(self):
        with self.assertRaises(ValueError): validate(sample(outcome="true"))

if __name__ == "__main__":
    unittest.main()
