"""Standard library regression tests for the BZLT evidence metadata validator."""
import csv
import unittest
from pathlib import Path
from bzlt_assurance import audit

ROOT = Path(__file__).resolve().parent

class EvidenceAssuranceTests(unittest.TestCase):
    def setUp(self):
        with (ROOT / "BZLT-Dated-Relationships.csv").open(newline="", encoding="utf-8") as f:
            self.rows = list(csv.DictReader(f))

    def test_current_public_edge_register(self):
        result = audit(self.rows)
        self.assertEqual(result["status"], "PASS", result["findings"])
        self.assertGreaterEqual(result["records"], 10)

    def test_duplicate_and_missing_source_fail(self):
        rows = [dict(self.rows[0]), dict(self.rows[0])]
        rows[1]["source_url"] = ""
        result = audit(rows)
        self.assertEqual(result["status"], "FAIL")
        self.assertIn("duplicate_id", [f["code"] for f in result["findings"]])
        self.assertIn("missing_field", [f["code"] for f in result["findings"]])

    def test_invalid_date_and_non_https_fail(self):
        row = dict(self.rows[0])
        row["effective_date"] = "2026-13-50"
        row["source_url"] = "http://example.com"
        result = audit([row])
        self.assertEqual(result["errors"], 2)

    def test_unknown_relation_requires_review(self):
        row = dict(self.rows[0])
        row["relation"] = "alleged_owner"
        result = audit([row])
        self.assertEqual(result["errors"], 0)
        self.assertEqual(result["warnings"], 1)

if __name__ == "__main__":
    unittest.main()
