import unittest
from evidence_quality import score,dataset_manifest
from classification_evaluation import classification_report
class QualityTests(unittest.TestCase):
 def test_score_does_not_certify(self):
  x=score({"id":"case","source":"https://example.org/case","verification_status":"official_event_listing_verified","limitations":"Context and causation have not been independently verified."})
  self.assertFalse(x["independently_verified"]);self.assertFalse(x["publication_authorized"])
 def test_manifest_rejects_duplicates(self):
  with self.assertRaises(ValueError):dataset_manifest([{"id":"x"},{"id":"x"}])
 def test_insufficient_labels(self):
  self.assertEqual(classification_report([])["status"],"insufficient_independently_labeled_data")
 def test_attestation_gate(self):
  rows=[{"record_id":str(i),"actual":i%2,"predicted":i%2,"label_provenance":"unreviewed","holdout":True} for i in range(30)]
  with self.assertRaises(ValueError):classification_report(rows)
 def test_metrics_math(self):
  rows=[{"record_id":str(i),"actual":i%2,"predicted":i%2,"label_provenance":"independent_review_attested","holdout":True} for i in range(30)]
  report=classification_report(rows)
  self.assertEqual(report["metrics"]["accuracy"],1.0)
  self.assertFalse(report["release_authorized"])
if __name__=="__main__":unittest.main()
