"""GRI release assurance gate: evidence-based, fail-closed readiness classification.
This is an internal readiness control, NOT independent certification.
"""
import argparse
import datetime as dt
import json
from pathlib import Path

REQUIRED = (
    "ci_tests_passed", "deployment_health_verified", "durable_database_verified",
    "backup_restore_test_passed", "signing_key_custody_verified",
    "external_checkpoint_verified", "source_provenance_verified",
    "production_ml_validation_verified", "security_review_approved",
    "independent_assessor_approved",
)
def assess(evidence):
    controls=evidence.get("controls",{})
    results={}
    for key in REQUIRED:
        item=controls.get(key,{})
        valid=(isinstance(item,dict) and item.get("passed") is True
               and isinstance(item.get("evidence_uri"),str)
               and item["evidence_uri"].startswith(("https://","urn:sha256:"))
               and isinstance(item.get("reviewer"),str) and bool(item["reviewer"].strip())
               and isinstance(item.get("verified_at_utc"),str) and bool(item["verified_at_utc"].strip()))
        results[key]={"verified":valid}
    ready=all(x["verified"] for x in results.values())
    return {"classification":"internal_release_ready_for_external_certification_review" if ready else "production_certification_pending",
            "certified":False,"verified_controls":sum(x["verified"] for x in results.values()),
            "total_controls":len(REQUIRED),"controls":results,
            "notice":"This internal gate cannot grant third-party certification."}

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("--evidence",default="production_assurance_evidence.json")
    parser.add_argument("--require-ready",action="store_true")
    args=parser.parse_args()
    evidence=json.loads(Path(args.evidence).read_text(encoding="utf-8"))
    report=assess(evidence)
    print(json.dumps(report,indent=2,sort_keys=True))
    if args.require_ready and report["classification"]!="internal_release_ready_for_external_certification_review":
        raise SystemExit(1)
if __name__=="__main__":
    main()
