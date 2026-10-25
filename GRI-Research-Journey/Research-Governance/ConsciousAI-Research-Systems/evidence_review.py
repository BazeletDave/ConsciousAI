"""Audit-oriented evidence review: two independent reviewers, immutable claim fingerprint.
This module does not claim a record was independently verified without signed review data.
"""
import hashlib,json
def fingerprint(record):
 fields={k:record.get(k) for k in ("id","source_id","source_url","title","verification_status")}
 return hashlib.sha256(json.dumps(fields,sort_keys=True,separators=(",",":"),ensure_ascii=False).encode()).hexdigest()
def assess_review(record,reviews):
 digest=fingerprint(record)
 valid=[]
 for r in reviews:
  if not isinstance(r,dict):continue
  if r.get("record_digest")!=digest or r.get("decision")!="source_and_claim_corrobated":continue
  if not all(isinstance(r.get(k),str) and r[k].strip() for k in ("reviewer_id","reviewed_at","evidence_url")):continue
  if not r["evidence_url"].startswith("https://"):continue
  valid.append(r["reviewer_id"])
 independent=len(set(valid))>=2
 return {"record_digest":digest,"reviewers_accepted":len(set(valid)),
  "independent_review_threshold_met":independent,
  "status":"human_review_threshold_met_claim_not_automatically_certified" if independent else "human_review_pending",
  "publication_authorized":False,
  "notice":"Two distinct review identities and matching digests are necessary but not sufficient; identity, independence, evidence and conclusions require institutional validation."}
