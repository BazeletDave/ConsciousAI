"""Run with python -m unittest discover -v."""
import json
import threading
import unittest
from http.server import ThreadingHTTPServer
from urllib.request import urlopen, Request
from urllib.error import HTTPError
from server import Handler, graph, assessment, load

class ResearchServiceTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.server = ThreadingHTTPServer(("127.0.0.1", 0), Handler)
        cls.port = cls.server.server_port
        cls.thread = threading.Thread(target=cls.server.serve_forever, daemon=True)
        cls.thread.start()

    @classmethod
    def tearDownClass(cls):
        cls.server.shutdown()
        cls.server.server_close()
        cls.thread.join(timeout=2)

    def fetch(self, path, body=None):
        data = None if body is None else json.dumps(body).encode()
        req = Request(f"http://127.0.0.1:{self.port}{path}", data=data,
                      headers={"Content-Type": "application/json"} if data else {})
        with urlopen(req, timeout=3) as res:
            return json.load(res)

    def test_graph_references_resolve(self):
        g = graph()
        self.assertEqual(len(g["nodes"]), 9)
        self.assertEqual(len(g["edges"]), 12)

    def test_cases_filter(self):
        result = self.fetch("/cases?organization=Uber")
        self.assertEqual(result["count"], 2)

    def test_case(self):
        self.assertEqual(self.fetch("/cases/GRI-LYFT-CHI-002")["organization"], "Lyft")

    def test_assessment_not_certification(self):
        a = self.fetch("/assessments", {"case_id": "GRI-LYFT-CHI-002"})
        self.assertTrue(a["review_required"])
        self.assertEqual(a["determination"], "not_assessed_for_ethics_or_legal_compliance")

    def test_unknown_case(self):
        with self.assertRaises(HTTPError) as ctx:
            self.fetch("/cases/NOT-REAL")
        self.assertEqual(ctx.exception.code, 404)

    def test_policies_empty_not_live(self):
        self.assertEqual(self.fetch("/policies")["records"], [])

    def test_intelligence_summary_preserves_verification_categories(self):
        summary = self.fetch("/intelligence/summary")
        self.assertEqual(summary["assessment_type"], "registry_inventory_not_independent_verification")
        self.assertEqual(summary["counts"]["cases"], len(load("cases.json")["records"]))
        self.assertEqual(summary["counts"]["events"], len(load("events.json")["records"]))
        self.assertEqual(sum(summary["verification_status_counts"].values()), sum(summary["counts"].values()))

    def test_ai_intelligence_watchlist_is_explicitly_unverified(self):
        data = self.fetch("/ai-intelligence")
        self.assertEqual(data["status"], "curated_research_watchlist_not_live_verified_feed")
        self.assertGreaterEqual(len(data["records"]), 4)
        for record in data["records"]:
            self.assertIn("pending_primary_source_review", record["verification_status"])
            self.assertTrue(record["sources"])
            self.assertTrue(all(source["url"].startswith("https://") for source in record["sources"]))

    def test_assurance_overview_is_read_only_and_unmeasured(self):
        result = self.fetch("/assurance/overview")
        self.assertEqual(result["records_assessed"], len(load("ai_intelligence.json")["records"]))
        self.assertEqual(result["review_required"], result["records_assessed"])
        self.assertEqual(result["eligible_for_human_publication_review"], 0)
        self.assertIsNone(result["accuracy"])
        self.assertIsNone(result["brier_score"])
        self.assertIsNone(result["drift"])
        self.assertTrue(all(x["assessment"]["decision"] == "hold_for_review" for x in result["items"]))
        self.assertTrue(all(not x["assessment"]["automated_remediation_allowed"] for x in result["items"]))

    def test_triage_endpoint_is_read_only_and_explainable(self):
        result = self.fetch("/intelligence/triage")
        self.assertEqual(result["count"], len(load("events.json")["records"]))
        self.assertEqual(result["method"], "deterministic_missing_evidence_heuristic")
        self.assertTrue(all(x["requires_human_review"] for x in result["records"]))
        self.assertTrue(all(x["model_trained"] is False for x in result["records"]))

    def test_head_dashboard_probe(self):
        req = Request(f"http://127.0.0.1:{self.port}/dashboard", method="HEAD")
        with urlopen(req, timeout=3) as response:
            self.assertEqual(response.status, 200)
            self.assertEqual(response.read(), b"")

    def test_governance_telemetry_fails_closed_without_source(self):
        from unittest.mock import patch
        with patch.dict("os.environ", {"GRI_GOVERNANCE_TELEMETRY_PATH": "/nonexistent/gri-source.json"}):
            data = self.fetch("/governance/telemetry")
        self.assertEqual(data["status"], "not_connected")
        self.assertIsNone(data["metrics"])

    def test_assurance_evidence_integrity_and_classification(self):
        from pathlib import Path
        from hashlib import sha256
        from build_assurance_evidence import canonical
        from server import ROOT
        path = ROOT / "assurance_evidence_snapshot.json"
        if not path.exists():
            self.skipTest("Evidence snapshot not yet generated by scheduled workflow")
        data = self.fetch("/governance/assurance-evidence")
        self.assertEqual(data["status"], "source_integrity_checked_not_independently_audited")
        self.assertEqual(data["source"], "gri_deterministic_assurance_engine")
        self.assertEqual(data["content_sha256"], sha256(canonical({k:v for k,v in data.items() if k not in ("content_sha256","status")})).hexdigest())
        self.assertEqual(data["evaluation_count"], len(data["results"]))
        self.assertEqual(data["human_review_count"], sum(x["review_required"] for x in data["results"]))

    def test_health_endpoint(self):
        data = self.fetch("/health")
        self.assertEqual(data["status"], "ok")
        self.assertEqual(data["missing"], [])
        self.assertEqual(data["invalid"], [])

    def test_registry_valid(self):
        data = load("cases.json")
        self.assertEqual(len({r["id"] for r in data["records"]}), len(data["records"]))

if __name__ == "__main__":
    unittest.main()
