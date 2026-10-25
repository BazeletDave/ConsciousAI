"""GRI operational intelligence pipeline: official metadata -> review queue and health.
No claim verification, no external writes except local JSON output.
"""
import argparse,hashlib,json,os,tempfile
from datetime import datetime,timezone
from pathlib import Path
ROOT=Path(__file__).resolve().parent
INPUT=ROOT/"policy_candidates.json"
OUTPUT=ROOT/"intelligence_feed.json"
TERMS=("artificial intelligence","machine learning","automated","algorithm","driver","rideshare","transportation","vehicle","mobility","autonomous")
def build(payload,now=None):
 now=now or datetime.now(timezone.utc).isoformat()
 if not isinstance(payload,dict) or not isinstance(payload.get("records"),list):raise ValueError("invalid input registry")
 queue=[];seen=set()
 for item in payload["records"]:
  if not isinstance(item,dict):continue
  url=item.get("official_source_url","")
  if not isinstance(url,str) or not url.startswith("https://www.federalregister.gov/"):continue
  doc=item.get("document_number")
  if not isinstance(doc,str) or not doc or doc in seen:continue
  seen.add(doc)
  title=str(item.get("title") or "")
  abstract=str(item.get("abstract") or "")
  matches=[t for t in TERMS if t in (title+" "+abstract).lower()]
  if not matches:continue
  queue.append({"id":"US-FR-"+doc,"source_url":url,"title":title[:300],
                "publication_date":item.get("publication_date"),
                "topics":matches,"priority":"review" if any(t in matches for t in ("driver","rideshare","autonomous","algorithm")) else "standard",
                "verification_status":"official_api_metadata_unreviewed",
                "human_review_required":True,"publication_authorized":False})
 queue.sort(key=lambda x:(x.get("publication_date") or "",x["id"]),reverse=True)
 raw=json.dumps(payload,sort_keys=True,separators=(",",":"),ensure_ascii=False).encode()
 return {"schema_version":"1.0","mode":"automated_official_metadata_triage",
         "generated_at":now,"source_last_collection_at":payload.get("last_collection_at"),
         "source_registry_sha256":hashlib.sha256(raw).hexdigest(),
         "source_records":len(payload["records"]),"matched_records":len(queue),
         "human_review_required":len(queue),"queue":queue[:250],
         "health":{"pipeline":"completed","source_collection_status":"not_independently_verified_by_this_stage"},
         "notice":"Keyword triage only; neither ML classification nor independent factual verification. All candidates remain unreviewed."}
def main():
 p=argparse.ArgumentParser();p.add_argument("--input",type=Path,default=INPUT);p.add_argument("--output",type=Path,default=OUTPUT);a=p.parse_args()
 result=build(json.loads(a.input.read_text(encoding="utf8")))
 with tempfile.NamedTemporaryFile("w",encoding="utf8",dir=a.output.parent,delete=False) as f:
  json.dump(result,f,indent=2,ensure_ascii=False);f.write("\n");tmp=f.name
 os.replace(tmp,a.output)
 print(json.dumps({"matched":result["matched_records"],"source_records":result["source_records"],"status":"completed"}))
if __name__=="__main__":main()
