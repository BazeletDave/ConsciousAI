"""Synthetic clock, malformed data, and HTTP readiness regression checks."""
from datetime import datetime, timedelta, timezone
import json
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest

from operational_health import collection_status, readiness, FEEDS, REQUIRED_DATASETS


class OperationalHealthTests(unittest.TestCase):
    def setUp(self):
        self.tmp = TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.now = datetime(2026, 10, 27, 20, tzinfo=timezone.utc)
        for name in REQUIRED_DATASETS:
            self.write(name, {})
        for name, field in FEEDS:
            data = {field: self.now.isoformat()}
            if name in {"international_mobility_feed.json", "enrollment_discovery.json"}:
                data["sources"] = [{"source_id": "fixture", "status": "fetched"}]
            self.write(name, data)

    def write(self, name, data):
        path = self.root / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(data), encoding="utf-8")

    def status(self):
        return collection_status(self.root, self.now)

    def test_current_and_readable(self):
        self.assertEqual(readiness(self.root)["status"], "ok")
        self.assertEqual(self.status()["status"], "current")

    def test_regeneration_cannot_mask_old_source(self):
        self.write("intelligence_feed.json", {
            "generated_at": self.now.isoformat(),
            "source_last_collection_at": (self.now - timedelta(hours=7)).isoformat(),
        })
        result = self.status()
        self.assertEqual(result["status"], "attention_required")
        self.assertEqual(result["feeds"][1]["status"], "stale")
        self.assertEqual(readiness(self.root)["status"], "ok")

    def test_six_hour_boundary(self):
        self.write("policy_candidates.json", {"last_collection_at": (self.now - timedelta(hours=6)).isoformat()})
        self.assertEqual(self.status()["feeds"][0]["status"], "current")
        self.assertEqual(collection_status(self.root, self.now + timedelta(seconds=1))["feeds"][0]["status"], "stale")

    def test_invalid_timestamps_and_shapes_fail_closed(self):
        for value in [None, {}, [], {"last_collection_at": "nonsense"},
                      {"last_collection_at": "2026-10-27T20:00:00"},
                      {"last_collection_at": 123}]:
            with self.subTest(value=value):
                self.write("policy_candidates.json", value)
                self.assertEqual(self.status()["feeds"][0]["status"], "invalid")

    def test_future_clock_and_timezone(self):
        self.write("policy_candidates.json", {"last_collection_at": (self.now + timedelta(minutes=6)).isoformat()})
        self.assertEqual(self.status()["feeds"][0]["status"], "future_timestamp")
        self.write("policy_candidates.json", {"last_collection_at": "2026-10-27T16:00:00-04:00"})
        self.assertEqual(self.status()["feeds"][0]["age_seconds"], 0)

    def test_partial_collection_visible(self):
        for sources in [[], None, [None], [{"source_id": "fixture", "status": "error"}]]:
            with self.subTest(sources=sources):
                self.write("international_mobility_feed.json", {"generated_at": self.now.isoformat(), "sources": sources})
                self.assertEqual(self.status()["feeds"][2]["status"], "collection_incomplete")

    def test_missing_and_corrupt_files(self):
        (self.root / "intelligence_feed.json").unlink()
        (self.root / "events.json").write_bytes(b"\xff")
        self.assertEqual(readiness(self.root)["missing"], ["intelligence_feed.json"])
        self.assertEqual(readiness(self.root)["invalid"], ["events.json"])
        self.assertEqual(self.status()["feeds"][1]["status"], "missing")
        (self.root / "policy_candidates.json").write_text("{", encoding="utf-8")
        self.assertEqual(self.status()["feeds"][0]["status"], "invalid")

    def test_naive_reference_time_rejected(self):
        with self.assertRaises(ValueError):
            collection_status(self.root, datetime(2026, 10, 27))

    def test_enrollment_partial_failure_not_masked_by_recent_run(self):
        self.write("enrollment_discovery.json", {"generated_at": self.now.isoformat(), "sources": [
            {"source_id": "oig", "status": "failed", "http_status": 406, "consecutive_failures": 3},
            {"source_id": "doj", "status": "fetched_no_relevant_titles"}]})
        item = self.status()["feeds"][-1]
        self.assertEqual(self.status()["status"], "attention_required")
        self.assertEqual(item["status"], "collection_incomplete")
        self.assertEqual(item["sources"][0]["http_status"], 406)

    def test_enrollment_delayed_stale_missing_and_malformed(self):
        for hours, expected in [(6, "current"), (7, "delayed"), (19, "stale")]:
            self.write("enrollment_discovery.json", {"generated_at": (self.now-timedelta(hours=hours)).isoformat(),
                "sources": [{"source_id":"fixture", "status":"fetched"}]})
            self.assertEqual(self.status()["feeds"][-1]["status"], expected)
        self.write("enrollment_discovery.json", {"generated_at": self.now.isoformat(), "sources": [None]})
        self.assertEqual(self.status()["feeds"][-1]["status"], "collection_incomplete")
        (self.root/"enrollment_discovery.json").unlink()
        self.assertEqual(self.status()["feeds"][-1]["status"], "missing")
