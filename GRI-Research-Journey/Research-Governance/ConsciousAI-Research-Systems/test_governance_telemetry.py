import json
import tempfile
import unittest
from datetime import datetime, timezone, timedelta
from pathlib import Path
from governance_telemetry import public_snapshot

def sample():
    return dict(schema_version="1.0", source="approved_operational_telemetry",
        observed_at=datetime.now(timezone.utc).isoformat(), inference_count=10,
        score_replay_pass_count=9, policy_block_count=2, pending_human_review_count=1,
        replay_status="PASS_SCORE_REPLAY_ONLY", chain_status="VERIFIED_LOCAL",
        chain_tip_sha256="a"*64, block_index=10)

class PublicTelemetryTests(unittest.TestCase):
    def read(self, data):
        with tempfile.TemporaryDirectory() as folder:
            path=Path(folder)/"telemetry.json"
            path.write_text(json.dumps(data), encoding="utf-8")
            return public_snapshot(path)
    def test_valid(self):
        self.assertEqual(self.read(sample())["metrics"]["score_replay_pass_rate"], .9)
    def test_rejects_synthetic_source(self):
        d=sample();d["source"]="SYNTHETIC"
        self.assertEqual(self.read(d)["status"],"invalid_source")
    def test_rejects_impossible_count(self):
        d=sample();d["score_replay_pass_count"]=11
        self.assertEqual(self.read(d)["status"],"invalid_source")
    def test_rejects_stale(self):
        d=sample();d["observed_at"]=(datetime.now(timezone.utc)-timedelta(hours=5)).isoformat()
        self.assertEqual(self.read(d)["status"],"stale")
    def test_missing_source(self):
        self.assertEqual(public_snapshot("/nonexistent/gri-telemetry.json")["status"],"not_connected")

if __name__=="__main__":
    unittest.main()
