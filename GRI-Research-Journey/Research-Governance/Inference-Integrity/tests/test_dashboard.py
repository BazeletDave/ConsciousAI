import sys
import unittest
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from dashboard import build_telemetry

class DashboardTests(unittest.TestCase):
    def test_deterministic_synthetic_evidence(self):
        first, second = build_telemetry(12), build_telemetry(12)
        self.assertEqual(first.to_dict("records"), second.to_dict("records"))
        self.assertTrue(first.attrs["chain_verified"])
        self.assertTrue((first["replay_status"] == "PASS_SCORE_REPLAY_ONLY").all())
        self.assertTrue((first["human_review"] == "NOT_IMPLEMENTED").all())

if __name__ == "__main__":
    unittest.main()
