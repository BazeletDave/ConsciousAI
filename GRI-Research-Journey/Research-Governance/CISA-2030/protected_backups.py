"""Offline AES-256-GCM protected SQLite backup/restore; optional cryptography dependency.

No remote upload, identity federation, or Render production integration.
"""
import hashlib
import hmac
import json
import os
import sqlite3
import tempfile
from pathlib import Path
from evidence_ledger import EvidenceLedger

FORMAT = b"GRI-EVIDENCE-V03\n"
MAX_BACKUP = 100 * 1024 * 1024

def _aesgcm():
    try:
        from cryptography.hazmat.primitives.ciphers.aead import AESGCM
    except ImportError as exc:
        raise RuntimeError("Install cryptography to use encrypted backups") from exc
    return AESGCM

def _keys(encryption_key, signing_key):
    if not isinstance(encryption_key, bytes) or len(encryption_key) != 32:
        raise ValueError("AES-256 key must be exactly 32 bytes")
    if not isinstance(signing_key, bytes) or len(signing_key) < 32 or hmac.compare_digest(encryption_key, signing_key):
        raise ValueError("independent signing key of at least 32 bytes required")

def encrypted_backup(ledger, target, encryption_key, signing_key):
    """Consistent snapshot encrypted before it leaves the private temporary directory."""
    _keys(encryption_key, signing_key)
    target = Path(target)
    manifest_path = Path(str(target) + ".manifest")
    if target.exists() or manifest_path.exists():
        raise FileExistsError("backup exists")
    state = ledger.verify()
    if not state["valid"]:
        raise ValueError("ledger integrity failure")
    target.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix="gri-backup-") as directory:
        os.chmod(directory, 0o700)
        staging = Path(directory) / "snapshot.db"
        with sqlite3.connect(str(staging)) as copy:
            ledger.db.backup(copy)
        payload = staging.read_bytes()
        if len(payload) > MAX_BACKUP:
            raise ValueError("backup too large")
        nonce = os.urandom(12)
        encrypted = FORMAT + nonce + _aesgcm()(encryption_key).encrypt(nonce, payload, FORMAT)
        manifest = {"format": "GRI-EVIDENCE-V03", "sha256": hashlib.sha256(encrypted).hexdigest(),
                    "bytes": len(encrypted), "ledger_head": state["head_sha256"], "events": state["events"]}
        signature = hmac.new(signing_key, json.dumps(manifest, sort_keys=True).encode(), hashlib.sha256).hexdigest()
        try:
            with open(target, "xb") as stream:
                os.chmod(target, 0o600)
                stream.write(encrypted)
            with open(manifest_path, "x", encoding="utf-8") as stream:
                os.chmod(manifest_path, 0o600)
                json.dump({"manifest": manifest, "hmac_sha256": signature}, stream, sort_keys=True)
        except Exception:
            target.unlink(missing_ok=True)
            manifest_path.unlink(missing_ok=True)
            raise
        return manifest

def restore_encrypted(source, target, encryption_key, signing_key, role_keys):
    """Restore only to a new path after authentication, decryption and ledger verification."""
    _keys(encryption_key, signing_key)
    source, target = Path(source), Path(target)
    if target.exists():
        raise FileExistsError("restore destination exists")
    wrapper = json.loads(Path(str(source) + ".manifest").read_text())
    manifest = wrapper["manifest"]
    signature = hmac.new(signing_key, json.dumps(manifest, sort_keys=True).encode(), hashlib.sha256).hexdigest()
    if not hmac.compare_digest(signature, wrapper["hmac_sha256"]):
        raise ValueError("manifest authentication failure")
    if source.stat().st_size > MAX_BACKUP + 1024:
        raise ValueError("backup too large")
    encrypted = source.read_bytes()
    if len(encrypted) != manifest["bytes"] or hashlib.sha256(encrypted).hexdigest() != manifest["sha256"] or not encrypted.startswith(FORMAT):
        raise ValueError("backup integrity failure")
    nonce = encrypted[len(FORMAT):len(FORMAT)+12]
    payload = _aesgcm()(encryption_key).decrypt(nonce, encrypted[len(FORMAT)+12:], FORMAT)
    target.parent.mkdir(parents=True, exist_ok=True)
    try:
        with open(target, "xb") as stream:
            os.chmod(target, 0o600)
            stream.write(payload)
        ledger = EvidenceLedger(target, role_keys)
        try:
            state = ledger.verify()
            if not state["valid"] or state["head_sha256"] != manifest["ledger_head"] or state["events"] != manifest["events"]:
                raise ValueError("restored ledger chain mismatch")
            return state
        finally:
            ledger.close()
    except Exception:
        target.unlink(missing_ok=True)
        raise
