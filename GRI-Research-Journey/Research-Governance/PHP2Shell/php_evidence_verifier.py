#!/usr/bin/env python3
"""Offline PHP evidence-ledger semantic consistency checker.

Does not establish authenticity of upstream commits, signatures, or audit claims.
"""
import argparse
import json
import re
from datetime import datetime, timezone
from pathlib import Path

THRESHOLDS = {(8,2):35,(8,3):36,(8,4):27,(8,5):12}
SHA = re.compile(r"^[0-9a-f]{40}$")
DIGEST = re.compile(r"^sha256:[0-9a-f]{64}$")
VERSION = re.compile(r"^(\d+)\.(\d+)\.(\d+)(?:[-+][A-Za-z0-9.-]+)?$")

def utc(value):
    if not isinstance(value,str):
        raise ValueError("Missing ISO timestamp")
    dt=datetime.fromisoformat(value.replace("Z","+00:00"))
    if dt.tzinfo is None or dt.utcoffset() is None:
        raise ValueError("Timestamp must have timezone")
    if dt.utcoffset().total_seconds()!=0:
        raise ValueError("Timestamp must be UTC")
    return dt.astimezone(timezone.utc)

def version(value):
    m=VERSION.fullmatch(value) if isinstance(value,str) else None
    if not m:
        raise ValueError("Invalid PHP version")
    return tuple(map(int,m.groups()))

def validate_asset(a):
    errors=[]
    aid=a.get("asset_id","UNKNOWN")
    def err(msg): errors.append(f"[{aid}] {msg}")
    required=("runtime_profile","source_verification","deployment_authorization",
              "image_integrity","worker_recycle_evidence","active_runtime_validation")
    for k in required:
        if not isinstance(a.get(k),dict):
            err(f"Missing object: {k}")
    if errors: return errors
    r,s,auth,img,w,val=(a[k] for k in required)
    commit=s.get("upstream_commit_hash")
    if not isinstance(commit,str) or not SHA.fullmatch(commit):
        err("Missing or malformed upstream commit hash")
    digest=img.get("image_digest_sha256")
    if not isinstance(digest,str) or not DIGEST.fullmatch(digest):
        err("Missing or malformed image digest")
    try:
        configured=version(r.get("php_version"))
        running=version(val.get("in_memory_version_string"))
        if configured!=running: err("Configured and active versions disagree")
        branch=s.get("branch")
        if branch!=f"PHP-{configured[0]}.{configured[1]}":
            err("PHP branch does not match configured version")
        threshold=THRESHOLDS.get(configured[:2])
        if threshold is None: err("Unknown or unsupported version branch")
        elif configured[2]<threshold and s.get("vendor_backport_verified") is not True:
            err("Version below threshold without documented backport")
    except ValueError as e: err(str(e))
    try:
        approved=utc(auth.get("approval_timestamp_utc"))
        started=utc(w.get("process_start_time_utc"))
        tested=utc(val.get("tested_at_utc"))
        if started<approved: err("Worker start precedes authorization")
        if tested<started: err("Runtime test precedes worker start")
    except (ValueError,TypeError) as e: err(f"Invalid chronological evidence: {e}")
    if a.get("audit_classification")=="VERIFIED_AUDITED":
        if s.get("diff_verification_status")!="VERIFIED_AUDITED": err("Unverified source diff")
        if img.get("signature_verified") is not True: err("Image signature not verified")
        if w.get("recycle_confirmed") is not True: err("Worker recycle not confirmed")
        if not auth.get("change_reference") or not auth.get("approved_by"):
            err("Change authorization incomplete")
        if val.get("validation_method")=="CLI_INSPECTION":
            err("CLI inspection alone does not attest to serving worker runtime")
        err("VERIFIED_AUDITED requires independent external attestation; offline evidence is insufficient")
    return errors

def validate_ledger(data):
    if not isinstance(data,dict) or not isinstance(data.get("assets"),list) or not data["assets"]:
        return ["Ledger must contain a nonempty assets array"]
    errors=[]
    for i,a in enumerate(data["assets"]):
        if not isinstance(a,dict): errors.append(f"Asset {i} is not an object")
        else: errors.extend(validate_asset(a))
    return errors

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("ledger",type=Path)
    args=ap.parse_args()
    errors=validate_ledger(json.loads(args.ledger.read_text(encoding="utf-8")))
    print(json.dumps({"result":"FAIL" if errors else "SEMANTIC_CHECKS_PASS_NOT_ATTESTED",
                      "errors":errors},indent=2))
    raise SystemExit(1 if errors else 0)

if __name__=="__main__":
    main()
