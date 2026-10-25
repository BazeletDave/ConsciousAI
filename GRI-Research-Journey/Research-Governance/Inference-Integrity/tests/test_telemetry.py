import sys
import unittest
from datetime import datetime, timezone
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from telemetry import GovernancePayload, InstitutionalDashboardState, validate_payload, demonstration

def sample(**changes):
    values = dict(timestamp=datetime.now(timezone.utc).isoformat(),
                  inference_integrity_score=0.99, active_policy_violations=1,
                  pending_human_reviews=0, replay_status="PASS_SCORE_REPLAY_ONLY",
                  chain_status="VERIFIED_LOCAL", block_index=1)
    values.update(changes)
    return GovernancePayload(**values)

class TelemetryTests(unittest.TestCase):
    def test_valid(self):
        self.assertTrue(validate_payload(sample()))
    def test_invalid_score(self):
        for v in (float("nan"), float("inf"), 1.5, -0.1, True):
            self.assertFalse(validate_payload(sample(inference_integrity_score=v)))
    def test_invalid_metadata(self):
        self.assertFalse(validate_payload(sample(timestamp="not-a-time")))
        self.assertFalse(validate_payload(sample(chain_status="CERTIFIED")))
        self.assertFalse(validate_payload(sample(pending_human_reviews=-1)))
    def test_monotonic_blocks(self):
        state = InstitutionalDashboardState()
        self.assertTrue(state.ingest(sample()))
        self.assertFalse(state.ingest(sample(block_index=1)))
        self.assertTrue(state.ingest(sample(block_index=2)))
    def test_snapshot_isolation(self):
        state = InstitutionalDashboardState()
        original = {"nested": {"count": 1}}
        state.update_research(original)
        original["nested"]["count"] = 9
        view = state.snapshot()
        self.assertEqual(view["research_intelligence"]["nested"]["count"], 1)
        view["research_intelligence"]["nested"]["count"] = 7
        self.assertEqual(state.snapshot()["research_intelligence"]["nested"]["count"], 1)
    def test_demonstration(self):
        self.assertEqual(demonstration()["integration"]["scope"], "SINGLE_PROCESS_DEMONSTRATION")

if __name__ == "__main__":
    unittest.main()
