import unittest
from benchmark_gate import assess_benchmark, _digest

def row(name, split, source):
    return {"record_id": name, "source_id": source, "split": split,
            "label": 1, "observed_at": "2026-10-25T12:00:00Z", "reviews": []}

class BenchmarkGateTests(unittest.TestCase):
    def test_unreviewed_synthetic_rejected(self):
        rows = [row("a", "train", "a"), row("b", "validation", "b"), row("c", "test", "c")]
        report = assess_benchmark(rows, synthetic=True)
        self.assertFalse(report["benchmark_eligible"])
        self.assertIn("synthetic_data_not_eligible", report["findings"])
        self.assertFalse(report["model_promotion_eligible"])

    def test_source_leakage_rejected(self):
        rows = [row("a", "train", "shared"), row("b", "validation", "shared"), row("c", "test", "other")]
        report = assess_benchmark(rows)
        self.assertIn("source_leakage_across_splits", report["findings"])

    def test_review_digests_and_split_gate(self):
        rows = [row("a", "train", "a"), row("b", "validation", "b"), row("c", "test", "c")]
        for item in rows:
            item["reviews"] = [{"reviewer_id": reviewer, "record_digest": _digest(item), "decision": "approve_label"} for reviewer in ("reviewer1", "reviewer2")]
        report = assess_benchmark(rows)
        self.assertTrue(report["benchmark_eligible"])
        self.assertFalse(report["model_promotion_eligible"])
        self.assertFalse(report["publication_authorized"])

    def test_duplicate_id_rejected(self):
        rows = [row("a", "train", "a"), row("a", "validation", "b"), row("c", "test", "c")]
        self.assertIn("duplicate_record_id", assess_benchmark(rows)["findings"])

if __name__ == "__main__":
    unittest.main()
