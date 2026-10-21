#!/usr/bin/env python3
"""Offline operational consistency assessment. No security certification."""
import argparse
import json
from pathlib import Path
from php_evidence_verifier import validate_asset, utc, version, THRESHOLDS, SHA, DIGEST

class ConsistencyLevel:
    CONSISTENT="CONSISTENT"
    INCONSISTENT="INCONSISTENT"
    INCOMPLETE="EVIDENCE_INCOMPLETE"
    UNVERIFIED="VERIFICATION_REQUIRED"

def assess(asset):
    aid=asset.get("asset_id","UNKNOWN")
    findings=[]
    r=asset.get("runtime_profile") or {}
    s=asset.get("source_verification") or {}
    image=asset.get("image_integrity") or {}
    worker=asset.get("worker_recycle_evidence") or {}
    val=asset.get("active_runtime_validation") or {}
    auth=asset.get("deployment_authorization") or {}
    provenance=ConsistencyLevel.UNVERIFIED
    commit=s.get("upstream_commit_hash")
    digest=image.get("image_digest_sha256")
    if not (isinstance(commit,str) and SHA.fullmatch(commit) and isinstance(digest,str) and DIGEST.fullmatch(digest)):
        provenance=ConsistencyLevel.INCOMPLETE
        findings.append("Missing or malformed provenance identifiers")
    else:
        findings.append("Provenance identifiers are well-formed, but source and signature authenticity are not independently established")
    runtime=ConsistencyLevel.CONSISTENT
    coverage=ConsistencyLevel.UNVERIFIED
    try:
        declared=version(r.get("php_version"))
        active=version(val.get("in_memory_version_string"))
        if declared!=active:
            runtime=ConsistencyLevel.INCONSISTENT
            findings.append("Runtime Drift: declared and observed version strings disagree")
        if val.get("validation_method") in ("CLI_INSPECTION","HTTP_PHPINFO_ENDPOINT"):
            runtime=ConsistencyLevel.UNVERIFIED if runtime==ConsistencyLevel.CONSISTENT else runtime
            findings.append("Validation method does not establish identity of every serving worker")
        approved=utc(auth.get("approval_timestamp_utc"))
        started=utc(worker.get("process_start_time_utc"))
        tested=utc(val.get("tested_at_utc"))
        if started<approved or tested<started:
            runtime=ConsistencyLevel.INCONSISTENT
            findings.append("Chronological contradiction: authorization, worker start, or test out of order")
        if worker.get("recycle_confirmed") is not True:
            if runtime!=ConsistencyLevel.INCONSISTENT: runtime=ConsistencyLevel.INCOMPLETE
            findings.append("Worker recycle not confirmed")
        if s.get("branch")!=f"PHP-{declared[0]}.{declared[1]}":
            coverage=ConsistencyLevel.INCONSISTENT
            findings.append("Declared branch does not match version")
        elif declared[:2] not in THRESHOLDS:
            coverage=ConsistencyLevel.UNVERIFIED
            findings.append("Branch is not covered by the current version matrix")
        elif declared[2]<THRESHOLDS[declared[:2]]:
            if s.get("vendor_backport_verified") is True:
                coverage=ConsistencyLevel.UNVERIFIED
                findings.append("Vendor backport claimed; vendor advisory and binary evidence not independently verified")
            else:
                coverage=ConsistencyLevel.INCONSISTENT
                findings.append("Coverage Gap: release below reported threshold without verified backport")
        else:
            coverage=ConsistencyLevel.UNVERIFIED
            findings.append("Release meets reported threshold; CVE fix provenance and deployed binary still require verification")
    except (ValueError,TypeError,KeyError) as exc:
        if runtime!=ConsistencyLevel.INCONSISTENT: runtime=ConsistencyLevel.INCOMPLETE
        findings.append(f"Missing or malformed operational evidence: {exc}")
    semantic=validate_asset(asset)
    for msg in semantic:
        if msg not in findings: findings.append(msg)
    if any(x==ConsistencyLevel.INCONSISTENT for x in (provenance,runtime,coverage)):
        overall="CONTRADICTIONS_DETECTED"
    else:
        overall="OPERATIONAL_CONSISTENCY_UNCONFIRMED"
    return {"asset_id":aid,"assessment":overall,
            "consistency_summary":{"provenance":provenance,"runtime":runtime,"patch_coverage":coverage},
            "findings":findings,"independently_attested":False}

def main():
    p=argparse.ArgumentParser()
    p.add_argument("ledger",type=Path)
    args=p.parse_args()
    data=json.loads(args.ledger.read_text(encoding="utf-8"))
    if not isinstance(data,dict) or not isinstance(data.get("assets"),list) or not data["assets"]:
        raise SystemExit("Ledger must contain a nonempty assets array")
    results=[assess(a) for a in data["assets"]]
    print(json.dumps(results,indent=2))
    raise SystemExit(1 if any(r["assessment"]=="CONTRADICTIONS_DETECTED" for r in results) else 0)
if __name__=="__main__":
    main()
