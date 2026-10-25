"""Regression checks for the public case explorer; no network or private course files."""
import unittest
from institutional_cases import public_case_explorer

class CaseExplorerTests(unittest.TestCase):
    def test_registry_provenance_and_limitations(self):
        snapshot=public_case_explorer()
        self.assertEqual(snapshot["count"],len(snapshot["records"]))
        self.assertGreater(snapshot["count"],0)
        for item in snapshot["records"]:
            self.assertTrue(item["source_reference"])
            self.assertTrue(item["limitations"])
            self.assertEqual(item["independent_validation"],"not_established")
            self.assertIn(item["source_kind"],("public_url","repository_reference"))
            for related in item["related_public_events"]:
                self.assertEqual(related["relation"],"analytical_research_link_not_causation")
    def test_no_course_assessments_or_unwarranted_claims(self):
        snapshot=public_case_explorer()
        self.assertEqual(snapshot["mode"],"public_registry_read_only")
        self.assertIn("not independently validated",snapshot["notice"])

if __name__=="__main__":
    unittest.main()
