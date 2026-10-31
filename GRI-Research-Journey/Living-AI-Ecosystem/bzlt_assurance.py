"""Offline metadata assurance for the GRI BZLT dated relationship register.
No network access, external dependencies, personal records or model inference.
"""
import argparse
import csv
import datetime as dt
import json
from collections import Counter
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parent
REQUIRED = ("edge_id","effective_date","source_entity","relation","target_entity","edge_type","source_url","evidence_note")
TYPES = {"regulatory","ownership","financial","asset_transfer","operating"}
RELATIONS = {"member_of","acquired_100_percent","consolidated_100_percent","issued_shares_for",
"acquired_specified_assets_of","indirect_equity_exposure_66.7_percent",
"indirect_debt_exposure_69.4_percent","indirect_equity_exposure_approx_92_percent",
"operated_brand","creditor_claims_converted_into","secured_loan_150m_USD_to",
"debt_extinguished_approx_842m_USD"}

def audit(rows):
    findings, seen = [], set()
    for line, row in enumerate(rows, 2):
        eid = row.get("edge_id","").strip() or f"row_{line}"
        def flag(code, severity, detail):
            findings.append(dict(edge_id=eid,line=line,code=code,severity=severity,detail=detail))
        for key in REQUIRED:
            if not row.get(key,"").strip():
                flag("missing_field","error",key)
        if eid in seen:
            flag("duplicate_id","error",eid)
        seen.add(eid)
        try:
            dt.date.fromisoformat(row.get("effective_date",""))
        except ValueError:
            flag("invalid_date","error",row.get("effective_date",""))
        if row.get("edge_type") not in TYPES:
            flag("unknown_type","error",row.get("edge_type",""))
        if row.get("relation") not in RELATIONS:
            flag("unreviewed_relation","warning",row.get("relation",""))
        url = urlparse(row.get("source_url",""))
        if url.scheme != "https" or not url.netloc or url.username or url.password:
            flag("source_url_invalid","error",row.get("source_url",""))
        if row.get("source_entity","").strip() == row.get("target_entity","").strip():
            flag("self_relation","warning","Requires review")
    counts = Counter(f["severity"] for f in findings)
    return dict(status="FAIL" if counts["error"] else "PASS",records=len(rows),
                errors=counts["error"],warnings=counts["warning"],findings=findings,
                assurance_scope="Metadata only: source documents not independently verified")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input",type=Path,default=ROOT/"BZLT-Dated-Relationships.csv")
    parser.add_argument("--output",type=Path)
    args = parser.parse_args()
    with args.input.open(encoding="utf-8",newline="") as fh:
        reader = csv.DictReader(fh)
        if not reader.fieldnames or any(k not in reader.fieldnames for k in REQUIRED):
            parser.error("Required CSV headers missing")
        result = audit(list(reader))
    output = json.dumps(result,indent=2,sort_keys=True)+"\n"
    if args.output:
        args.output.write_text(output,encoding="utf-8")
    print(output)
    raise SystemExit(bool(result["errors"]))

if __name__ == "__main__":
    main()
