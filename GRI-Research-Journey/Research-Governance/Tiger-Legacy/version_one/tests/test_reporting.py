"""Offline adapter contract and fail-closed integration tests."""
import copy
import json
import tempfile
import unittest
from pathlib import Path
from reporting import build_synthetic_report, read_snapshot, verify_report
from tiger_legacy import canonical
from hashlib import sha256

class ReportingIntegrationTests(unittest.TestCase):
    def setUp(self):
        self.report = build_synthetic_report("synthetic-test-commit")

    def test_verified_read_only_contract(self):
        summary = verify_report(self.report)
        self.assertEqual(summary["fixture_checks_passed"], 4)
        self.assertEqual(summary["production_security"], "unmeasured")
        self.assertFalse(summary["model_promoted"])
        self.assertEqual(summary["operational_actions_authorized"], 0)
        self.assertNotIn("fixture_checks", summary)

    def test_offline_snapshot_read_does_not_modify_file(self):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / "report.json"
            p.write_text(json.dumps(self.report), encoding="utf-8")
            before = p.read_bytes()
            self.assertEqual(read_snapshot(p)["fixture_checks_total"], 4)
            self.assertEqual(p.read_bytes(), before)

    def test_tamper_fails_closed(self):
        changed = copy.deepcopy(self.report)
        changed["fixture_checks_passed"] = 100
        with self.assertRaises(ValueError):
            verify_report(changed)

    def test_rehashed_unsafe_claim_fails_closed(self):
        changed = copy.deepcopy(self.report)
        changed["model_promoted"] = True
        changed["content_sha256"] = sha256(canonical({k:v for k,v in changed.items() if k != "content_sha256"})).hexdigest()
        with self.assertRaises(ValueError):
            verify_report(changed)

    def test_rehashed_failed_check_fails_closed(self):
        changed = copy.deepcopy(self.report)
        changed["fixture_checks"]["cross_tenant_denied"] = False
        changed["content_sha256"] = sha256(canonical({k:v for k,v in changed.items() if k != "content_sha256"})).hexdigest()
        with self.assertRaises(ValueError):
            verify_report(changed)

    def test_missing_snapshot_fails_closed(self):
        with self.assertRaises(FileNotFoundError):
            read_snapshot("/nonexistent/gri-tiger-legacy-report.json")

    def test_deterministic_report(self):
        self.assertEqual(self.report, build_synthetic_report("synthetic-test-commit"))

    def test_no_client_identifiers_exposed(self):
        public = verify_report(self.report)
        self.assertNotIn("alpha", json.dumps(public))
        self.assertNotIn("alice", json.dumps(public))

if __name__ == "__main__":
    unittest.main()
