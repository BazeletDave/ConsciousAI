"""GRI mobility ML evaluation baseline contract.

Synthetic fixtures verify arithmetic and fail-closed model governance only.
These tests do NOT train or independently validate a mobility prediction model.
"""
import math
import unittest

from evaluation_pipeline import evaluate_numeric_predictions, evaluation_capabilities
from model_registry import evaluate_release, platform_capabilities
from assurance_engine import classification_metrics, calibration_metrics, drift_monitor


class MobilityMLEvaluationBaseline(unittest.TestCase):
    def test_no_trained_mobility_model_is_claimed(self):
        capabilities = platform_capabilities()
        self.assertEqual(capabilities["trained_models"], 0)
        mobility = next(m for m in capabilities["models"] if m["id"] == "mobility-offer-forecast")
        self.assertFalse(mobility["trained"])
        self.assertEqual(mobility["status"], "design")
        self.assertEqual(evaluation_capabilities()["verified_evaluations"], 0)

    def test_holdout_sample_floor(self):
        rows = [{"actual": float(i), "predicted": float(i)} for i in range(29)]
        result = evaluate_numeric_predictions(rows)
        self.assertEqual(result["status"], "insufficient_data")
        self.assertFalse(result["eligible_for_release"])

    def test_deterministic_synthetic_metrics_are_not_certification(self):
        rows = [{"actual": float(i), "predicted": float(i + 2)} for i in range(30)]
        a = evaluate_numeric_predictions(rows)
        b = evaluate_numeric_predictions(rows)
        self.assertEqual(a["evaluation_digest"], b["evaluation_digest"])
        self.assertEqual(a["metrics"], {"mae": 2.0, "rmse": 2.0})
        self.assertFalse(a["eligible_for_release"])
        self.assertEqual(a["status"], "evaluated_not_certified")

    def test_nonfinite_predictions_fail(self):
        rows = [{"actual": float(i), "predicted": float(i)} for i in range(30)]
        rows[-1]["predicted"] = math.nan
        with self.assertRaises(ValueError):
            evaluate_numeric_predictions(rows)

    def test_independent_review_is_required_for_release(self):
        result = evaluate_release({"model_id": "mobility-offer-forecast"})
        self.assertFalse(result["eligible"])
        self.assertTrue(any("missing:" in reason for reason in result["reasons"]))

    def test_binary_classification_metrics_on_synthetic_labels(self):
        samples = [
            {"truth": True, "prediction": True},
            {"truth": True, "prediction": False},
            {"truth": False, "prediction": True},
            {"truth": False, "prediction": False},
        ]
        result = classification_metrics(samples)
        self.assertEqual(result["confusion_matrix"], {"tp": 1, "tn": 1, "fp": 1, "fn": 1})
        self.assertEqual(result["accuracy"], 0.5)

    def test_synthetic_brier_score(self):
        result = calibration_metrics([
            {"truth": True, "probability": 0.8},
            {"truth": False, "probability": 0.2},
        ])
        self.assertEqual(result["brier_score"], 0.04)

    def test_drift_heuristic_requires_human_review(self):
        result = drift_monitor([1, 2, 3, 4], [10, 11, 12, 13])
        self.assertTrue(result["heuristic_alert"])
        self.assertTrue(result["review_required"])


if __name__ == "__main__":
    unittest.main()
