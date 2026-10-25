import unittest
from research_intake import build_knowledge_snapshot, load_snapshot

def example(**overrides):
    row = dict(id="GRI-TEST-001", title="Testable governance question", date="2026-10-25",
               domain="ai_governance", claim_type="hypothesis", summary="Test whether human review improves decision quality.",
               source_type="independent_research", provenance="GRI working hypothesis",
               limitations="Not empirically tested", review_status="draft", publication_authorized=False)
    row.update(overrides)
    return row

class ResearchIntakeTests(unittest.TestCase):
    def test_empty_registry(self):
        self.assertEqual(load_snapshot()["record_count"], 0)
    def test_draft_is_not_published(self):
        self.assertEqual(build_knowledge_snapshot([example()])["record_count"], 0)
    def test_approved_record_is_published(self):
        item = example(review_status="approved", publication_authorized=True, reviewer="GRI human reviewer")
        result = build_knowledge_snapshot([item])
        self.assertEqual(result["record_count"], 1)
        self.assertNotIn("provenance", result["records"][0])
    def test_publication_without_review_fails(self):
        with self.assertRaises(ValueError):
            build_knowledge_snapshot([example(publication_authorized=True)])
    def test_approval_requires_reviewer(self):
        with self.assertRaises(ValueError):
            build_knowledge_snapshot([example(review_status="approved")])
    def test_duplicate_fails(self):
        with self.assertRaises(ValueError):
            build_knowledge_snapshot([example(), example()])
    def test_deterministic_digest(self):
        self.assertEqual(build_knowledge_snapshot([example()])["sha256"],
                         build_knowledge_snapshot([example()])["sha256"])

if __name__ == "__main__":
    unittest.main()
