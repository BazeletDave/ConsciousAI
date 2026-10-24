import unittest
from evaluation_pipeline import evaluate_numeric_predictions, evaluation_capabilities

class TestEvaluation(unittest.TestCase):
    def test_insufficient(self):
        x=evaluate_numeric_predictions([])
        self.assertEqual(x["status"], "insufficient_data")
        self.assertIsNone(x["metrics"])
    def test_exact_predictions(self):
        x=evaluate_numeric_predictions([{"actual": i, "predicted": i} for i in range(30)])
        self.assertEqual(x["metrics"], {"mae": 0, "rmse": 0})
        self.assertFalse(x["eligible_for_release"])
    def test_known_error(self):
        x=evaluate_numeric_predictions([{"actual": 0, "predicted": 2} for _ in range(30)])
        self.assertEqual(x["metrics"]["mae"], 2)
        self.assertEqual(x["metrics"]["rmse"], 2)
    def test_reproducible(self):
        data=[{"actual": 3, "predicted": 4} for _ in range(30)]
        self.assertEqual(evaluate_numeric_predictions(data)["evaluation_digest"],
                         evaluate_numeric_predictions(data)["evaluation_digest"])
    def test_reject_nan(self):
        with self.assertRaises(ValueError):
            evaluate_numeric_predictions([{"actual": 1, "predicted": float("nan")} for _ in range(30)])
    def test_reject_extra_fields(self):
        with self.assertRaises(ValueError):
            evaluate_numeric_predictions([{"actual": 1, "predicted": 1, "email": "private"} for _ in range(30)])
    def test_reject_minimum_bypass(self):
        with self.assertRaises(ValueError):
            evaluate_numeric_predictions([], min_samples=1)
    def test_no_claims(self):
        self.assertEqual(evaluation_capabilities()["verified_evaluations"], 0)
if __name__ == "__main__": unittest.main()
