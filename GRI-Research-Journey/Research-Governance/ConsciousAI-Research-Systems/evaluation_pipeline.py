"""Reproducible, non-training evaluation of consented numerical research records.

No raw records or identifiers are returned by the public summary endpoint.
No model is promoted automatically; evaluation is only a research diagnostic.
"""
import hashlib
import json
import math

def evaluate_numeric_predictions(rows, *, min_samples=30):
    if not isinstance(rows, list):
        raise ValueError("rows must be a list")
    if not isinstance(min_samples, int) or isinstance(min_samples, bool) or min_samples < 30:
        raise ValueError("min_samples must be at least 30")
    if len(rows) < min_samples:
        return {"status": "insufficient_data", "sample_count": len(rows), "minimum": min_samples,
                "metrics": None, "eligible_for_release": False}
    pairs = []
    for row in rows:
        if not isinstance(row, dict) or set(row) != {"actual", "predicted"}:
            raise ValueError("each row must contain only actual and predicted")
        a, p = row["actual"], row["predicted"]
        if any(isinstance(x, bool) or not isinstance(x, (int, float)) or not math.isfinite(x) for x in (a, p)):
            raise ValueError("nonfinite or nonnumeric prediction")
        pairs.append((float(a), float(p)))
    errors = [p-a for a,p in pairs]
    mae = sum(abs(e) for e in errors) / len(errors)
    rmse = math.sqrt(sum(e*e for e in errors) / len(errors))
    digest = hashlib.sha256(json.dumps(pairs, separators=(",", ":")).encode()).hexdigest()
    return {"status": "evaluated_not_certified", "sample_count": len(pairs),
            "metrics": {"mae": round(mae, 6), "rmse": round(rmse, 6)},
            "evaluation_digest": digest, "eligible_for_release": False,
            "limitations": ["No independent holdout verification", "No fairness or drift analysis",
                            "No dataset consent or provenance attestation"]}

def evaluation_capabilities():
    return {"version": "1.2_candidate", "pipeline": "numeric_prediction_evaluation",
            "status": "available_for_offline_research", "minimum_sample_count": 30,
            "trained_models": 0, "verified_evaluations": 0, "release_automation": False,
            "notice": "Evaluation code is implemented; no real dataset or validated model is asserted."}
