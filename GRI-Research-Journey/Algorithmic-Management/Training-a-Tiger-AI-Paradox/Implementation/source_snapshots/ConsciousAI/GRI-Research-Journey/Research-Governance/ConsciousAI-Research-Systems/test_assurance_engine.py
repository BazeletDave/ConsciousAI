import unittest
from assurance_engine import evaluate, classification_metrics, calibration_metrics, drift_monitor
class AssuranceTests(unittest.TestCase):
    def setUp(self):
        self.record={"id":"synthetic-1","claim":"Test claim","observed_at":"2026-10-22T00:00:00Z","verification_status":"verified","sources":[{"publisher":"A","url":"https://example.org/a","independently_reviewed":True},{"publisher":"B","url":"https://example.org/b","independently_reviewed":True}]}
    def test_verified_requires_human_review(self):
        x=evaluate(self.record)
        self.assertEqual(x["decision"],"eligible_for_human_publication_review")
        self.assertTrue(x["review_required"])
        self.assertFalse(x["automated_remediation_allowed"])
    def test_missing_independent_evidence_fails_closed(self):
        self.record["sources"]=self.record["sources"][:1]
        self.assertEqual(evaluate(self.record)["decision"],"hold_for_review")
    def test_contradiction_blocks(self):
        self.record["contradictory_evidence"]=True
        self.assertEqual(evaluate(self.record)["decision"],"hold_for_review")
    def test_invalid_source(self):
        self.record["sources"][0]["url"]="http://invalid"
        with self.assertRaises(ValueError):evaluate(self.record)
    def test_classification(self):
        x=classification_metrics([{"truth":True,"prediction":True},{"truth":False,"prediction":True},{"truth":False,"prediction":False},{"truth":True,"prediction":False}])
        self.assertEqual(x["accuracy"],0.5)
        self.assertEqual(x["false_positive_rate"],0.5)
    def test_calibration(self):
        self.assertEqual(calibration_metrics([{"truth":True,"probability":0.8},{"truth":False,"probability":0.2}])["brier_score"],0.04)
    def test_drift(self):
        self.assertTrue(drift_monitor([1,2,3],[9,10])["heuristic_alert"])
if __name__=="__main__":unittest.main()
