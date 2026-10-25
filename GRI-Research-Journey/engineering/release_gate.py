"""Fail-closed research release assessment; never deploys."""
REQUIRED = ("ci_passed","benchmark_independently_validated","security_review_passed",
"privacy_review_passed","license_review_passed","academic_integrity_review_passed",
"authenticated_approval","staging_rollback_tested","operational_monitoring_verified")
def assess_release(evidence):
    if not isinstance(evidence,dict):
        raise ValueError("evidence must be object")
    missing=[key for key in REQUIRED if evidence.get(key) is not True]
    return {"checks":{key:evidence.get(key) is True for key in REQUIRED},
            "missing":missing,"checklist_complete":not missing,
            "deployment_authorized":False,"deployment_performed":False,
            "notice":"Self-attested flags cannot substitute for authenticated independent review."}
