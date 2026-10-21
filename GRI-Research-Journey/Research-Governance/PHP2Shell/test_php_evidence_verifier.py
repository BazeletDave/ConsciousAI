import copy
import unittest
from php_evidence_verifier import validate_asset, validate_ledger

class LedgerTests(unittest.TestCase):
    def setUp(self):
        self.a={
            "asset_id":"AST-WEB01",
            "runtime_profile":{"php_version":"8.3.36"},
            "source_verification":{"branch":"PHP-8.3","upstream_commit_hash":"a"*40,"vendor_backport_verified":False,"diff_verification_status":"PENDING_SOURCE_CHECK"},
            "deployment_authorization":{"change_reference":"CHG-1","approved_by":"security@example.org","approval_timestamp_utc":"2026-10-21T12:00:00Z"},
            "image_integrity":{"image_digest_sha256":"sha256:"+"b"*64,"signature_verified":False},
            "worker_recycle_evidence":{"process_start_time_utc":"2026-10-21T12:15:00Z","recycle_confirmed":False},
            "active_runtime_validation":{"in_memory_version_string":"8.3.36","tested_at_utc":"2026-10-21T12:20:00Z","validation_method":"CLI_INSPECTION"},
            "audit_classification":"POPULATION_COMPLETE"}
    def test_consistent_record_not_attested(self):
        self.assertEqual(validate_asset(self.a),[])
    def test_reject_false_audit(self):
        a=copy.deepcopy(self.a);a["audit_classification"]="VERIFIED_AUDITED"
        self.assertTrue(any("external attestation" in e for e in validate_asset(a)))
    def test_reject_bad_hash(self):
        a=copy.deepcopy(self.a);a["source_verification"]["upstream_commit_hash"]="fake"
        self.assertTrue(any("commit hash" in e for e in validate_asset(a)))
    def test_reject_version_mismatch(self):
        a=copy.deepcopy(self.a);a["active_runtime_validation"]["in_memory_version_string"]="8.3.35"
        self.assertTrue(any("disagree" in e for e in validate_asset(a)))
    def test_reject_temporal_paradox(self):
        a=copy.deepcopy(self.a);a["worker_recycle_evidence"]["process_start_time_utc"]="2026-10-21T11:00:00Z"
        self.assertTrue(any("precedes" in e for e in validate_asset(a)))
    def test_reject_naive_time(self):
        a=copy.deepcopy(self.a);a["deployment_authorization"]["approval_timestamp_utc"]="2026-10-21T12:00:00"
        self.assertTrue(any("timezone" in e for e in validate_asset(a)))
    def test_reject_unsupported_branch(self):
        a=copy.deepcopy(self.a);a["runtime_profile"]["php_version"]="8.6.0";a["active_runtime_validation"]["in_memory_version_string"]="8.6.0";a["source_verification"]["branch"]="PHP-8.6"
        self.assertTrue(any("Unknown or unsupported" in e for e in validate_asset(a)))
    def test_reject_empty_ledger(self):
        self.assertTrue(validate_ledger({"assets":[]}))
if __name__=="__main__":unittest.main()
