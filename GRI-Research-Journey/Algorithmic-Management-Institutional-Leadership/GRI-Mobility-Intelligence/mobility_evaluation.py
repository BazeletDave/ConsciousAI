"""Issue 13: reproducible synthetic-only rolling-origin forecast and policy evaluation.

Quantile residual intervals are calibrated on strictly prior observations; no prospective
performance or real-world coverage claims. Offline standard library only.
"""
from math import ceil, isfinite
from mobility_core import compare_strategies, evaluate_scenario

def _values(history):
    if not isinstance(history, list) or len(history) < 8:
        raise ValueError("at least eight chronological observations required")
    if any(type(x) not in (int, float) or not isfinite(x) or x < 0 for x in history):
        raise ValueError("history must contain finite nonnegative numbers")
    return [float(x) for x in history]

def _quantile(values, coverage):
    ordered = sorted(values)
    return ordered[min(len(ordered) - 1, max(0, ceil((len(ordered) + 1) * coverage) - 1))]

def temporal_evaluation(history, train_size=4, calibration_size=2, coverage=0.8):
    """Train, calibration, and holdout are chronological and disjoint."""
    values = _values(history)
    if type(train_size) is not int or type(calibration_size) is not int or train_size < 2 or calibration_size < 2:
        raise ValueError("invalid split")
    if train_size + calibration_size >= len(values):
        raise ValueError("nonempty temporal holdout required")
    if not 0 < coverage < 1:
        raise ValueError("coverage must be between zero and one")
    train = values[:train_size]
    calibration = values[train_size:train_size + calibration_size]
    holdout = values[train_size + calibration_size:]
    center = sum(train) / len(train)
    residuals = [abs(x - center) for x in calibration]
    radius = _quantile(residuals, coverage)
    low, high = max(0, center - radius), center + radius
    baseline = train[-1]
    model_errors = [abs(x - center) for x in holdout]
    baseline_errors = [abs(x - baseline) for x in holdout]
    covered = sum(low <= x <= high for x in holdout)
    return {
        "splits": {"train": train_size, "calibration": calibration_size, "holdout": len(holdout)},
        "forecast": round(center, 4),
        "interval": [round(low, 4), round(high, 4)],
        "nominal_coverage": coverage,
        "holdout_coverage": round(covered / len(holdout), 4),
        "holdout_mae": round(sum(model_errors) / len(holdout), 4),
        "last_value_rules_baseline_mae": round(sum(baseline_errors) / len(holdout), 4),
        "ood": {
            "outside_training_range": sum(x < min(train) or x > max(train) for x in holdout),
            "holdout_count": len(holdout),
        },
        "limitations": "Synthetic retrospective split. Residual quantile assumes exchangeability; temporal drift can invalidate coverage. No prospective validation."
    }

def compare_policy_cases(cases, constraints):
    """Compare constrained selection with a deterministic gross-only rules baseline."""
    if not isinstance(cases, dict) or not cases:
        raise ValueError("named cases required")
    chosen = compare_strategies(cases, constraints)
    feasible = {k: evaluate_scenario(v, constraints)["drive"] for k, v in cases.items()}
    eligible = [k for k, result in feasible.items() if result["feasible"]]
    baseline = max(eligible, key=lambda k: cases[k]["gross"]) if eligible else "no_drive"
    return {
        "constrained_selection": chosen["selected"],
        "gross_only_feasible_baseline": baseline,
        "constrained_estimated_net": 0 if chosen["selected"] == "no_drive" else feasible[chosen["selected"]]["estimated_net"],
        "baseline_estimated_net": 0 if baseline == "no_drive" else feasible[baseline]["estimated_net"],
        "all_hard_constraints_enforced": True,
        "status": "Synthetic offline policy comparison only; no earnings improvement claim"
    }
