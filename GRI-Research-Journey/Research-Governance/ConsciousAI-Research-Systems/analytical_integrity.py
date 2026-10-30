"""Fail-closed, read-only analytical output provenance audit. No certification implied."""
from __future__ import annotations
from urllib.parse import urlparse

FRAMEWORK = {
    "id": "nelson_institutional_political_economy",
    "attribution": "Roy C. Nelson, Thunderbird School of Global Management teaching context",
    "application": "GRI independent analytical application; not faculty or institutional endorsement",
    "lenses": ["liberalism", "economic_nationalism", "structuralism"],
    "status": "proposed_interpretive_lens_not_record_level_assessment",
}
CRITERIA = ("source_evidence", "academic_attribution", "fact_inference_separation", "limitations", "review_accountability")
VERIFIED_STATUSES = {"verified", "independently_verified", "official_event_listing_verified"}

def _external(url):
    return isinstance(url, str) and urlparse(url).scheme == "https" and bool(urlparse(url).netloc)

def assess_record(record, family):
    """Preserve source classification; never infer independent verification from a label or URL."""
    raw_status = record.get("verification_status") or "unspecified"
    source = record.get("primary_source_url") or record.get("source")
    evidence = {
        "source_reference": source if isinstance(source, str) and source.strip() else None,
        "source_kind": "external_url" if _external(source) else ("repository_path" if source else "missing"),
        "publication_date": record.get("publication_date") or record.get("event_date"),
        "retrieved_at": record.get("retrieved_at"),
        "document_locator": record.get("document_locator"),
        "independent_verification": record.get("independent_verification", False) is True,
        "verification_status_reported": raw_status,
    }
    # Model attribution must be explicit per record. Global research context is not attribution.
    attribution = record.get("academic_framework")
    if not isinstance(attribution, dict) or not attribution.get("id") or not attribution.get("attribution"):
        attribution = None
    claim_type = record.get("claim_type")
    limitations = record.get("limitations")
    review = record.get("review_status")
    reviewer = record.get("reviewer_id")
    checks = {
        "source_evidence": bool(evidence["source_reference"] and evidence["publication_date"] and evidence["retrieved_at"] and evidence["document_locator"]),
        "academic_attribution": bool(attribution),
        "fact_inference_separation": claim_type in {"observed_fact", "reported_claim", "analytical_inference", "hypothesis", "forecast"},
        "limitations": isinstance(limitations, str) and bool(limitations.strip()),
        "review_accountability": bool(review and reviewer and record.get("reviewed_at")),
    }
    independent = evidence["independent_verification"]
    declared_verified = raw_status in VERIFIED_STATUSES or str(raw_status).endswith("_verified")
    eligible = all(checks.values()) and independent and review == "approved" and declared_verified
    # An official event listing may verify the existence of a listing, not the claims within it.
    if family == "events" and raw_status == "official_event_listing_verified":
        eligible = False
    missing = [key for key in CRITERIA if not checks[key]]
    if not independent:
        missing.append("independent_verification")
    if declared_verified and not eligible:
        classification = "verified_claim_blocked_pending_evidence"
    else:
        classification = "eligible_for_verified_claim" if eligible else "not_verified"
    return {
        "id": record.get("id"), "family": family,
        "claim": record.get("claim") or record.get("summary") or record.get("title"),
        "evidence": evidence,
        "academic_framework": attribution,
        "institutional_context_framework": FRAMEWORK,
        "claim_type": claim_type or "unclassified",
        "limitations": limitations or "Not documented in this record.",
        "review": {"status": review or "not_documented", "reviewer_id": reviewer, "reviewed_at": record.get("reviewed_at")},
        "criteria": checks, "missing_requirements": missing,
        "classification": classification,
        "certified": False,
        "notice": "Record assessment is not an independent audit, causal finding, or academic endorsement.",
    }

def audit_inventory(cases, events, policies):
    assessed = [assess_record(record, family) for family, records in
                (("cases", cases), ("events", events), ("policies", policies)) for record in records]
    return {
        "schema_version": "1.0",
        "assessment_type": "complete_local_registry_record_audit",
        "criteria": list(CRITERIA),
        "total_records": len(assessed),
        "criteria_pass_counts": {key: sum(x["criteria"][key] for x in assessed) for key in CRITERIA},
        "verified_eligible_count": sum(x["classification"] == "eligible_for_verified_claim" for x in assessed),
        "blocked_verified_claims": sum(x["classification"] == "verified_claim_blocked_pending_evidence" for x in assessed),
        "certification": "withheld_pending_independent_review_and_live_payload_validation",
        "scope": "cases.json, events.json, policies.json; not every dashboard data source",
        "records": assessed,
    }
