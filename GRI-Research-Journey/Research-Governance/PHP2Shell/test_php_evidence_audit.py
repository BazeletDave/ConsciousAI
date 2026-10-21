import unittest
from php_evidence_audit import verify_upstream_commit, verify_cosign, schema_errors

class ExternalEvidenceTests(unittest.TestCase):
    def test_git_fails_closed_without_checkout(self):
        ok,_=verify_upstream_commit("a"*40,None)
        self.assertFalse(ok)
    def test_git_rejects_invalid_hash(self):
        ok,_=verify_upstream_commit("bad",None)
        self.assertFalse(ok)
    def test_cosign_fails_closed_without_key(self):
        ok,_=verify_cosign("registry.example.org/php","sha256:"+"b"*64,None)
        self.assertFalse(ok)
    def test_cosign_rejects_invalid_digest(self):
        ok,_=verify_cosign("registry.example.org/php","fake",None)
        self.assertFalse(ok)
    def test_missing_jsonschema_fails_closed(self):
        import php_evidence_audit as audit
        previous=audit.Draft202012Validator
        try:
            audit.Draft202012Validator=None
            self.assertTrue(schema_errors({},{}))
        finally:
            audit.Draft202012Validator=previous
if __name__=="__main__":unittest.main()
