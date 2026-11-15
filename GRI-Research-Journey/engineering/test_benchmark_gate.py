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

    def test_whitespace_padded_source_id_rejected(self):
        rows = [row("a", "train", " shared"), row("b", "validation", "shared"), row("c", "test", "other")]
        with self.assertRaisesRegex(ValueError, "invalid source_id"):
            assess_benchmark(rows)

    def test_whitespace_padded_reviewer_identity_not_counted(self):
        rows = [row("a", "train", "a"), row("b", "validation", "b"), row("c", "test", "c")]
        for item in rows:
            item["reviews"] = [
                {"reviewer_id": reviewer, "record_digest": _digest(item), "decision": "approve_label"}
                for reviewer in ("reviewer1", " reviewer2 ")
            ]
        report = assess_benchmark(rows)
        self.assertFalse(report["benchmark_eligible"])
        self.assertIn("independent_label_review_pending", report["findings"])

    def test_conflicting_reviewer_decisions_fail_closed(self):
        rows = [row("a", "train", "a"), row("b", "validation", "b"), row("c", "test", "c")]
        for item in rows:
            item["reviews"] = [
                {"reviewer_id": reviewer, "record_digest": _digest(item), "decision": "approve_label"}
                for reviewer in ("reviewer1", "reviewer2")
            ]
        rows[0]["reviews"].append({"reviewer_id": "reviewer1", "record_digest": _digest(rows[0]), "decision": "reject_label"})
        report = assess_benchmark(rows)
        self.assertFalse(report["benchmark_eligible"])
        self.assertIn("conflicting_reviewer_decisions", report["findings"])
        self.assertIn("independent_label_review_pending", report["findings"])

    def test_duplicate_approval_does_not_count_as_second_reviewer(self):
        rows = [row("a", "train", "a"), row("b", "validation", "b"), row("c", "test", "c")]
        for item in rows:
            approval = {"reviewer_id": "reviewer1", "record_digest": _digest(item), "decision": "approve_label"}
            item["reviews"] = [approval.copy(), approval.copy()]
        report = assess_benchmark(rows)
        self.assertFalse(report["benchmark_eligible"])
        self.assertIn("independent_label_review_pending", report["findings"])

    def test_duplicate_id_rejected(self):
        rows = [row("a", "train", "a"), row("a", "validation", "b"), row("c", "test", "c")]
        self.assertIn("duplicate_record_id", assess_benchmark(rows)["findings"])

if __name__ == "__main__":
    unittest.main()
