"""Offline GRI Mobility Intelligence CLI. JSON files only; no network access."""
import argparse
import json
from pathlib import Path
from mobility_core import evaluate_scenario, validate_record, net_contribution, baseline_forecast

def run(argv=None):
    p = argparse.ArgumentParser(description="GRI offline mobility research prototype")
    p.add_argument("mode", choices=["scenario", "ledger", "forecast"])
    p.add_argument("input", help="local JSON file")
    p.add_argument("--output", help="optional local JSON output path")
    a = p.parse_args(argv)
    data = json.loads(Path(a.input).read_text(encoding="utf-8"))
    if a.mode == "scenario":
        result = evaluate_scenario(data["scenario"], data["constraints"])
    elif a.mode == "ledger":
        if not isinstance(data, list):
            raise ValueError("ledger input must be an array")
        result = []
        for record in data:
            validate_record(record)
            row = {"record_id": record["record_id"], "validated": True}
            if record["event_type"] in ("TRIP_COMPLETED", "PAYMENT_SETTLED"):
                row["net_contribution"] = net_contribution(record)
            result.append(row)
    else:
        result = baseline_forecast(data["history"], data["horizon_index"])
    output = json.dumps(result, indent=2, sort_keys=True)
    if a.output:
        Path(a.output).write_text(output + "\n", encoding="utf-8")
    else:
        print(output)
    return result

if __name__ == "__main__":
    run()
