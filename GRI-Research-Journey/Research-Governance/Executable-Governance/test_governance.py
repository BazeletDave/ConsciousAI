import unittest
from governance import Event, evaluate

class GovernanceTests(unittest.TestCase):
    def event(self, **changes):
        d = dict(event_id="t1", moving=True, handling_detected=True,
                 driver_attribution_verified=True, confidence=0.95)
        d.update(changes)
        return Event(**d)

    def test_warning(self):
        self.assertEqual(evaluate(self.event())["action"],"WARNING_PERMITTED")
    def test_not_moving(self):
        self.assertEqual(evaluate(self.event(moving=False))["action"],"NO_ACTION")
    def test_not_handling(self):
        self.assertEqual(evaluate(self.event(handling_detected=False))["action"],"NO_ACTION")
    def test_no_attribution(self):
        self.assertEqual(evaluate(self.event(driver_attribution_verified=False))["action"],"NO_ACTION")
    def test_uncertain(self):
        self.assertEqual(evaluate(self.event(confidence=0.89))["action"],"REVIEW_EVIDENCE")
    def test_boundary(self):
        self.assertEqual(evaluate(self.event(confidence=0.90))["action"],"WARNING_PERMITTED")
    def test_invalid_confidence(self):
        with self.assertRaises(ValueError): evaluate(self.event(confidence=1.2))
    def test_no_real_world_inputs(self):
        with self.assertRaises(ValueError): evaluate(self.event(source_type="real"))
    def test_reproducible_audit(self):
        self.assertEqual(evaluate(self.event())["decision_hash"],evaluate(self.event())["decision_hash"])

if __name__ == "__main__":
    unittest.main()
