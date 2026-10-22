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

    def test_head_dashboard_probe(self):
        req = Request(f"http://127.0.0.1:{self.port}/dashboard", method="HEAD")
        with urlopen(req, timeout=3) as response:
            self.assertEqual(response.status, 200)
            self.assertEqual(response.read(), b"")

    def test_registry_valid(self):
        data = load("cases.json")
        self.assertEqual(len({r["id"] for r in data["records"]}), len(data["records"]))

if __name__ == "__main__":
    unittest.main()
