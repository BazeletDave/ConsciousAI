"""Tests for fail-closed GRI production assurance classification."""
import unittest
from production_assurance_gate import assess, REQUIRED

class ProductionAssuranceGateTests(unittest.TestCase):
    def test_missing_evidence_never_certifies(self):
        report=assess({"controls":{}})
        self.assertFalse(report["certified"])
        self.assertEqual(report["classification"],"production_certification_pending")
        self.assertEqual(report["verified_controls"],0)
    def test_partial_evidence_remains_pending(self):
        report=assess({"controls":{REQUIRED[0]:{"passed":True,"evidence_uri":"https://example.org/review","reviewer":"auditor","verified_at_utc":"2026-10-25T00:00:00Z"}}})
        self.assertEqual(report["verified_controls"],1)
        self.assertFalse(report["certified"])
    def test_all_evidence_only_qualifies_for_external_review(self):
        item={"passed":True,"evidence_uri":"urn:sha256:"+"a"*64,"reviewer":"auditor","verified_at_utc":"2026-10-25T00:00:00Z"}
        report=assess({"controls":{key:item for key in REQUIRED}})
        self.assertEqual(report["classification"],"internal_release_ready_for_external_certification_review")
        self.assertFalse(report["certified"])
if __name__=="__main__":
    unittest.main()
