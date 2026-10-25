"""Conservative, reproducible evidence-quality diagnostics. Scores are triage, never verification."""
import hashlib,json
from urllib.parse import urlparse
WEIGHTS={"traceability":30,"source_type":20,"limitations":15,"review":25,"reproducibility":10}
def score(record, reviews=()):
 if not isinstance(record,dict):raise ValueError("record must be an object")
 url=record.get("primary_source_url") or record.get("source_url") or record.get("source") or ""
 official=isinstance(url,str) and url.startswith("https://") and bool(urlparse(url).hostname)
 status=str(record.get("verification_status","")).lower()
 trace=30 if official else (12 if isinstance(url,str) and url.strip() else 0)
 source=20 if official and any(k in status for k in ("official","publisher")) else (8 if official else 0)
 limitations=15 if isinstance(record.get("limitations"),str) and len(record["limitations"].strip())>=20 else 0
 from evidence_review import assess_review
 review=assess_review(record,list(reviews))
 reviewed=25 if review["independent_review_threshold_met"] else 0
 reproducibility=10 if isinstance(record.get("methodology_url"),str) and record["methodology_url"].startswith("https://") else 0
 components={"traceability":trace,"source_type":source,"limitations":limitations,"review":reviewed,"reproducibility":reproducibility}
 total=sum(components.values())
 return {"id":record.get("id"),"score":total,"max_score":100,"components":components,
 "tier":"review_candidate" if total>=65 else "insufficient_evidence",
 "independently_verified":False,"publication_authorized":False,
 "review_status":review["status"],"method":"deterministic_heuristic_v1",
 "notice":"Score measures documented evidence attributes, not claim truth, source authenticity, or legal validity."}
def dataset_manifest(records):
 if not isinstance(records,list):raise ValueError("records must be a list")
 ids=[str(x.get("id","")) for x in records]
 if not all(ids) or len(ids)!=len(set(ids)):raise ValueError("missing or duplicate record IDs")
 digest=hashlib.sha256(json.dumps(records,sort_keys=True,ensure_ascii=False,separators=(",",":")).encode()).hexdigest()
 return {"dataset_digest":digest,"records":len(records),"reviewed_records":0,
 "independent_claim_verifications":0,"label_status":"not_independently_labeled",
 "release_authorized":False}
