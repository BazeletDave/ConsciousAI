"""GRI model governance registry: explicit evaluation and release gates, no trained model claims."""
from __future__ import annotations
from datetime import datetime, timezone

MODEL_CATALOG = (
    {"id": "enrollment-discovery-tfidf", "domain": "institutional",
     "method": "adaptive_publisher_title_tfidf_cosine", "status": "scheduled_metadata_adaptation",
     "trained": False, "fitted_feature_index": True, "evaluation": None,
     "endpoint": "/intelligence/enrollment-research", "fraud_classifier": False},
    {"id": "enrollment-document-tfidf", "domain": "institutional",
     "method": "corpus_fitted_tfidf_cosine", "status": "research_retrieval",
     "trained": False, "fitted_feature_index": True, "evaluation": None,
     "endpoint": "/intelligence/enrollment-research", "fraud_classifier": False},
    {"id": "mobility-offer-forecast", "domain": "mobility", "method": "supervised_regression",
     "status": "design", "trained": False, "evaluation": None},
    {"id": "governance-risk-anomaly", "domain": "governance", "method": "anomaly_detection",
     "status": "design", "trained": False, "evaluation": None},
    {"id": "institutional-document-rag", "domain": "institutional", "method": "retrieval_augmented_generation",
     "status": "design", "trained": False, "evaluation": None},
    {"id": "cyber-evidence-triage", "domain": "cyber", "method": "evidence_classification",
     "status": "design", "trained": False, "evaluation": None},
)

def evaluate_release(candidate):
    """Conservative fail-closed governance gate; a pass is not independent certification."""
    required = ("model_id", "version", "dataset_digest", "evaluation_digest",
                "owner", "reviewer", "reviewed_at", "human_approved",
                "holdout_samples", "metric_name", "metric_value", "metric_threshold",
                "privacy_review", "security_review", "provenance_verified")
    missing = [k for k in required if k not in candidate]
    if missing:
        return {"eligible": False, "reasons": ["missing:" + ",".join(missing)]}
    reasons = []
    for field in ("dataset_digest", "evaluation_digest"):
        val = candidate[field]
        if not isinstance(val, str) or len(val) != 64 or any(c not in "0123456789abcdef" for c in val):
            reasons.append("invalid_" + field)
    if not isinstance(candidate["holdout_samples"], int) or isinstance(candidate["holdout_samples"], bool) or candidate["holdout_samples"] < 30:
        reasons.append("insufficient_holdout")
    from math import isfinite
    value, threshold = candidate["metric_value"], candidate["metric_threshold"]
    if any(isinstance(x, bool) or not isinstance(x, (int, float)) or not isfinite(x) for x in (value, threshold)):
        reasons.append("invalid_metric")
    elif value < threshold:
        reasons.append("metric_below_threshold")
    for field in ("human_approved", "privacy_review", "security_review", "provenance_verified"):
        if candidate[field] is not True:
            reasons.append("required_gate_" + field)
    if candidate["owner"] == candidate["reviewer"]:
        reasons.append("independent_reviewer_required")
    try:
        reviewed = datetime.fromisoformat(candidate["reviewed_at"].replace("Z", "+00:00"))
        if reviewed.tzinfo is None or reviewed > datetime.now(timezone.utc):
            reasons.append("invalid_review_time")
    except (ValueError, AttributeError, TypeError):
        reasons.append("invalid_review_time")
    return {"eligible": not reasons, "reasons": reasons,
            "notice": "Engineering gate only; separate release authorization and audit required."}

def platform_capabilities():
    return {"schema_version": "1.1", "release_label": "v1.1_candidate",
            "mode": "research_prototype_read_only", "models": list(MODEL_CATALOG),
            "registered_models": len(MODEL_CATALOG), "trained_models": 0,
            "model_promotion": "requires_independent_review",
            "applications": ["mobility", "governance", "institutional", "cyber"],
            "notice": "Predictive models remain planned. Enrollment document retrieval fits a TF IDF feature index to reviewed public summaries; independent retrieval evaluation is pending."}
