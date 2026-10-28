import unittest
from assurance import assess

class AssuranceTests(unittest.TestCase):
    def setUp(self):
        self.case = {"case_id": "synthetic-001", "scenario_type": "synthetic",
                     "source_id": "GRI-SIM", "observations": {"detected": True, "override_success": False}}

    def test_measurement_and_missingness(self):
        out = assess(self.case)
        self.assertEqual(out["measures"]["defend"], "pass")
        self.assertEqual(out["measures"]["human_authority"], "fail")
        self.assertEqual(out["measures"]["prevail"], "unmeasured")
        self.assertFalse(out["production_validated"])

    def test_determinism(self):
        self.assertEqual(assess(self.case)["record_sha256"], assess(self.case)["record_sha256"])

    def test_no_real_world_case(self):
        self.case["scenario_type"] = "production"
        with self.assertRaises(ValueError):
            assess(self.case)

    def test_no_inferred_success(self):
        self.case["observations"]["patch_verified"] = "yes"
        with self.assertRaises(ValueError):
            assess(self.case)

if __name__ == "__main__":
    unittest.main()
