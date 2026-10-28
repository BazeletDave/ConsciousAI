"""Offline controlled intake and portable integrity-verified SQLite backups.

Not a production authentication provider, encrypted vault, or network API.
"""
import hashlib
import hmac
import json
import os
import sqlite3
import tempfile
from pathlib import Path
from evidence_ledger import EvidenceLedger
from evidence_validation import DOMAINS, TYPES, timestamp

def intake(ledger, principal, record, artifact):
    """Prevalidate before recording; review must happen separately."""
    if not isinstance(record, dict):
        raise ValueError("record must be object")
    if record.get("domain") not in DOMAINS or record.get("observation_type") not in TYPES:
        raise ValueError("invalid domain or observation type")
    if record.get("scenario_type") != "real":
        raise ValueError("real scenario classification required")
    timestamp(record.get("observed_at"))
    if record.get("outcome") is not True and record.get("outcome") is not False:
        raise ValueError("boolean outcome required")
    if not isinstance(record.get("source_url"), str) or not record["source_url"].startswith("https://"):
        raise ValueError("HTTPS source URL required")
    return ledger.collect(principal, record, artifact)

def export_backup(ledger, target, backup_key):
    """SQLite-consistent snapshot plus HMAC manifest; not encryption."""
    if not isinstance(backup_key, bytes) or len(backup_key) < 32:
        raise ValueError("strong backup signing key required")
    target = Path(target)
    if target.exists() or target.with_suffix(target.suffix + ".manifest").exists():
        raise FileExistsError("refusing to overwrite backup")
    if not ledger.verify()["valid"]:
        raise ValueError("ledger integrity failure")
    target.parent.mkdir(parents=True, exist_ok=True)
    try:
        with sqlite3.connect(str(target)) as copy:
            ledger.db.backup(copy)
        os.chmod(target, 0o600)
        payload = target.read_bytes()
        manifest = {"schema_version": "1.0", "sha256": hashlib.sha256(payload).hexdigest(),
                    "bytes": len(payload), "ledger_head": ledger.verify()["head_sha256"]}
        signature = hmac.new(backup_key, json.dumps(manifest, sort_keys=True).encode(), hashlib.sha256).hexdigest()
        target.with_suffix(target.suffix + ".manifest").write_text(json.dumps({"manifest": manifest, "hmac_sha256": signature}, sort_keys=True))
        os.chmod(target.with_suffix(target.suffix + ".manifest"), 0o600)
        return manifest
    except Exception:
        target.unlink(missing_ok=True)
        target.with_suffix(target.suffix + ".manifest").unlink(missing_ok=True)
        raise

def restore_backup(source, target, backup_key, role_keys):
    """Verify signed manifest, restore to NEW path, validate full ledger chain."""
    source, target = Path(source), Path(target)
    if target.exists():
        raise FileExistsError("restore target must not exist")
    wrapper = json.loads(source.with_suffix(source.suffix + ".manifest").read_text())
    manifest = wrapper["manifest"]
    expected = hmac.new(backup_key, json.dumps(manifest, sort_keys=True).encode(), hashlib.sha256).hexdigest()
    if not hmac.compare_digest(expected, wrapper["hmac_sha256"]):
        raise ValueError("backup manifest signature invalid")
    payload = source.read_bytes()
    if hashlib.sha256(payload).hexdigest() != manifest["sha256"] or len(payload) != manifest["bytes"]:
        raise ValueError("backup integrity failure")
    target.parent.mkdir(parents=True, exist_ok=True)
    try:
        with open(target, "xb") as f:
            f.write(payload)
        os.chmod(target, 0o600)
        ledger = EvidenceLedger(target, role_keys)
        try:
            state = ledger.verify()
            if not state["valid"] or state["head_sha256"] != manifest["ledger_head"]:
                raise ValueError("restored ledger integrity failure")
            return state
        finally:
            ledger.close()
    except Exception:
        target.unlink(missing_ok=True)
        raise
