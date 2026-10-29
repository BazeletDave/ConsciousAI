"""Read-only synthetic Tiger Legacy reporting. No operational authority."""
import hashlib
import json
from pathlib import Path

SNAPSHOT = "tiger_legacy_synthetic_snapshot.json"
MANIFEST = "tiger_legacy_trust_manifest.json"
SCHEMA = "gri.tiger_legacy.synthetic_assurance.v1"

def snapshot(root):
    root = Path(root)
    manifest = json.loads((root / MANIFEST).read_text(encoding="utf-8"))
    if (manifest.get("schema_version") != "gri.tiger_legacy.trust_manifest.v1"
            or manifest.get("classification") != "research_only_repository_pinned_digest"
            or manifest.get("snapshot_file") != SNAPSHOT):
        raise ValueError("invalid trusted manifest")
    expected = manifest.get("snapshot_sha256")
    if not isinstance(expected, str) or len(expected) != 64:
        raise ValueError("invalid pinned digest")
    raw = (root / SNAPSHOT).read_bytes()
    if hashlib.sha256(raw).hexdigest() != expected:
        raise ValueError("pinned snapshot integrity failure")
    report = json.loads(raw)
    digest = report.get("content_sha256")
    payload = {k: v for k, v in report.items() if k != "content_sha256"}
    canonical = json.dumps(payload, sort_keys=True, separators=(",", ":"), allow_nan=False).encode()
    if hashlib.sha256(canonical).hexdigest() != digest:
        raise ValueError("internal report digest failure")
    if report.get("schema_version") != SCHEMA or report.get("classification") != "synthetic_research_only":
        raise ValueError("incorrect classification")
    if (report.get("model_promoted") is not False
            or report.get("operational_actions_authorized") != 0
            or report.get("production_security") != "unmeasured"
            or report.get("test_scope") != "deterministic_fixture_not_regression_suite"
            or report.get("evidence_integrity") != "local_hmac_chain_verified_not_independently_audited"):
        raise ValueError("invalid safety claims")
    checks = report.get("fixture_checks")
    if (not isinstance(checks, dict)
            or set(checks) != {"authorized_before_expiry", "cross_tenant_denied", "denied_at_expiry", "revoked_denied"}
            or any(value is not True for value in checks.values())
            or report.get("fixture_checks_total") != 4 or report.get("fixture_checks_passed") != 4):
        raise ValueError("fixture failure")
    return {k: report[k] for k in (
        "schema_version", "classification", "source_commit", "model_promoted",
        "operational_actions_authorized", "production_security", "evidence_integrity",
        "test_scope", "fixture_checks_passed", "fixture_checks_total", "limitations"
    )} | {"integrity_status": "repository_pinned_snapshot_digest_checked_not_independent_attestation"}
