"""GRI source-monitoring prototype. Stdlib-only, offline, review-gated.
Input JSONL records are supplied from separately authorized collection processes.
No scraping, API calls, or automatic publication.
"""
import argparse, hashlib, json
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

REQUIRED = {"source_url", "source_platform", "source_date", "claim_text_paraphrase", "verification_status"}
STATUSES = {"CORPORATE_CLAIM","FIRSTHAND_UNVERIFIED","INDEPENDENTLY_CORROBORATED","UNVERIFIED_SPECULATION","REJECTED"}
def ingest(records):
    findings, seen, errors = [], set(), []
    for line_no, row in enumerate(records, 1):
        if not isinstance(row, dict) or not REQUIRED.issubset(row):
            errors.append({"line": line_no, "reason": "missing required fields"}); continue
        if not all(isinstance(row[k],str) and row[k].strip() for k in REQUIRED):
            errors.append({"line": line_no, "reason": "invalid fields"}); continue
        if row["verification_status"] not in STATUSES:
            errors.append({"line": line_no, "reason": "unknown verification status"}); continue
        if not row["source_url"].startswith(("https://","http://")):
            errors.append({"line": line_no, "reason": "invalid source URL"}); continue
        canonical = json.dumps({k:row[k] for k in sorted(REQUIRED)},sort_keys=True,ensure_ascii=False)
        digest = hashlib.sha256(canonical.encode()).hexdigest()
        if digest in seen: continue
        seen.add(digest)
        findings.append({"evidence_id": digest, **{k:row[k] for k in sorted(REQUIRED)},
                         "review_state":"PENDING_HUMAN_REVIEW",
                         "publication_authorized":False})
    return {"schema":"gri-source-monitor-v1","generated_at":datetime.now(timezone.utc).isoformat(),
            "unique_records":len(findings),"by_status":dict(Counter(x["verification_status"] for x in findings)),
            "errors":errors,"findings":findings,
            "constraints":["No automatic promotion of claims to verified","No publication without separate human approval","Source collection and legal review are outside this module"]}
def main():
    ap=argparse.ArgumentParser();ap.add_argument("--input",required=True);ap.add_argument("--output",required=True)
    a=ap.parse_args()
    with open(a.input,encoding="utf-8") as f:records=[json.loads(line) for line in f if line.strip()]
    Path(a.output).write_text(json.dumps(ingest(records),indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
if __name__=="__main__":main()
