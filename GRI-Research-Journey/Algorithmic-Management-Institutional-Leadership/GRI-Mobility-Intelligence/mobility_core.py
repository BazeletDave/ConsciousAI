"""Offline, synthetic-first GRI Mobility Intelligence research utilities. No platform access."""
from datetime import datetime, timedelta
from math import isfinite

def _number(value, name):
    if isinstance(value, bool) or not isinstance(value, (int, float)) or not isfinite(value) or value < 0:
        raise ValueError(f"{name} must be finite and nonnegative")
    return float(value)

def parse_time(value):
    if not isinstance(value, str):
        raise ValueError("timestamp must be ISO 8601 string")
    dt = datetime.fromisoformat(value)
    if dt.tzinfo is None or dt.utcoffset() is None:
        raise ValueError("timezone offset required")
    return dt

def validate_record(record):
    """Validate a non-identifying, opt-in research record; never ingest passenger PII."""
    allowed = {"record_id", "consent_id", "consent_active", "synthetic", "event_type", "start", "end", "gross", "tips", "incentives", "incentives_in_gross", "paid_miles", "unpaid_miles", "cost_per_mile", "tolls", "source"}
    if not isinstance(record, dict) or set(record) - allowed:
        raise ValueError("unknown fields or invalid record")
    required = {"record_id", "consent_id", "consent_active", "synthetic", "event_type", "start", "end", "gross", "tips", "incentives", "incentives_in_gross", "paid_miles", "unpaid_miles", "cost_per_mile", "tolls", "source"}
    if not required <= set(record):
        raise ValueError("missing required fields")
    if not isinstance(record["record_id"], str) or not record["record_id"] or not isinstance(record["source"], str) or not record["source"]:
        raise ValueError("record id and source required")
    if not isinstance(record["consent_id"], str) or not record["consent_id"] or record["consent_active"] is not True:
        raise ValueError("active, documented consent required")
    if type(record["synthetic"]) is not bool or type(record["incentives_in_gross"]) is not bool:
        raise ValueError("boolean flags required")
    if record["event_type"] not in ("OFFER", "OFFER_ACCEPTED", "TRIP_COMPLETED", "PAYMENT_SETTLED", "OFFER_DECLINED"):
        raise ValueError("invalid event type")
    if parse_time(record["end"]) < parse_time(record["start"]):
        raise ValueError("end precedes start")
    for key in ("gross", "tips", "incentives", "paid_miles", "unpaid_miles", "cost_per_mile", "tolls"):
        _number(record[key], key)
    if record["event_type"] == "OFFER_DECLINED" and (record["gross"] or record["tips"] or record["tolls"]):
        raise ValueError("declined offers have no realized payout or trip toll")
    return True

def net_contribution(record):
    validate_record(record)
    if record["event_type"] not in ("TRIP_COMPLETED", "PAYMENT_SETTLED"):
        raise ValueError("not a realized trip")
    incentive = 0 if record["incentives_in_gross"] else record["incentives"]
    return round(record["gross"] + record["tips"] + incentive - (record["paid_miles"] + record["unpaid_miles"]) * record["cost_per_mile"] - record["tolls"], 2)

def evaluate_scenario(scenario, constraints):
    """Compare a manually supplied hypothetical itinerary with no-drive. Hard exclusions prevail."""
    required = ("start", "end", "return_by", "next_commitment", "minimum_sleep_hours", "max_duty_hours", "gross", "miles", "cost_per_mile", "tolls", "uncertainty")
    if not all(k in scenario for k in required):
        raise ValueError("scenario incomplete")
    start, end = parse_time(scenario["start"]), parse_time(scenario["end"])
    deadline, commitment = parse_time(scenario["return_by"]), parse_time(scenario["next_commitment"])
    sleep = _number(scenario["minimum_sleep_hours"], "minimum_sleep_hours")
    duty = _number(scenario["max_duty_hours"], "max_duty_hours")
    for key in ("gross", "miles", "cost_per_mile", "tolls", "uncertainty"):
        _number(scenario[key], key)
    if not isinstance(constraints, dict) or not isinstance(constraints.get("blocked_intervals"), list):
        raise ValueError("blocked intervals required")
    violations = []
    if end < start or end > deadline:
        violations.append("return deadline or chronology")
    if end - start > timedelta(hours=duty):
        violations.append("duty limit")
    if commitment - end < timedelta(hours=sleep):
        violations.append("sleep opportunity")
    for block in constraints["blocked_intervals"]:
        bstart, bend = parse_time(block["start"]), parse_time(block["end"])
        if start < bend and bstart < end:
            violations.append("protected schedule block")
    net = round(scenario["gross"] - scenario["miles"] * scenario["cost_per_mile"] - scenario["tolls"], 2)
    return {"no_drive": {"feasible": True, "estimated_net": 0.0},
            "drive": {"feasible": not violations, "violations": violations,
                      "estimated_net": net, "uncertainty": scenario["uncertainty"],
                      "recommended": not violations and net - scenario["uncertainty"] > 0},
            "notice": "Offline hypothetical scenario, not live demand or guaranteed earnings"}

def baseline_forecast(history, horizon_index):
    """Leakage-safe trailing mean baseline; history must be chronological and predate horizon."""
    if not isinstance(horizon_index, int) or horizon_index < 2 or horizon_index > len(history):
        raise ValueError("insufficient historical observations")
    train = history[:horizon_index]
    for value in train:
        _number(value, "history")
    mean = sum(train) / len(train)
    absolute_errors = [abs(train[i] - sum(train[:i]) / i) for i in range(1, len(train))]
    uncertainty = max(absolute_errors) if absolute_errors else 0.0
    return {"estimate": round(mean, 2), "uncertainty_proxy": round(uncertainty, 2),
            "status": "synthetic baseline; not calibrated; no performance claim"}
