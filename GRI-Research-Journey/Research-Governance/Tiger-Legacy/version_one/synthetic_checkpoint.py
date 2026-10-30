"""Synthetic-only external checkpoint verification and signing key rotation laboratory.

This module does not provide independent custody, HSM protection, or production PKI.
"""
import hashlib
import hmac
from tiger_legacy import canonical

class SyntheticCheckpointAuthority:
    def __init__(self, keys, active_key_id):
        if not isinstance(keys, dict) or not keys:
            raise ValueError("keys required")
        if any(not isinstance(k, str) or not k or not isinstance(v, bytes) or len(v) < 32 for k, v in keys.items()):
            raise ValueError("invalid synthetic key registry")
        if active_key_id not in keys:
            raise ValueError("unknown active key")
        self._keys = dict(keys)
        self._active = active_key_id
        self._retired = set()

    def rotate(self, new_key_id, new_key):
        if not isinstance(new_key_id, str) or not new_key_id or new_key_id in self._keys:
            raise ValueError("key identifier must be new")
        if not isinstance(new_key, bytes) or len(new_key) < 32:
            raise ValueError("minimum 32 byte key")
        self._keys[new_key_id] = new_key
        self._active = new_key_id

    def retire(self, key_id):
        if key_id == self._active or key_id not in self._keys:
            raise ValueError("cannot retire active or unknown key")
        self._retired.add(key_id)

    def attest(self, checkpoint):
        if not isinstance(checkpoint, dict) or checkpoint.get("schema") != "gri.tiger_legacy.ledger_checkpoint.v1":
            raise ValueError("invalid checkpoint schema")
        if type(checkpoint.get("count")) is not int or checkpoint["count"] < 0:
            raise ValueError("invalid count")
        head = checkpoint.get("head")
        if not isinstance(head, str) or len(head) != 64 or any(c not in "0123456789abcdef" for c in head):
            raise ValueError("invalid head")
        payload = {"schema": "gri.tiger_legacy.checkpoint_attestation.v1",
                   "key_id": self._active, "checkpoint": dict(checkpoint)}
        signature = hmac.new(self._keys[self._active], canonical(payload), hashlib.sha256).hexdigest()
        return {**payload, "signature": signature}

    def verify(self, attestation, ledger):
        if not isinstance(attestation, dict) or set(attestation) != {"schema", "key_id", "checkpoint", "signature"}:
            return False
        key_id = attestation["key_id"]
        if not isinstance(key_id, str) or key_id not in self._keys or key_id in self._retired:
            return False
        if attestation["schema"] != "gri.tiger_legacy.checkpoint_attestation.v1":
            return False
        signature = attestation["signature"]
        if not isinstance(signature, str) or len(signature) != 64:
            return False
        payload = {k: v for k, v in attestation.items() if k != "signature"}
        expected = hmac.new(self._keys[key_id], canonical(payload), hashlib.sha256).hexdigest()
        if not hmac.compare_digest(expected, signature):
            return False
        checkpoint = attestation["checkpoint"]
        return isinstance(checkpoint, dict) and ledger.verify(checkpoint=checkpoint)
