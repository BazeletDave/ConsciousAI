import unittest
from research_rights_gate import validate

def record(**changes):
    result = dict(source_id="LS-001", author="Landry Signé", publisher="Brookings",
                  url="https://example.org", rights_basis="", license="",
                  visibility="public", ingestion_permission=False,
                  training_permission=False, citation_locator="", content_hash="",
                  reviewer="", review_status="proposed")
    result.update(changes)
    return result

class RightsTests(unittest.TestCase):
    def test_metadata_only(self):
        self.assertEqual(validate(record()), [])
    def test_unreviewed_training_blocked(self):
        self.assertTrue(validate(record(training_permission=True)))
    def test_restricted_ingestion_blocked(self):
        self.assertTrue(validate(record(visibility="restricted", ingestion_permission=True)))
    def test_training_without_ingestion_blocked(self):
        self.assertTrue(validate(record(training_permission=True)))
    def test_approved_licensed_training(self):
        self.assertEqual(validate(record(ingestion_permission=True, training_permission=True,
                         rights_basis="written permission", license="written permission",
                         citation_locator="p. 1", content_hash="sha256:abc",
                         reviewer="authorized steward", review_status="approved")), [])
    def test_empty_reviewer_blocked(self):
        self.assertTrue(validate(record(ingestion_permission=True, rights_basis="licensed",
                         citation_locator="p. 1", content_hash="sha256:abc",
                         review_status="approved")))
if __name__ == "__main__":
    unittest.main()
