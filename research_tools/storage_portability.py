"""Portable, offline GRI staging evidence export and cost telemetry.

This module does not change production storage or imply PostgreSQL integration.
"""
import argparse
import hashlib
import json
import sqlite3
import time
from pathlib import Path

def canonical(value):
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")

def export_evidence(db_path, output_path):
    db_path, output_path = Path(db_path), Path(output_path)
    if not db_path.is_file() or output_path.exists():
        raise ValueError("database must exist and export must not exist")
    with sqlite3.connect(f"file:{db_path.resolve()}?mode=ro", uri=True) as db:
        if db.execute("PRAGMA integrity_check").fetchone()[0] != "ok":
            raise ValueError("source integrity check failed")
        rows = db.execute("SELECT digest, payload, status, inserted_at FROM evidence ORDER BY digest").fetchall()
    records = []
    for digest, payload, status, inserted_at in rows:
        item = json.loads(payload)
        if item.get("digest") != digest or status != "HUMAN_REVIEW_REQUIRED":
            raise ValueError("inconsistent evidence ledger")
        if item.get("publication_approved") is not False or item.get("training_eligible") is not False:
            raise ValueError("unexpected promotion")
        records.append({"digest":digest,"payload":item,"status":status,"inserted_at":inserted_at})
    data = {"schema_version":"1.0","classification":"RESTRICTED_STAGING_NOT_PUBLIC",
            "records":records,"record_count":len(records)}
    payload = canonical(data)
    output_path.parent.mkdir(parents=True,exist_ok=True)
    with output_path.open("xb") as f:
        f.write(payload)
    output_path.chmod(0o600)
    return {"record_count":len(records),"bytes":len(payload),"sha256":hashlib.sha256(payload).hexdigest(),
            "note":"Restricted local export. Encrypt before transferring offsite."}

def telemetry(db_path, runs=1, duration_seconds=0, storage_cost_per_gb_month=0):
    if runs < 0 or duration_seconds < 0 or storage_cost_per_gb_month < 0:
        raise ValueError("nonnegative values required")
    path=Path(db_path)
    size=path.stat().st_size if path.is_file() else 0
    return {"schema_version":"1.0","measurement":"staging_local_only",
            "database_bytes":size,"processing_runs":runs,"processing_seconds":duration_seconds,
            "estimated_storage_usd_month":round(size / 1_000_000_000 * storage_cost_per_gb_month,6),
            "excluded_costs":["CPU","egress","backup","API","managed_database"],
            "notice":"Estimate, not a provider invoice; free-tier limits must be checked independently."}

if __name__=="__main__":
    p=argparse.ArgumentParser()
    p.add_argument("action",choices=["export","telemetry"])
    p.add_argument("--db",required=True,type=Path)
    p.add_argument("--output",type=Path)
    p.add_argument("--storage-rate",type=float,default=0)
    a=p.parse_args()
    if a.action=="export":
        if a.output is None:p.error("--output required for export")
        result=export_evidence(a.db,a.output)
    else:
        result=telemetry(a.db,storage_cost_per_gb_month=a.storage_rate)
    print(json.dumps(result,indent=2))
