import unittest
from mobility_engine import evaluate_offer, rank_offers, public_summary
class TestMobility(unittest.TestCase):
    def setUp(self):
        self.schedule = {"max_finish_time_hour": 22, "sleep_hours_available": 7.5}
        self.offer = {"offer_id": "U1", "platform": "Uber", "offered_pay": 38.5, "incentives": 5,
                      "pickup_miles": 2.1, "ride_miles": 18.4, "waiting_min": 5, "duration_min": 35,
                      "tolls": 2, "offer_time_hour": 18, "return_home_transit_min": 25}
    def test_economics(self):
        x = evaluate_offer(self.offer, self.schedule)
        self.assertEqual((x["estimated_net"], x["net_per_full_hour"]), (33.71, 31.12))
    def test_class(self):
        self.assertIn("class_conflict", evaluate_offer(dict(self.offer, overlaps_class_block=True), self.schedule)["rejection_reasons"])
    def test_deadline(self):
        self.assertIn("return_deadline", evaluate_offer(dict(self.offer, offer_time_hour=21.5), self.schedule)["rejection_reasons"])
    def test_sleep(self):
        self.assertIn("sleep_limit", evaluate_offer(self.offer, dict(self.schedule, sleep_hours_available=5))["rejection_reasons"])
    def test_invalid(self):
        for field, value in (("ride_miles", -1), ("offered_pay", float("nan"))):
            with self.assertRaises(ValueError): evaluate_offer(dict(self.offer, **{field: value}), self.schedule)
    def test_ranking(self):
        x = rank_offers([dict(self.offer, offer_id="LOW", offered_pay=10), self.offer], self.schedule)
        self.assertEqual(x["feasible_ranked"][0]["offer_id"], "U1")
    def test_no_fake_ml(self):
        self.assertEqual(public_summary()["trained_models"], 0)
if __name__ == "__main__": unittest.main()
