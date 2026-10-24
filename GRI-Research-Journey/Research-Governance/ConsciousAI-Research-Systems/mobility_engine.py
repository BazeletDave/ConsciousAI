"""GRI Mobility Intelligence: read-only deterministic research engine. No live ingestion."""
import math
RATE = 0.38  # GRI assumption, not an IRS mileage rate

def nonnegative(value, name):
    if isinstance(value, bool) or not isinstance(value, (float, int)) or not math.isfinite(value) or value < 0:
        raise ValueError(name + " must be finite and nonnegative")
    return float(value)

def evaluate_offer(offer, schedule):
    miles = nonnegative(offer["pickup_miles"], "pickup_miles") + nonnegative(offer["ride_miles"], "ride_miles")
    gross = nonnegative(offer["offered_pay"], "offered_pay") + nonnegative(offer.get("incentives", 0), "incentives")
    cost = miles * RATE + nonnegative(offer.get("tolls", 0), "tolls")
    minutes = sum(nonnegative(offer.get(k, 0), k) for k in ("duration_min", "waiting_min", "return_home_transit_min"))
    if minutes <= 0:
        raise ValueError("zero committed duration")
    hours = minutes / 60
    finish = nonnegative(offer["offer_time_hour"], "offer_time_hour") + hours
    reasons = []
    if offer.get("overlaps_class_block", False):
        reasons.append("class_conflict")
    if finish > nonnegative(schedule["max_finish_time_hour"], "max_finish_time_hour"):
        reasons.append("return_deadline")
    if nonnegative(schedule["sleep_hours_available"], "sleep_hours_available") < nonnegative(schedule.get("min_sleep_required", 7), "min_sleep_required"):
        reasons.append("sleep_limit")
    return {"offer_id": offer["offer_id"], "platform": offer["platform"], "estimated_net": round(gross - cost, 2),
            "full_commitment_hours": round(hours, 3), "net_per_full_hour": round((gross - cost) / hours, 2),
            "feasible": not reasons, "rejection_reasons": reasons,
            "classification": "illustrative_scenario_not_realized_earnings"}

def rank_offers(offers, schedule):
    rows = [evaluate_offer(o, schedule) for o in offers]
    return {"feasible_ranked": sorted((x for x in rows if x["feasible"]), key=lambda x: x["net_per_full_hour"], reverse=True),
            "rejected": [x for x in rows if not x["feasible"]]}

def public_summary():
    return {"schema_version": "0.1", "program": "GRI Mobility Intelligence", "dataset_id": "RESEARCH_DATASET_12",
            "status": "research_prototype", "verified_observations": 0, "trained_models": 0,
            "financial_assumption_usd_per_mile": RATE, "deployment_mode": "read_only",
            "notice": "No live data ingestion, machine learning model, or dispatch automation."}
