"""Issue 13 deterministic retrospective and safety tests."""
import unittest
from mobility_evaluation import temporal_evaluation, compare_policy_cases

BASE = dict(start="2026-11-05T18:00:00-05:00", end="2026-11-05T20:00:00-05:00",
    return_by="2026-11-05T21:00:00-05:00", next_commitment="2026-11-06T08:00:00-05:00",
    minimum_sleep_hours=8, max_duty_hours=4, gross=50, miles=30,
    cost_per_mile=.4, tolls=3, uncertainty=10)

class EvaluationTests(unittest.TestCase):
    def test_disjoint_temporal_holdout(self):
        r = temporal_evaluation([10,12,11,13,14,15,16,17])
        self.assertEqual(r["splits"], {"train":4,"calibration":2,"holdout":2})
        self.assertEqual(r["forecast"], 11.5)
    def test_interval_and_ood(self):
        r = temporal_evaluation([10,12,11,13,14,15,16,17])
        self.assertEqual(r["ood"]["outside_training_range"], 2)
        self.assertEqual(r["holdout_coverage"], 0)
    def test_no_holdout_rejected(self):
        with self.assertRaises(ValueError):
            temporal_evaluation([1,2,3,4,5,6,7,8], 6, 2)
    def test_nan_rejected(self):
        with self.assertRaises(ValueError):
            temporal_evaluation([1,2,3,4,5,6,7,float("nan")])
    def test_policy_comparison(self):
        cases = {"local":BASE, "costly":dict(BASE, gross=70, miles=160)}
        result = compare_policy_cases(cases, {"blocked_intervals":[]})
        self.assertEqual(result["constrained_selection"], "local")
        self.assertEqual(result["gross_only_feasible_baseline"], "costly")
    def test_hard_constraints(self):
        cases = {"unsafe":dict(BASE, return_by="2026-11-05T19:00:00-05:00")}
        result = compare_policy_cases(cases, {"blocked_intervals":[]})
        self.assertEqual(result["constrained_selection"], "no_drive")
        self.assertEqual(result["gross_only_feasible_baseline"], "no_drive")

if __name__ == "__main__":
    unittest.main()
