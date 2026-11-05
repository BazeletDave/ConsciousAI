import unittest
from research_schema_bridge import candidate_to_draft

C = {"review_status":"HUMAN_REVIEW_REQUIRED","publication_approved":False,
     "training_eligible":False,"digest":"a"*64,"source_type":"reddit",
     "observed_at":"2026-10-26T12:00:00Z","title":"Example",
     "summary":"Unverified claim","url":"https://reddit.com/r/example"}

class BridgeTests(unittest.TestCase):
    def test_draft(self):
        r = candidate_to_draft(C)
        self.assertEqual(r["review_status"], "draft")
        self.assertFalse(r["publication_authorized"])
        self.assertEqual(r["claim_type"], "source_report")

    def test_reject_promotion(self):
        for key, value in [("review_status","approved"),("publication_approved",True),
                           ("training_eligible",True),("digest","invalid")]:
            with self.subTest(key=key), self.assertRaises(ValueError):
                candidate_to_draft(C | {key:value})

    def test_bad_timestamp(self):
        with self.assertRaises(ValueError):
            candidate_to_draft(C | {"observed_at":"2026-10-26"})

if __name__ == "__main__":
    unittest.main()
