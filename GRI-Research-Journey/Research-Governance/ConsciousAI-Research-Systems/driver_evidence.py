"""Consent-based driver evidence intake and corroboration readiness. Offline, no scraping."""
import hashlib
REQUIRED=("record_id","platform","country","observed_at","source_type","consent_status")
def assess(record):
 if not isinstance(record,dict):raise ValueError("record must be an object")
 missing=[x for x in REQUIRED if not isinstance(record.get(x),str) or not record[x].strip()]
 if missing:return {"accepted":False,"missing_fields":missing,"verification_status":"insufficient_metadata"}
 if record["consent_status"]!="explicit_research_consent":
  return {"accepted":False,"missing_fields":[],"verification_status":"consent_not_established"}
 refs=record.get("evidence_refs",[])
 if not isinstance(refs,list) or any(not isinstance(x,dict) or not x.get("type") or not x.get("sha256") or len(x["sha256"])!=64 for x in refs):
  return {"accepted":False,"missing_fields":[],"verification_status":"invalid_evidence_references"}
 independent=any(x.get("independent_of_participant") is True for x in refs)
 status="corroboration_review_pending" if independent else "firsthand_unverified"
 return {"accepted":True,"record_id":record["record_id"],"verification_status":status,
  "evidence_count":len(refs),"human_review_required":True,"publication_authorized":False,
  "notice":"Evidence references and hashes are self-asserted until authenticated by an independent reviewer."}
