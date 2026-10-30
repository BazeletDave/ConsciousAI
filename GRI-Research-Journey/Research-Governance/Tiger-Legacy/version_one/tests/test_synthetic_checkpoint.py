"""Checkpoint custody and rotation negative tests; all fixtures synthetic."""
import os
import tempfile
import unittest
from evidence_ledger import EvidenceLedger
from synthetic_checkpoint import SyntheticCheckpointAuthority

class CheckpointTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.ledger = EvidenceLedger(os.path.join(self.tmp.name, "evidence.sqlite"), b"synthetic-ledger-key-32-bytes-minimum")
        self.authority = SyntheticCheckpointAuthority({"k1": b"synthetic-custody-key-one-32-bytes-minimum"}, "k1")
        self.ledger.append("a", {"synthetic": True})

    def test_attested_checkpoint(self):
        self.assertTrue(self.authority.verify(self.authority.attest(self.ledger.checkpoint()), self.ledger))

    def test_detects_truncation(self):
        proof = self.authority.attest(self.ledger.checkpoint())
        empty = EvidenceLedger(os.path.join(self.tmp.name, "empty.sqlite"), b"synthetic-ledger-key-32-bytes-minimum")
        self.assertFalse(self.authority.verify(proof, empty))

    def test_detects_extension_after_checkpoint(self):
        proof = self.authority.attest(self.ledger.checkpoint())
        self.ledger.append("b", {"synthetic": "later"})
        self.assertFalse(self.authority.verify(proof, self.ledger))

    def test_rejects_tampered_head(self):
        proof = self.authority.attest(self.ledger.checkpoint())
        proof["checkpoint"]["head"] = "f" * 64
        self.assertFalse(self.authority.verify(proof, self.ledger))

    def test_key_rotation_keeps_prior_verification(self):
        proof = self.authority.attest(self.ledger.checkpoint())
        self.authority.rotate("k2", b"synthetic-custody-key-two-32-bytes-minimum")
        self.assertTrue(self.authority.verify(proof, self.ledger))
        self.assertTrue(self.authority.verify(self.authority.attest(self.ledger.checkpoint()), self.ledger))

    def test_retirement_revokes_old_attestation(self):
        proof = self.authority.attest(self.ledger.checkpoint())
        self.authority.rotate("k2", b"synthetic-custody-key-two-32-bytes-minimum")
        self.authority.retire("k1")
        self.assertFalse(self.authority.verify(proof, self.ledger))

    def test_wrong_authority(self):
        proof = self.authority.attest(self.ledger.checkpoint())
        other = SyntheticCheckpointAuthority({"k1": b"entirely-different-custody-key-minimum-32"}, "k1")
        self.assertFalse(other.verify(proof, self.ledger))

    def test_malformed_proof(self):
        self.assertFalse(self.authority.verify({"key_id": "k1"}, self.ledger))

    def test_invalid_checkpoint_rejected(self):
        with self.assertRaises(ValueError):
            self.authority.attest({"schema": "gri.tiger_legacy.ledger_checkpoint.v1", "count": -1, "head": "0" * 64})

    def test_reused_key_id_denied(self):
        with self.assertRaises(ValueError):
            self.authority.rotate("k1", b"synthetic-custody-key-two-32-bytes-minimum")

if __name__ == "__main__":
    unittest.main()
