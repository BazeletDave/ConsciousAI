"""Fail-closed evidence gate for PHP2Shell assurance; no vulnerability exploitation."""
REQUIRED = ("affected_version","patched_version","affected_condition_observed","patched_condition_absent","repeat_count","artifact_digest","independent_reviewer")
def evaluate_evidence(record):
    missing=[k for k in REQUIRED if k not in record]
    if missing: return {"status":"pending","reason":"missing_required_evidence","missing":missing}
    if record["affected_version"]!="8.4.26" or record["patched_version"]!="8.4.27":
        return {"status":"pending","reason":"unmatched_version_pair"}
    if not isinstance(record["repeat_count"],int) or isinstance(record["repeat_count"],bool) or record["repeat_count"]<2:
        return {"status":"pending","reason":"insufficient_repeats"}
    if record["affected_condition_observed"] is not True or record["patched_condition_absent"] is not True:
        return {"status":"pending","reason":"vulnerability_condition_not_established"}
    if not isinstance(record["artifact_digest"],str) or len(record["artifact_digest"])!=64:
        return {"status":"pending","reason":"artifact_digest_invalid"}
    if record["independent_reviewer"] is not True:
        return {"status":"condition_comparison_reported","reason":"independent_review_pending"}
    return {"status":"evidence_package_claims_independent_verification","reason":"requires_external_artifact_and_reviewer_authentication"}
