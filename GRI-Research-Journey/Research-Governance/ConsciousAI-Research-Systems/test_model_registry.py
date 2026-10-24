import unittest
from model_registry import evaluate_release, platform_capabilities
class TestRegistry(unittest.TestCase):
    def test_catalog(self):
        x=platform_capabilities()
        self.assertEqual(x["trained_models"], 0)
        self.assertEqual(x["registered_models"], 4)
    def test_missing(self):
        self.assertFalse(evaluate_release({})["eligible"])
    def test_reject_unreviewed(self):
        self.assertFalse(evaluate_release(self.good() | {"human_approved": False})["eligible"])
    def test_reject_low_holdout(self):
        self.assertFalse(evaluate_release(self.good() | {"holdout_samples": 2})["eligible"])
    def test_reject_invalid_hash(self):
        self.assertFalse(evaluate_release(self.good() | {"dataset_digest": "fake"})["eligible"])
    def test_reject_same_reviewer(self):
        self.assertFalse(evaluate_release(self.good() | {"reviewer": "owner"})["eligible"])
    def test_valid_gate(self):
        self.assertTrue(evaluate_release(self.good())["eligible"])
    def good(self):
        return dict(model_id="m",version="1",dataset_digest="a"*64,evaluation_digest="b"*64,
                    owner="owner",reviewer="independent",reviewed_at="2026-10-01T00:00:00Z",
                    human_approved=True,holdout_samples=100,metric_name="accuracy",
                    metric_value=0.95,metric_threshold=0.9,privacy_review=True,
                    security_review=True,provenance_verified=True)
if __name__=="__main__": unittest.main()
