import unittest
from php_assurance_evidence_gate import evaluate_evidence
class EvidenceGateTests(unittest.TestCase):
    def test_empty_fails_closed(self): self.assertEqual(evaluate_evidence({})["status"],"pending")
    def test_version_mismatch(self):
        r=self.valid();r["patched_version"]="8.4.26"
        self.assertEqual(evaluate_evidence(r)["reason"],"unmatched_version_pair")
    def test_no_vulnerable_condition(self):
        r=self.valid();r["affected_condition_observed"]=False
        self.assertEqual(evaluate_evidence(r)["status"],"pending")
    def test_no_independent_review(self):
        r=self.valid();r["independent_reviewer"]=False
        self.assertEqual(evaluate_evidence(r)["status"],"condition_comparison_reported")
    def test_claim_not_certification(self):
        self.assertEqual(evaluate_evidence(self.valid())["status"],"evidence_package_claims_independent_verification")
    @staticmethod
    def valid():
        return dict(affected_version="8.4.26",patched_version="8.4.27",affected_condition_observed=True,patched_condition_absent=True,repeat_count=2,artifact_digest="a"*64,independent_reviewer=True)
if __name__=="__main__":unittest.main()
