import unittest
from ingest_federal_register import collect, merge

class IngestionTests(unittest.TestCase):
    def test_official_metadata_is_unreviewed(self):
        def fake(url):
            return {"results": [{"document_number": "2026-12345", "html_url":
                "https://www.federalregister.gov/d/2026-12345",
                "title": "Artificial Intelligence Research",
                "type": "NOTICE", "publication_date": "2026-10-19"}]}
        found = collect(fetch=fake, now="2026-10-19T12:00:00+00:00")
        self.assertEqual(len(found), 1)
        row = found["2026-12345"]
        self.assertEqual(row["verification_status"], "official_api_metadata_unreviewed")
        self.assertTrue(row["review_required"])

    def test_merge_preserves_first_seen(self):
        old = {"records": [{"id": "US-FR-2026-12345", "first_seen_at": "first",
                            "verification_status": "reviewed", "review_required": False}]}
        fresh = {"2026-12345": {"id": "US-FR-2026-12345", "first_seen_at": "later",
                 "last_seen_at": "later", "verification_status": "official_api_metadata_unreviewed",
                 "review_required": True, "publication_date": "2026-10-19"}}
        result = merge(old, fresh)
        self.assertEqual(result["records"][0]["first_seen_at"], "first")
        self.assertEqual(result["records"][0]["verification_status"], "reviewed")

if __name__ == "__main__":
    unittest.main()
