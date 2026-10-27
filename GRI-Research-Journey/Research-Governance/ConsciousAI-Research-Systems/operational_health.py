"""Local readiness and collection diagnostics. No network access or data mutation."""
from datetime import datetime, timezone
import json

REQUIRED_DATASETS = (
    "cases.json", "events.json", "policies.json", "intelligence_feed.json",
    "international_mobility_feed.json", "research_dataset/manifest.json",
)
# Two three-hour collection windows allow for scheduler and deployment delays.
MAX_AGE_SECONDS = 6 * 60 * 60
CLOCK_SKEW_SECONDS = 5 * 60
FEEDS = (
    ("policy_candidates.json", "last_collection_at"),
    ("intelligence_feed.json", "source_last_collection_at"),
    ("international_mobility_feed.json", "generated_at"),
)


def readiness(root):
    missing, invalid = [], []
    for name in REQUIRED_DATASETS:
        path = root / name
        if not path.is_file():
            missing.append(name)
            continue
        try:
            json.loads(path.read_text(encoding="utf-8"))
        except (ValueError, OSError):
            invalid.append(name)
    return {
        "status": "degraded" if missing or invalid else "ok",
        "service": "GRI governance intelligence research platform",
        "required_datasets": len(REQUIRED_DATASETS), "missing": missing, "invalid": invalid,
        "notice": "Readiness verifies local data presence and JSON parsing, not freshness, external source uptime, or independent research validation.",
    }


def collection_status(root, now=None):
    now = now or datetime.now(timezone.utc)
    if now.tzinfo is None or now.utcoffset() is None:
        raise ValueError("An aware reference time is required")
    feeds = []
    for name, field in FEEDS:
        item = {"dataset": name, "timestamp_field": field, "collected_at": None,
                "age_seconds": None, "status": "missing"}
        try:
            data = json.loads((root / name).read_text(encoding="utf-8"))
            if not isinstance(data, dict):
                raise ValueError("Object required")
            stamp = data.get(field)
            if not isinstance(stamp, str):
                raise ValueError("Timestamp required")
            parsed = datetime.fromisoformat(stamp.replace("Z", "+00:00"))
            if parsed.tzinfo is None or parsed.utcoffset() is None:
                raise ValueError("Timezone required")
            age = (now - parsed).total_seconds()
            item.update(collected_at=stamp, age_seconds=round(age, 3),
                        status="future_timestamp" if age < -CLOCK_SKEW_SECONDS else
                        "stale" if age > MAX_AGE_SECONDS else "current")
            if name == "international_mobility_feed.json":
                sources = data.get("sources")
                valid = (isinstance(sources, list) and bool(sources) and
                         all(isinstance(s, dict) and isinstance(s.get("source_id"), str)
                             and s.get("status") == "fetched" for s in sources))
                item["source_collection_status"] = "all_fetched" if valid else "incomplete"
                if not valid and item["status"] == "current":
                    item["status"] = "collection_incomplete"
        except FileNotFoundError:
            pass
        except (ValueError, OSError):
            item["status"] = "invalid"
        feeds.append(item)
    return {
        "schema_version": "1.0", "checked_at": now.isoformat(),
        "status": "current" if all(f["status"] == "current" for f in feeds) else "attention_required",
        "max_age_seconds": MAX_AGE_SECONDS, "clock_skew_seconds": CLOCK_SKEW_SECONDS,
        "feeds": feeds,
        "notice": "Local collection timestamps are operational metadata, not proof of source accuracy, independent verification, or complete coverage. This diagnostic does not control service readiness.",
    }
