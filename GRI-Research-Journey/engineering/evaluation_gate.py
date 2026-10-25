"""Offline research evaluation gates; no training or deployment side effects."""
from math import isfinite

def evaluate_binary(labels, probabilities, *, threshold=0.5, bins=5):
    if len(labels) != len(probabilities) or not labels:
        raise ValueError("nonempty equal-length inputs required")
    if any(type(y) is not int or y not in (0, 1) for y in labels):
        raise ValueError("labels must be binary integers")
    if any(not isinstance(p, (int, float)) or not isfinite(p) or not 0 <= p <= 1 for p in probabilities):
        raise ValueError("probabilities must be finite and in [0,1]")
    if not 0 < threshold < 1 or not isinstance(bins, int) or bins < 2:
        raise ValueError("invalid evaluation configuration")
    predictions = [int(p >= threshold) for p in probabilities]
    accuracy = sum(a == b for a, b in zip(labels, predictions)) / len(labels)
    brier = sum((p - y) ** 2 for p, y in zip(probabilities, labels)) / len(labels)
    return {"n": len(labels), "accuracy": accuracy, "brier_score": brier,
            "publication_authorized": False, "model_promotion_eligible": False,
            "note": "Descriptive evaluation only; requires independent adjudication, held-out benchmark and governance approval."}

def drift_alert(reference, current, *, threshold=0.2):
    if not reference or not current:
        raise ValueError("nonempty samples required")
    if any(not isinstance(v, (int, float)) or not isfinite(v) for v in [*reference, *current]):
        raise ValueError("samples must be finite numeric values")
    if not isfinite(threshold) or threshold <= 0:
        raise ValueError("positive finite threshold required")
    delta = abs(sum(current) / len(current) - sum(reference) / len(reference))
    return {"mean_shift": delta, "alert": delta > threshold,
            "automatic_retraining_allowed": False,
            "note": "Exploratory mean-shift heuristic; not a validated distribution drift detector."}
