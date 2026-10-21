#!/usr/bin/env python3
"""Offline PHP case study and inventory triage. No probing or exploitation."""
import argparse
import json
import re
from datetime import datetime
from pathlib import Path

FIXED = {(8, 2): 35, (8, 3): 36, (8, 4): 27, (8, 5): 12}
CVE = ["CVE-2026-109618", "CVE-2026-109619"]

def classify(version, backport_evidence=None):
    if not isinstance(version, str) or not re.fullmatch(r"\d+\.\d+\.\d+", version):
        return "unknown_version"
    major, minor, patch = map(int, version.split("."))
    if backport_evidence:
        return "vendor_verification_required"
    if (major, minor) in FIXED:
        return "update_required" if patch < FIXED[(major, minor)] else "fixed_version_reported"
    if major < 8 or (major == 8 and minor < 2):
        return "unsupported_review"
    return "unknown_branch_review"

def _audit_status(asset):
    fields = ("image_digest", "responsible_owner", "patch_authorization")
    populated = all(isinstance(asset.get(k), str) and asset[k].strip() for k in fields)
    if not populated:
        return "incomplete_record"
    evidence = ("audit_reference", "audit_timestamp", "audit_verifier")
    documented = (asset.get("independently_audited") is True
                  and all(isinstance(asset.get(k), str) and asset[k].strip() for k in evidence))
    if documented:
        try:
            datetime.fromisoformat(asset["audit_timestamp"].replace("Z", "+00:00"))
        except ValueError:
            documented = False
    return "audit_evidence_recorded" if documented else "population_complete"

def analyze(data):
    if not isinstance(data, dict) or not isinstance(data.get("assets"), list):
        raise ValueError("Input must contain an assets array")
    out = []
    for asset in data["assets"]:
        if not isinstance(asset, dict):
            raise ValueError("Each asset must be an object")
        version = asset.get("php_version")
        status = classify(version, asset.get("vendor_backport_evidence"))
        exposed = asset.get("internet_facing")
        if type(exposed) is not bool:
            exposed = None
        criticality = asset.get("criticality", "unknown")
        if criticality not in ("low", "medium", "high", "critical", "unknown"):
            criticality = "unknown"
        priority = ("urgent_review" if status == "update_required" and exposed is True else
                    "review" if status != "fixed_version_reported" else "verify_deployment")
        out.append({
            "name": str(asset.get("name") or "UNNAMED_ASSET"),
            "php_version": version, "status": status,
            "internet_facing": exposed, "criticality": criticality,
            "priority": priority,
            "image_digest": asset.get("image_digest"),
            "worker_type": asset.get("worker_type"),
            "responsible_owner": asset.get("responsible_owner"),
            "patch_authorization": asset.get("patch_authorization"),
            "backport_evidence": asset.get("vendor_backport_evidence"),
            "record_status": _audit_status(asset),
            "audit_reference": asset.get("audit_reference"),
            "audit_timestamp": asset.get("audit_timestamp"),
            "audit_verifier": asset.get("audit_verifier"),
            "note": "Offline screening only; audit metadata is not proof of verification or remediation."
        })
    return out

def render_markdown(results):
    lines = ["# PHP Shared Runtime Vulnerabilities: Inventory Case Study",
             "", "Grand Research Institute | Research date: 2026-10-21", "",
             "## How it happened", "Reported PHP memory and lifecycle handling defects require examination of upstream patches and regression tests. Mechanistic assertions must be corroborated against source code.", "",
             "## What happened", "Security releases and advisories prompted emergency remediation. Potential exposure, attempted exploitation, confirmed exploitation and compromise must be reported separately.", "",
             "## What it impacts", "Potential server execution, integrity and confidentiality impacts depend on configuration, exploit prerequisites and installed runtime.", "",
             "## Where it impacts", "Shared PHP dependencies can affect CMS applications, hosting providers and public sector services. Platform dependence alone is not evidence of compromise.", "",
             "## Inventory findings", "| Asset | Version | Exposure | Criticality | Classification | Priority | Record status |",
             "| --- | --- | --- | --- | --- | --- | --- |"]
    for r in results:
        fields = [r["name"], r["php_version"], r["internet_facing"], r["criticality"], r["status"], r["priority"], r["record_status"]]
        lines.append("| " + " | ".join(str(v).replace("|", "\\|").replace("\n", " ") for v in fields) + " |")
    lines += ["", "## Where we go from here", "1. Confirm upstream advisory and vendor patch provenance.",
              "2. Inventory all PHP runtimes and embedded dependencies.",
              "3. Prioritize exposed critical services and authorize remediation.",
              "4. Restart or redeploy affected workers according to platform procedures.",
              "5. Verify active patched runtime and retain evidence.",
              "6. Measure disclosure to remediation and remediation to verification latency.", "",
              "## Evidence boundaries", "This offline screening is not a live security audit, exploit test, proof of compromise or independently validated remediation.", "",
              "## References", "- https://www.php.net/",
              "- https://www.cyber.gc.ca/en/alerts-advisories/al26-026-critical-vulnerabilities-impacting-php-cve-2026-109618-cve-2026-109619",
              "- https://github.com/NCSC-NL/php2shell"]
    return "\n".join(lines) + "\n"

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("inventory", type=Path, help="Required JSON asset inventory; no synthetic defaults")
    parser.add_argument("--report", type=Path)
    args = parser.parse_args()
    data = json.loads(args.inventory.read_text(encoding="utf-8"))
    results = analyze(data)
    report = {"case": "PHP shared runtime vulnerabilities", "cves": CVE, "results": results}
    print(json.dumps(report, indent=2))
    if args.report:
        args.report.write_text(render_markdown(results), encoding="utf-8")

if __name__ == "__main__":
    main()
