"""Synthetic deterministic policy comparison. Research only, not a production authorization service."""
import argparse
import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
ALLOWED_ACTIONS = frozenset({"read"})

def technical_only(case):
    """Intentionally weak baseline: token and consent presence only."""
    return bool(case["token"] and case["consent"])

def institutional(case):
    """Fail closed for the experimental control set; not real identity verification."""
    return bool(
        case["token"] and case["mandate"] and case["consent"]
        and not case["revoked"] and not case["conflict"]
        and case["operator"] and case["separated"]
        and case["action"] in ALLOWED_ACTIONS
    )

def confusion(rows, key):
    tp = sum(not r["expected_allow"] and not r[key] for r in rows)
    fn = sum(not r["expected_allow"] and r[key] for r in rows)
    fp = sum(r["expected_allow"] and not r[key] for r in rows)
    tn = sum(r["expected_allow"] and r[key] for r in rows)
    return {"blocked_unsafe":tp,"false_approvals":fn,"false_denials":fp,"allowed_safe":tn,
            "unsafe_total":tp+fn,"safe_total":fp+tn}

def evaluate(fixtures):
    if fixtures.get("synthetic_only") is not True:
        raise ValueError("Only explicitly synthetic fixtures are permitted")
    rows = []
    ids = set()
    for case in fixtures["scenarios"]:
        if case["id"] in ids:
            raise ValueError("Duplicate scenario identifier")
        ids.add(case["id"])
        required = {"id","token","mandate","consent","revoked","conflict","operator","separated","action","expected_allow"}
        if set(case) != required:
            raise ValueError("Unexpected or missing fixture fields")
        if any(type(case[k]) is not bool for k in required - {"id","action"}):
            raise ValueError("Boolean fixture fields required")
        rows.append({"id":case["id"],"expected_allow":case["expected_allow"],
                     "technical_allow":technical_only(case),"institutional_allow":institutional(case)})
    canonical = json.dumps(fixtures,sort_keys=True,separators=(",",":")).encode()
    return {"schema_version":"1.0","synthetic_only":True,"fixture_sha256":hashlib.sha256(canonical).hexdigest(),
            "scenario_count":len(rows),"baseline":confusion(rows,"technical_allow"),
            "intervention":confusion(rows,"institutional_allow"),"decisions":rows,
            "limitations":"Deterministic hand-authored cases; no statistical generalization, real authentication, ML model or RL training."}

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("--fixtures",type=Path,default=HERE/"fixtures.json")
    parser.add_argument("--output",type=Path)
    args=parser.parse_args()
    report=evaluate(json.loads(args.fixtures.read_text(encoding="utf-8")))
    result=json.dumps(report,sort_keys=True,indent=2)+"\n"
    if args.output:
        args.output.write_text(result,encoding="utf-8")
    else:
        print(result,end="")

if __name__=="__main__":
    main()
