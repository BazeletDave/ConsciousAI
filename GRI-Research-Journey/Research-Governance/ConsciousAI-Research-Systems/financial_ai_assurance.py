"""Evidence-gated institutional financial AI assurance research prototype."""
from datetime import datetime, timezone
DOMAINS=("provenance","measurement","scenario_coverage","model_validation","independent_challenge","human_authority","resilience","accountability")
CRITICAL={"provenance","human_authority"}
def assess(record):
    if not isinstance(record,dict): raise ValueError("record must be a dict")
    evidence=record.get("evidence",{})
    if not isinstance(evidence,dict): evidence={}
    checks={}
    for domain in DOMAINS:
        item=evidence.get(domain)
        if not isinstance(item,dict):
            checks[domain]={"status":"not_measured","reason":"No evidence record"}
            continue
        fields=("reference","reviewer","observed_at","finding")
        if any(not isinstance(item.get(f),str) or not item[f].strip() for f in fields):
            checks[domain]={"status":"evidence_pending","reason":"Missing reference, reviewer, observation time or finding"}
            continue
        try:
            observed=datetime.fromisoformat(item["observed_at"].replace("Z","+00:00"))
            if observed.tzinfo is None or observed > datetime.now(timezone.utc): raise ValueError()
        except (ValueError,OverflowError):
            checks[domain]={"status":"evidence_pending","reason":"Invalid timestamp"}
            continue
        checks[domain]={"status":"submitted_unverified","reason":"Evidence metadata is present; independent validation required"}
    blocked=any(checks[d]["status"]!="submitted_unverified" for d in CRITICAL)
    return {"framework":"GRI financial AI assurance v0.1","record_id":str(record.get("record_id",""))[:128],"checks":checks,"overall":"blocked_missing_critical_evidence" if blocked else "requires_independent_validation","certified":False,"validated":False}
