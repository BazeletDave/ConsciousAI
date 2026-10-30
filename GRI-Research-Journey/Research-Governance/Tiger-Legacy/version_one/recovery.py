"""Synthetic backup and recovery verification with an externally retained checkpoint.

A local checkpoint alone cannot protect against privileged rollback of both data and proof.
"""
from pathlib import Path
from evidence_ledger import EvidenceLedger

def verified_recovery(backup_path, recovered_path, ledger_key, attestation, authority):
    source = Path(backup_path).resolve()
    target = Path(recovered_path).resolve()
    if source == target or not source.is_file() or target.exists():
        raise ValueError("invalid recovery paths; destination must not exist")
    backup = EvidenceLedger(source, ledger_key)
    if not authority.verify(attestation, backup):
        raise PermissionError("backup checkpoint validation failed")
    backup.backup(target)
    try:
        restored = EvidenceLedger(target, ledger_key)
        if not authority.verify(attestation, restored):
            raise PermissionError("restored evidence validation failed")
        return restored.checkpoint()
    except Exception:
        target.unlink(missing_ok=True)
        raise
