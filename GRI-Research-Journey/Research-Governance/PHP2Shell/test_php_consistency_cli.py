import json
import unittest
from php_consistency_cli import template, evaluate

class ConsistencyCLITests(unittest.TestCase):
    def test_template_is_explicitly_synthetic(self):
        data=template()
        self.assertIn("_template_notice",data)
        self.assertFalse(data["assets"][0]["image_integrity"]["signature_verified"])
        self.assertEqual(data["assets"][0]["source_verification"]["diff_verification_status"],"PENDING_SOURCE_CHECK")
    def test_schema_failure_returns_nonzero(self):
        report,code=evaluate({"assets":[]},{"type":"object","required":["ledger_metadata"]})
        self.assertEqual(code,2)
        self.assertEqual(report["status"],"INVALID_LEDGER")
    def test_unverified_does_not_exit_zero(self):
        report,code=evaluate({"assets":[{}]},{"type":"object","required":["assets"]})
        self.assertNotEqual(code,0)
        self.assertFalse(report["independently_certified"])
if __name__=="__main__":unittest.main()
