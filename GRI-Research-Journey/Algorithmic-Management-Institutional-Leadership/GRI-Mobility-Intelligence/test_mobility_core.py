"""Run: python -m unittest discover -p 'test_mobility_core.py' in this directory."""
import unittest
from mobility_core import evaluate_scenario, validate_record, net_contribution, baseline_forecast, compare_strategies

RECORD = dict(record_id="synthetic-1", consent_id="synthetic-consent", consent_active=True,
    synthetic=True, event_type="PAYMENT_SETTLED", start="2026-11-05T18:00:00-05:00",
    end="2026-11-05T19:00:00-05:00", gross=30, tips=5, incentives=2,
    incentives_in_gross=False, paid_miles=10, unpaid_miles=5, cost_per_mile=.4,
    tolls=2, source="synthetic fixture")
SCENARIO = dict(start="2026-11-05T18:00:00-05:00", end="2026-11-05T20:00:00-05:00",
    return_by="2026-11-05T21:00:00-05:00", next_commitment="2026-11-06T08:00:00-05:00",
    minimum_sleep_hours=8, max_duty_hours=4, gross=50, miles=30, cost_per_mile=.4,
    tolls=3, uncertainty=10)

class MobilityTests(unittest.TestCase):
    def test_net(self):
        self.assertEqual(net_contribution(RECORD), 29)
    def test_declined_not_realized(self):
        r = dict(RECORD, event_type="OFFER_DECLINED", gross=0, tips=0, tolls=0)
        self.assertTrue(validate_record(r))
        with self.assertRaises(ValueError): net_contribution(r)
    def test_no_consent(self):
        with self.assertRaises(ValueError): validate_record(dict(RECORD, consent_active=False))
    def test_pii_field_rejected(self):
        with self.assertRaises(ValueError): validate_record(dict(RECORD, passenger_name="private"))
    def test_bad_numbers(self):
        with self.assertRaises(ValueError): validate_record(dict(RECORD, paid_miles=float("nan")))
    def test_no_drive(self):
        self.assertTrue(evaluate_scenario(SCENARIO, {"blocked_intervals":[]})["no_drive"]["feasible"])
    def test_return_deadline(self):
        r = evaluate_scenario(dict(SCENARIO, return_by="2026-11-05T19:00:00-05:00"), {"blocked_intervals":[]})
        self.assertFalse(r["drive"]["feasible"])
    def test_sleep(self):
        r = evaluate_scenario(dict(SCENARIO, next_commitment="2026-11-06T02:00:00-05:00"), {"blocked_intervals":[]})
        self.assertFalse(r["drive"]["feasible"])
    def test_schedule(self):
        r = evaluate_scenario(SCENARIO, {"blocked_intervals":[{"start":"2026-11-05T19:00:00-05:00","end":"2026-11-05T20:00:00-05:00"}]})
        self.assertFalse(r["drive"]["feasible"])
    def test_duty(self):
        r = evaluate_scenario(dict(SCENARIO, max_duty_hours=1), {"blocked_intervals":[]})
        self.assertFalse(r["drive"]["feasible"])
    def test_negative_net(self):
        r = evaluate_scenario(dict(SCENARIO, gross=0), {"blocked_intervals":[]})
        self.assertFalse(r["drive"]["recommended"])
    def test_named_strategy_selection(self):
        options = {"local": SCENARIO, "unpaid_reposition": dict(SCENARIO, miles=120)}
        result = compare_strategies(options, {"blocked_intervals":[]})
        self.assertEqual(result["selected"], "local")
        self.assertTrue(result["no_drive"]["feasible"])
    def test_all_infeasible_selects_no_drive(self):
        options = {"late_return": dict(SCENARIO, return_by="2026-11-05T19:00:00-05:00")}
        self.assertEqual(compare_strategies(options, {"blocked_intervals":[]})["selected"], "no_drive")
    def test_forecast(self):
        self.assertEqual(baseline_forecast([10, 20, 30], 2)["estimate"], 15)
    def test_forecast_insufficient(self):
        with self.assertRaises(ValueError): baseline_forecast([10], 1)

if __name__ == "__main__":
    unittest.main()
