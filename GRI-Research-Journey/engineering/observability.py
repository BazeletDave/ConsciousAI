"""Deterministic research telemetry assessment, not a live health claim."""
from datetime import datetime, timezone

def assess_collector(run, *, now, maximum_age_seconds=10800):
    if not isinstance(run, dict) or not isinstance(now, datetime) or now.tzinfo is None:
        raise ValueError("run and timezone-aware now required")
    if not isinstance(maximum_age_seconds, (int,float)) or maximum_age_seconds <= 0:
        raise ValueError("maximum age must be positive")
    try:
        finished = datetime.fromisoformat(run["finished_at"].replace("Z","+00:00"))
    except (KeyError, ValueError, TypeError) as exc:
        raise ValueError("invalid finished_at") from exc
    if finished.tzinfo is None:
        raise ValueError("finished_at must include timezone")
    age = (now.astimezone(timezone.utc)-finished.astimezone(timezone.utc)).total_seconds()
    valid = run.get("status") == "success" and type(run.get("records_processed")) is int and run["records_processed"] >= 0
    healthy = valid and 0 <= age <= maximum_age_seconds
    return {"status": "HEALTHY" if healthy else "ALERT",
            "age_seconds": age, "records_processed": run.get("records_processed"),
            "source": "supplied_run_record", "production_verified": False}
