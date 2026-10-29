import unittest
from financial_ai_assurance import assess,DOMAINS
class AssuranceTests(unittest.TestCase):
 def test_missing_evidence_blocks(self):
  result=assess({})
  self.assertEqual(len(result["checks"]),8)
  self.assertEqual(result["overall"],"blocked_missing_critical_evidence")
  self.assertFalse(result["certified"])
 def test_partial_remains_pending(self):
  result=assess({"evidence":{"provenance":{"reference":"a"}}})
  self.assertEqual(result["checks"]["provenance"]["status"],"evidence_pending")
 def test_complete_metadata_still_not_validated(self):
  evidence={d:{"reference":"r","reviewer":"human","observed_at":"2026-10-01T00:00:00Z","finding":"review pending"} for d in DOMAINS}
  result=assess({"evidence":evidence})
  self.assertEqual(result["overall"],"requires_independent_validation")
  self.assertFalse(result["validated"])
 def test_future_timestamp_rejected(self):
  result=assess({"evidence":{"provenance":{"reference":"r","reviewer":"h","observed_at":"2099-01-01T00:00:00Z","finding":"x"}}})
  self.assertEqual(result["checks"]["provenance"]["status"],"evidence_pending")
if __name__=="__main__": unittest.main()
