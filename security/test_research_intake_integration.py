"""Integration checks for the production research intake validation path."""
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "GRI-Research-Journey" / "Research-Governance" / "ConsciousAI-Research-Systems"))
from research_intake import validate

def base(**updates):
    r = dict(id="GRI-TEST-001", title="Test", date="2026-10-28",
             domain="ai_governance", claim_type="source_report", summary="Test only",
             source_type="faculty_publication", provenance="public listing",
             limitations="unreviewed", review_status="approved",
             publication_authorized=True, reviewer="GRI reviewer")
    r.update(updates)
    return r

class Integration(unittest.TestCase):
    def test_external_without_rights_fails_closed(self):
        with self.assertRaisesRegex(ValueError, "research rights gate"):
            validate(base())
    def test_external_without_permission_cannot_publish(self):
        rights = dict(source_id="LS-001", author="Landry Signé", publisher="Brookings",
                      url="https://example.org", rights_basis="", license="",
                      visibility="public", ingestion_permission=False,
                      training_permission=False, citation_locator="", content_hash="")
        with self.assertRaisesRegex(ValueError, "publication requires approved ingestion rights"):
            validate(base(**rights))
    def test_external_approved_source_allowed(self):
        rights = dict(source_id="LS-001", author="Landry Signé", publisher="Brookings",
                      url="https://example.org", rights_basis="authorized metadata reuse",
                      license="", visibility="public", ingestion_permission=True,
                      training_permission=False, citation_locator="publisher listing",
                      content_hash="sha256:test", review_status="approved")
        self.assertEqual(validate(base(**rights))["source_id"], "LS-001")

if __name__ == "__main__":
    unittest.main()
