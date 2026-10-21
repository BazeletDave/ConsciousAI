#!/usr/bin/env python3
"""CLI for offline PHP evidence-ledger checks. Does not certify remediation."""
import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

from php_evidence_audit import schema_errors
from php_operational_consistency import assess
from php_evidence_verifier import validate_ledger

SCHEMA=Path(__file__).with_name("php_evidence_ledger.schema.json")

def template():
    return {
        "_template_notice": "SYNTHETIC PLACEHOLDERS ONLY. Remove this key and supply real evidence before validation.",
        "ledger_metadata": {
            "ledger_id": "REPLACE_WITH_UUID",
            "schema_version": "1.0.0",
            "generated_at_utc": datetime.now(timezone.utc).isoformat(),
            "auditor": {"name": "REPLACE_WITH_AUDITOR", "email": "replace@example.invalid", "role": "SecOps Engineer"}
        },
        "assets": [{
            "asset_id": "AST-EXAMPLE",
            "hostname": "example.invalid",
            "environment": "staging",
            "runtime_profile": {"php_version": "REPLACE_WITH_OBSERVED_VERSION", "process_manager": "php-fpm", "is_internet_facing": False},
            "source_verification": {"branch": "PHP-8.3", "upstream_commit_hash": "VERIFICATION_REQUIRED",
                "vendor_backport_verified": False, "diff_verification_status": "PENDING_SOURCE_CHECK"},
            "deployment_authorization": {"change_reference": "REPLACE_WITH_CHANGE_ID",
                "approved_by": "replace@example.invalid", "approval_timestamp_utc": "REPLACE_WITH_UTC_TIMESTAMP"},
            "image_integrity": {"image_digest_sha256": "MISSING_IMAGE_DIGEST",
                "registry_uri": "REPLACE_WITH_REGISTRY_REFERENCE", "signature_verified": False},
            "worker_recycle_evidence": {"restart_command": "REPLACE_WITH_APPROVED_ACTION",
                "master_pid": 1, "process_start_time_utc": "REPLACE_WITH_UTC_TIMESTAMP", "recycle_confirmed": False},
            "active_runtime_validation": {"validation_method": "CLI_INSPECTION",
                "in_memory_version_string": "REPLACE_WITH_OBSERVED_VERSION", "tested_at_utc": "REPLACE_WITH_UTC_TIMESTAMP"},
            "audit_classification": "REMEDIATION_INCOMPLETE"
        }]
    }

def evaluate(data, schema):
    problems=schema_errors(data,schema)
    if problems:
        return {"status":"INVALID_LEDGER","schema_errors":problems,"evaluations":[]},2
    semantic=validate_ledger(data)
    evaluations=[assess(a) for a in data["assets"]]
    contradictions=any(x["assessment"]=="CONTRADICTIONS_DETECTED" for x in evaluations)
    status="CONTRADICTIONS_DETECTED" if contradictions else "EVIDENCE_UNVERIFIED"
    if semantic:
        status="CONTRADICTIONS_OR_EVIDENCE_GAPS" if contradictions else "EVIDENCE_INCOMPLETE"
    return {"status":status,"schema_errors":[],"semantic_findings":semantic,
            "evaluations":evaluations,"independently_certified":False},1

def main(argv=None):
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("inventory",nargs="?",type=Path)
    p.add_argument("--format",choices=("table","json"),default="table")
    p.add_argument("--generate-template",action="store_true")
    args=p.parse_args(argv)
    if args.generate_template:
        print(json.dumps(template(),indent=2))
        return 0
    if not args.inventory:
        p.error("inventory JSON file required unless --generate-template is used")
    try:
        data=json.loads(args.inventory.read_text(encoding="utf-8"))
        schema=json.loads(SCHEMA.read_text(encoding="utf-8"))
        report,exit_code=evaluate(data,schema)
    except (OSError,ValueError,TypeError,KeyError) as exc:
        print(f"Input error: {exc}",file=sys.stderr)
        return 2
    if args.format=="json":
        print(json.dumps(report,indent=2))
    else:
        print("PHP Evidence Ledger | "+report["status"])
        print("Offline assessment only; no independent remediation certification.")
        for issue in report.get("schema_errors",[]):
            print("SCHEMA: "+issue)
        for issue in report.get("semantic_findings",[]):
            print("SEMANTIC: "+issue)
        for item in report["evaluations"]:
            print(f"{item['asset_id']}: {item['assessment']}")
            for key,value in item["consistency_summary"].items():
                print(f"  {key}: {value}")
            for finding in item["findings"]:
                print(f"  - {finding}")
    return exit_code

if __name__=="__main__":
    sys.exit(main())
