"""Generate an audit-readable snapshot of actual deterministic assurance evaluations.

Runs in the scheduled GitHub Actions job. Does not claim production ML inference.
"""
from datetime import datetime, timezone
from hashlib import sha256
from pathlib import Path
import json
from assurance_engine import evaluate

ROOT=Path(__file__).resolve().parent
def canonical(obj):
    return json.dumps(obj, sort_keys=True, separators=(",",":"), ensure_ascii=False).encode()
def build():
    feed=json.loads((ROOT/"ai_intelligence.json").read_text(encoding="utf-8"))
    results=[]
    for item in feed["records"]:
        rec={"id":item["id"],"claim":item["summary"],
             "observed_at":feed["updated_at"]+"T00:00:00+00:00",
             "verification_status":"unreviewed",
             "sources":[{"publisher":s["name"],"url":s["url"],
                         "independently_reviewed":False} for s in item["sources"]]}
        decision=evaluate(rec)
        results.append({"record_id":decision["record_id"],"record_hash":decision["record_hash"],
                        "decision":decision["decision"],"review_required":decision["review_required"]})
    results.sort(key=lambda r:r["record_id"])
    payload={"schema_version":"1.0","source":"gri_deterministic_assurance_engine",
             "generated_at":datetime.now(timezone.utc).isoformat(),
             "watchlist_updated_at":feed["updated_at"],
             "evaluation_count":len(results),
             "human_review_count":sum(r["review_required"] for r in results),
             "results":results,
             "scope":"Actual deterministic watchlist assurance evaluations; NOT production ML inference, model accuracy, or independent source verification."}
    payload["content_sha256"]=sha256(canonical({k:v for k,v in payload.items() if k!="content_sha256"})).hexdigest()
    return payload
if __name__=="__main__":
    path=ROOT/"assurance_evidence_snapshot.json"
    path.write_text(json.dumps(build(),indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
