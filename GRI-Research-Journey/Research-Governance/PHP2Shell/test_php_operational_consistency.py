import copy
import unittest
from php_operational_consistency import assess

class OperationalConsistencyTests(unittest.TestCase):
    def setUp(self):
        self.asset={
            "asset_id":"AST-WEB01",
            "runtime_profile":{"php_version":"8.3.36"},
            "source_verification":{"branch":"PHP-8.3","upstream_commit_hash":"a"*40,"vendor_backport_verified":False,"diff_verification_status":"PENDING_SOURCE_CHECK"},
            "deployment_authorization":{"change_reference":"CHG-1","approved_by":"secops@example.org","approval_timestamp_utc":"2026-10-21T12:00:00Z"},
            "image_integrity":{"image_digest_sha256":"sha256:"+"b"*64,"signature_verified":True},
            "worker_recycle_evidence":{"process_start_time_utc":"2026-10-21T12:15:00Z","recycle_confirmed":True},
            "active_runtime_validation":{"validation_method":"CLI_INSPECTION","in_memory_version_string":"8.3.36","tested_at_utc":"2026-10-21T12:20:00Z"},
            "audit_classification":"POPULATION_COMPLETE"}
    def test_consistent_synthetic_not_attested(self):
        r=assess(self.asset)
        self.assertEqual(r["assessment"],"OPERATIONAL_CONSISTENCY_UNCONFIRMED")
        self.assertFalse(r["independently_attested"])
    def test_runtime_drift(self):
        a=copy.deepcopy(self.asset)
        a["active_runtime_validation"]["in_memory_version_string"]="8.3.35"
        self.assertEqual(assess(a)["assessment"],"CONTRADICTIONS_DETECTED")
    def test_chronology(self):
        a=copy.deepcopy(self.asset)
        a["worker_recycle_evidence"]["process_start_time_utc"]="2026-10-21T11:00:00Z"
        self.assertEqual(assess(a)["assessment"],"CONTRADICTIONS_DETECTED")
    def test_unsupported_branch_not_safe(self):
        a=copy.deepcopy(self.asset)
        a["runtime_profile"]["php_version"]="8.6.0"
        a["active_runtime_validation"]["in_memory_version_string"]="8.6.0"
        a["source_verification"]["branch"]="PHP-8.6"
        self.assertNotEqual(assess(a)["consistency_summary"]["patch_coverage"],"CONSISTENT")
    def test_missing_provenance(self):
        a=copy.deepcopy(self.asset)
        a["source_verification"]["upstream_commit_hash"]="VERIFICATION_REQUIRED"
        self.assertEqual(assess(a)["consistency_summary"]["provenance"],"EVIDENCE_INCOMPLETE")
if __name__=="__main__":
    unittest.main()
