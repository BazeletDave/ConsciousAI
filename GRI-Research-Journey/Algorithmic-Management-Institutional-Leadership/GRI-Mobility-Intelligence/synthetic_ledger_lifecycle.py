"""Offline synthetic-only ledger import, export and deletion for issue 12.

No network, real participant ingestion, or consent verification service.
"""
import argparse
import csv
import json
from pathlib import Path
from mobility_core import validate_record

FIELDS = ("record_id","consent_id","consent_active","synthetic","event_type","start","end",
          "gross","tips","incentives","incentives_in_gross","paid_miles","unpaid_miles",
          "cost_per_mile","tolls","source")
BOOL_FIELDS = {"consent_active", "synthetic", "incentives_in_gross"}
NUMBER_FIELDS = {"gross","tips","incentives","paid_miles","unpaid_miles","cost_per_mile","tolls"}

def _parse_csv_value(key, value):
    if key in BOOL_FIELDS:
        if value not in ("true", "false"):
            raise ValueError("invalid boolean CSV value")
        return value == "true"
    if key in NUMBER_FIELDS:
        return float(value)
    return value

def read_ledger(path):
    path = Path(path)
    if path.suffix.lower() == ".json":
        records = json.loads(path.read_text(encoding="utf-8"))
    elif path.suffix.lower() == ".csv":
        with path.open(newline="", encoding="utf-8") as handle:
            reader = csv.DictReader(handle)
            if reader.fieldnames is None or set(reader.fieldnames) != set(FIELDS):
                raise ValueError("CSV headers must match schema")
            records = [{k: _parse_csv_value(k, row[k]) for k in FIELDS} for row in reader]
    else:
        raise ValueError("only JSON and CSV supported")
    if not isinstance(records, list):
        raise ValueError("ledger must be an array")
    ids = set()
    for record in records:
        validate_record(record)
        if record["synthetic"] is not True:
            raise ValueError("real participant records are disabled in public prototype")
        if record["record_id"] in ids:
            raise ValueError("duplicate record_id")
        ids.add(record["record_id"])
    return records

def write_ledger(path, records):
    path = Path(path)
    if path.exists():
        raise FileExistsError("refusing to overwrite an existing file")
    if path.suffix.lower() not in (".csv", ".json"):
        raise ValueError("only JSON and CSV supported")
    if not isinstance(records, list):
        raise ValueError("ledger must be an array")
    for record in records:
        validate_record(record)
        if record["synthetic"] is not True:
            raise ValueError("real participant records disabled")
    if path.suffix.lower() == ".json":
        path.write_text(json.dumps(records, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    else:
        with path.open("x", newline="", encoding="utf-8") as handle:
            writer = csv.DictWriter(handle, fieldnames=FIELDS)
            writer.writeheader()
            for record in records:
                writer.writerow({k: str(record[k]).lower() if k in BOOL_FIELDS else record[k] for k in FIELDS})

def run(argv=None):
    parser = argparse.ArgumentParser(description="Synthetic-only local ledger lifecycle")
    parser.add_argument("action", choices=("export", "delete"))
    parser.add_argument("input")
    parser.add_argument("output")
    parser.add_argument("--record-id", help="record to exclude from exported dataset")
    args = parser.parse_args(argv)
    if args.action == "delete" and not args.record_id:
        parser.error("delete requires --record-id")
    if args.action == "export" and args.record_id:
        parser.error("export does not accept --record-id")
    records = read_ledger(args.input)
    if args.action == "delete":
        if not any(r["record_id"] == args.record_id for r in records):
            raise ValueError("record not found")
        records = [r for r in records if r["record_id"] != args.record_id]
    write_ledger(args.output, records)
    return {"action": args.action, "exported_records": len(records),
            "source_unchanged": True, "notice": "Local synthetic output only; source and backups not deleted"}

if __name__ == "__main__":
    print(json.dumps(run(), indent=2))
