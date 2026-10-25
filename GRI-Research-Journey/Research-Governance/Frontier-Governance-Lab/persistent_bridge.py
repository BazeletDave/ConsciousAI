"""Verify persisted assurance snapshot and link it to read-only intake records.

The persisted snapshot is a Git-tracked artifact, not a durable external audit log.
No synthetic metrics are inferred from news. No authorization is granted.
"""
import json
from hashlib import sha256
from pathlib import Path
from evidence import digest
from intelligence_adapter import load_watchlist

def _canonical_source(value):
    # Match the producer's exact canonicalization, including UTF-8 non-ASCII.
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")

def verify_persisted_snapshot(path):
    raw = json.loads(Path(path).read_text(encoding="utf-8"))
    if not isinstance(raw, dict):
        raise ValueError("snapshot must be object")
    expected = raw.get("content_sha256")
    body = {k:v for k,v in raw.items() if k != "content_sha256"}
    if (raw.get("schema_version") != "1.0" or
        raw.get("source") != "gri_deterministic_assurance_engine" or
        not isinstance(expected, str) or len(expected) != 64 or
        sha256(_canonical_source(body)).hexdigest() != expected):
        raise ValueError("persisted snapshot integrity or provenance invalid")
    results = raw.get("results")
    if not isinstance(results, list) or type(raw.get("evaluation_count")) is not int or raw["evaluation_count"] != len(results):
        raise ValueError("snapshot count mismatch")
    seen = set()
    for result in results:
        if not isinstance(result, dict) or not isinstance(result.get("record_id"), str) or not result["record_id"].strip() or result["record_id"] in seen:
            raise ValueError("invalid or duplicate result")
        seen.add(result["record_id"])
        h = result.get("record_hash")
        if not isinstance(h, str) or len(h) != 64 or any(c not in "0123456789abcdef" for c in h):
            raise ValueError("invalid record hash")
        if type(result.get("review_required")) is not bool:
            raise ValueError("invalid review flag")
    if type(raw.get("human_review_count")) is not int or raw["human_review_count"] != sum(r["review_required"] for r in results):
        raise ValueError("human review count mismatch")
    return raw

def build_linked_manifest(watchlist_path, persisted_path):
    records = load_watchlist(watchlist_path)
    snapshot = verify_persisted_snapshot(persisted_path)
    by_id = {r["record_id"]:r for r in snapshot["results"]}
    if set(by_id) != {r.record_id for r in records}:
        raise ValueError("watchlist and persisted evaluation IDs differ; rebuild snapshot")
    # Do not infer that producer's record_hash matches raw watchlist digest.
    # Producer hashes a transformed assurance record; it is independently stored.
    linked = []
    for r in sorted(records, key=lambda r:r.record_id):
        persisted = by_id[r.record_id]
        if not persisted["review_required"]:
            raise ValueError("unreviewed publication decision requires independent authorization")
        linked.append({
            "record_id":r.record_id,
            "source_status_unverified":r.source_status,
            "watchlist_snapshot_sha256":r.snapshot_digest,
            "persisted_evaluation_record_hash":persisted["record_hash"],
            "persisted_decision":persisted["decision"],
            "human_review_required":True,
            "operational_authorization":False,
        })
    body = {
        "schema_version":"gri.persisted-bridge.v1",
        "mode":"READ_ONLY_RESEARCH",
        "persisted_snapshot_sha256":snapshot["content_sha256"],
        "watchlist_updated_at":snapshot["watchlist_updated_at"],
        "evaluation_count":len(linked),
        "records":linked,
        "external_audit_anchor":None,
        "notice":"Digest linkage and internal consistency only. Does not independently validate primary sources, source-to-record semantic mapping, reviewer identity or operational safety.",
    }
    return {**body, "manifest_sha256":digest(body)}
