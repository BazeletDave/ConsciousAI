"""Offline, read-only synthetic Tiger Legacy report contract. Never performs security actions."""
import hashlib
import json
from pathlib import Path
from tiger_legacy import TigerLegacy, canonical

SCHEMA = "gri.tiger_legacy.synthetic_assurance.v1"

def build_synthetic_report(source_commit="unverified-local-source"):
    lab = TigerLegacy(b"synthetic-only-lab-key-32-bytes-minimum")
    lab.add_resource("resource-a", "alpha", "sample", "alice", "synthetic fixture")
    lab.add_resource("resource-b", "beta", "sample", "bob", "synthetic fixture")
    lab.grant("grant-a", "alpha", "sample", "alice", "viewer", "view", 200)
    decisions = {
        "authorized_before_expiry": lab.authorize("alpha", "sample", "viewer", "view", 199),
        "denied_at_expiry": not lab.authorize("alpha", "sample", "viewer", "view", 200),
        "cross_tenant_denied": not lab.authorize("beta", "sample", "viewer", "view", 199),
    }
    lab.revoke("revoke-a", "alpha", "sample", "alice", "viewer", "view")
    decisions["revoked_denied"] = not lab.authorize("alpha", "sample", "viewer", "view", 100)
    report = {
        "schema_version": SCHEMA,
        "classification": "synthetic_research_only",
        "source_commit": source_commit,
        "model_promoted": False,
        "operational_actions_authorized": 0,
        "production_security": "unmeasured",
        "evidence_integrity": "local_hmac_chain_verified_not_independently_audited" if lab.verify() else "invalid",
        "test_scope": "deterministic_fixture_not_regression_suite",
        "fixture_checks": decisions,
        "fixture_checks_passed": sum(decisions.values()),
        "fixture_checks_total": len(decisions),
        "limitations": [
            "No real authentication, persistence, independent attestation, or client integration.",
            "Fixture checks are not regression suite results or evidence of production security."
        ],
    }
    report["content_sha256"] = hashlib.sha256(canonical(report)).hexdigest()
    return report

def verify_report(report):
    if not isinstance(report, dict):
        raise ValueError("report must be an object")
    digest = report.get("content_sha256")
    payload = {k: v for k, v in report.items() if k != "content_sha256"}
    if not isinstance(digest, str) or hashlib.sha256(canonical(payload)).hexdigest() != digest:
        raise ValueError("report digest mismatch")
    if report.get("schema_version") != SCHEMA or report.get("classification") != "synthetic_research_only":
        raise ValueError("unexpected report classification")
    if report.get("model_promoted") is not False or report.get("operational_actions_authorized") != 0 or report.get("production_security") != "unmeasured":
        raise ValueError("unsafe operational claim")
    if report.get("evidence_integrity") != "local_hmac_chain_verified_not_independently_audited":
        raise ValueError("unverified evidence")
    checks = report.get("fixture_checks")
    if not isinstance(checks, dict) or set(checks) != {"authorized_before_expiry", "denied_at_expiry", "cross_tenant_denied", "revoked_denied"}:
        raise ValueError("invalid fixture checks")
    if any(value is not True for value in checks.values()) or report.get("fixture_checks_passed") != 4 or report.get("fixture_checks_total") != 4:
        raise ValueError("fixture checks failed")
    if not isinstance(report.get("source_commit"), str) or not report["source_commit"]:
        raise ValueError("source commit missing")
    if report.get("test_scope") != "deterministic_fixture_not_regression_suite":
        raise ValueError("scope misrepresented")
    return {k: report[k] for k in (
        "schema_version", "classification", "source_commit", "model_promoted",
        "operational_actions_authorized", "production_security", "evidence_integrity",
        "test_scope", "fixture_checks_passed", "fixture_checks_total", "limitations"
    )}

def read_snapshot(path):
    """Read and validate an existing offline JSON report; no mutation or network."""
    return verify_report(json.loads(Path(path).read_text(encoding="utf-8")))

if __name__ == "__main__":
    print(json.dumps(build_synthetic_report(), sort_keys=True, indent=2))
