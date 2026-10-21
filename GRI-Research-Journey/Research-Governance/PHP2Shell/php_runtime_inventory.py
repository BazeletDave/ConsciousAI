#!/usr/bin/env python3
"""Offline PHP runtime inventory triage for CVE-2026-109618/109619.

No network calls, vulnerability exploitation, or filesystem scanning.
Vendor backports must be independently verified by the operator.
"""
import json
import re
import sys

FIXED = { (8, 2): 35, (8, 3): 36, (8, 4): 27, (8, 5): 12 }

def assess(asset):
    name = str(asset.get("name", "unnamed"))
    version = str(asset.get("php_version", ""))
    match = re.fullmatch(r"(\d+)\.(\d+)\.(\d+)", version)
    if not match:
        return {"name": name, "status": "manual_review", "reason": "Missing or nonstandard PHP version"}
    major, minor, patch = map(int, match.groups())
    if asset.get("vendor_backport_verified") is True:
        status, reason = "verify_vendor_evidence", "Backport claimed; validate package advisory and installed build"
    elif (major, minor) in FIXED:
        status = "fixed_version_reported" if patch >= FIXED[(major, minor)] else "update_required"
        reason = "Version-only screening; verify actual runtime and package provenance"
    elif major < 8 or (major == 8 and minor < 2):
        status, reason = "unsupported_review", "Unsupported upstream branch; seek vendor fix or upgrade"
    else:
        status, reason = "manual_review", "Unknown branch; consult current PHP vendor advisory"
    return {"name": name, "php_version": version, "internet_facing": bool(asset.get("internet_facing")), "status": status, "reason": reason}

def main():
    if len(sys.argv) != 2:
        raise SystemExit("Usage: python3 php_runtime_inventory.py inventory.json")
    with open(sys.argv[1], encoding="utf-8") as handle:
        data = json.load(handle)
    if not isinstance(data, dict) or not isinstance(data.get("assets"), list):
        raise SystemExit("Expected JSON object containing an assets array")
    print(json.dumps({"results": [assess(a) for a in data["assets"] if isinstance(a, dict)]}, indent=2))

if __name__ == "__main__":
    main()
