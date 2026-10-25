"""GRI metadata-only dataset builder: no teaching-case text or participant data."""
import hashlib,json,re
from pathlib import Path
ROOT=Path(__file__).resolve().parent
PRIVATE=re.compile(r"(student|interview|participant|transcript|consent|private|restricted)",re.I)
def build(cases,events):
 rows=[]
 for family,items in (("case_registry",cases),("event_registry",events)):
  for item in items:
   ident=str(item.get("id","")).strip()
   if not ident:continue
   source=item.get("primary_source_url") or item.get("source") or ""
   # Whitelist public metadata only. No claim text or personal data is exported.
   row={"record_id":ident,"case_family":family,"organization":str(item.get("organization",""))[:120],
        "source_reference":str(source)[:500],"verification_status":str(item.get("verification_status",""))[:120],
        "rights_status":"public_metadata_only_review_pending",
        "label_status":"unlabeled","independent_review_status":"pending",
        "claim_text_included":False,"publication_authorized":False}
   if PRIVATE.search(ident) or PRIVATE.search(str(source)):row["rights_status"]="restricted_excluded";continue
   rows.append(row)
 if len({r["record_id"] for r in rows})!=len(rows):raise ValueError("duplicate record ID")
 rows.sort(key=lambda x:x["record_id"])
 return rows
def group_holdout(rows):
 """All records in a family remain together; prevents within-family leakage."""
 groups=sorted({r["case_family"] for r in rows})
 assignment={}
 for g in groups:
  bucket=int(hashlib.sha256(("GRI-v1:"+g).encode()).hexdigest()[:8],16)%5
  assignment[g]="holdout" if bucket==0 else "development"
 if len(groups)>1 and not any(x=="holdout" for x in assignment.values()):
  assignment[groups[-1]]="holdout"
 if len(groups)>1 and not any(x=="development" for x in assignment.values()):
  assignment[groups[0]]="development"
 return [dict(r,split=assignment[r["case_family"]]) for r in rows]
def manifest(rows):
 payload=json.dumps(rows,sort_keys=True,separators=(",",":"),ensure_ascii=False)
 counts={k:sum(r["split"]==k for r in rows) for k in ("development","holdout")}
 return {"schema_version":"1.0","dataset_digest":hashlib.sha256(payload.encode()).hexdigest(),
  "records":len(rows),"split_counts":counts,"case_families":sorted({r["case_family"] for r in rows}),
  "independently_adjudicated":0,"label_coverage":0,"rights_status":"public_metadata_only_review_pending",
  "benchmark_eligible":False,"limitations":["Metadata rights still require steward approval","No verified labels",
  "Case families are coarse; expand before assessing generalization","No proprietary teaching text or personal interviews included"]}
def main():
 cases=json.loads((ROOT/"cases.json").read_text())["records"]
 events=json.loads((ROOT/"events.json").read_text())["records"]
 rows=group_holdout(build(cases,events))
 output=ROOT/"research_dataset"
 output.mkdir(exist_ok=True)
 (output/"candidate_metadata.json").write_text(json.dumps(rows,indent=2)+"\n")
 (output/"manifest.json").write_text(json.dumps(manifest(rows),indent=2)+"\n")
 print(json.dumps(manifest(rows),indent=2))
if __name__=="__main__":main()
