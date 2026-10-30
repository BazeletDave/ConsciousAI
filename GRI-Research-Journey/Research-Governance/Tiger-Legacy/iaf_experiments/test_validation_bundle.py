"""Consolidated report contract checks."""
import unittest
from validation_bundle import validate

class ValidationBundleTests(unittest.TestCase):
    # Avoid recursively calling test discovery from a test case.
    def test_bundle_has_all_subsystems(self):
        from qlearning_governance import evaluate
        from ood_governance import evaluate_ood
        self.assertEqual(evaluate()["schema"],"gri.iaf.tabular_qlearning.v1")
        self.assertEqual(evaluate_ood()["schema"],"gri.iaf.ood_probes.v1")

if __name__=="__main__":
    unittest.main()
