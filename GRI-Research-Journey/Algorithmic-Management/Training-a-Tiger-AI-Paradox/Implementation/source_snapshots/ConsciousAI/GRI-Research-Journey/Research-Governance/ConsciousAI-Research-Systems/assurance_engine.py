"""GRI Assurance Engine v1: deterministic, auditable research evaluation, not an ML model."""
from __future__ import annotations
from collections import Counter
from datetime import datetime, timezone
from hashlib import sha256
from math import sqrt
import json

STATUS = {"verified", "corroborated", "unreviewed", "disputed", "retracted"}
def canonical_hash(obj):
    return sha256(json.dumps(obj, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode()).hexdigest()

def evaluate(record):
    """Fail closed for unsupported claims; independent evidence required for verified status."""
    if not isinstance(record, dict):
        raise ValueError("record must be an object")
    required = ("id", "claim", "sources", "verification_status", "observed_at")
    if any(not record.get(k) for k in required):
        raise ValueError("missing required evidence field")
    if record["verification_status"] not in STATUS:
        raise ValueError("unknown verification status")
    try:
        datetime.fromisoformat(record["observed_at"].replace("Z", "+00:00"))
    except (ValueError, AttributeError) as exc:
        raise ValueError("invalid observation timestamp") from exc
    sources = record["sources"]
    if not isinstance(sources, list) or not sources:
        raise ValueError("sources required")
    if any(not isinstance(s, dict) or not isinstance(s.get("url"), str) or not s["url"].startswith("https://") or not s.get("publisher") for s in sources):
        raise ValueError("sources require publisher and https URL")
    publishers = {s["publisher"].strip().casefold() for s in sources}
    independently_corrob = len(publishers) >= 2 and all(s.get("independently_reviewed") is True for s in sources)
    flags = []
    if record["verification_status"] in {"verified", "corroborated"} and not independently_corrob:
        flags.append("independent_corroboration_missing")
    if record.get("automated_action_requested"):
        flags.append("human_authorization_required")
    if record.get("contradictory_evidence"):
        flags.append("contradictory_evidence_requires_review")
    return {"record_id": record["id"], "record_hash": canonical_hash(record),
            "decision": "hold_for_review" if flags or record["verification_status"] != "verified" else "eligible_for_human_publication_review",
            "flags": flags, "distinct_publishers": len(publishers),
            "review_required": True, "automated_remediation_allowed": False,
            "notice": "Not a truth certification or legal/compliance determination."}

def classification_metrics(samples):
    """Requires externally established binary ground truth, not self-generated labels."""
    if not samples:
        raise ValueError("nonempty labeled evaluation set required")
    cm = Counter()
    groups = {}
    for s in samples:
        if not isinstance(s.get("truth"), bool) or not isinstance(s.get("prediction"), bool):
            raise ValueError("truth and prediction must be booleans")
        cm[("tp" if s["truth"] and s["prediction"] else "tn" if not s["truth"] and not s["prediction"] else "fp" if s["prediction"] else "fn")] += 1
        if "group" in s:
            groups.setdefault(str(s["group"]), []).append(s)
    tp, tn, fp, fn = (cm[k] for k in ("tp", "tn", "fp", "fn"))
    def ratio(a,b): return round(a/b, 6) if b else None
    return {"n":len(samples),"confusion_matrix":dict(tp=tp,tn=tn,fp=fp,fn=fn),
            "accuracy":ratio(tp+tn,len(samples)),"precision":ratio(tp,tp+fp),
            "recall":ratio(tp,tp+fn),"false_positive_rate":ratio(fp,fp+tn),
            "false_negative_rate":ratio(fn,fn+tp),
            "group_positive_prediction_rates":{k:ratio(sum(x["prediction"] for x in v),len(v)) for k,v in groups.items()},
            "limitations":"Group rates are descriptive only; they do not establish fairness or causal bias."}

def calibration_metrics(samples):
    """Brier score for externally labeled probabilistic predictions."""
    if not samples: raise ValueError("nonempty samples required")
    for s in samples:
        if not isinstance(s.get("truth"), bool) or isinstance(s.get("probability"),bool) or not isinstance(s.get("probability"),(int,float)) or not 0 <= s["probability"] <= 1:
            raise ValueError("invalid labeled probability")
    return {"n":len(samples),"brier_score":round(sum((s["probability"]-int(s["truth"]))**2 for s in samples)/len(samples),6),
            "lower_is_better":True,"notice":"Calibration requires independent outcome labels and representative evaluation data."}

def drift_monitor(baseline,current,threshold=0.2):
    """Standardized mean shift heuristic; not a trained detector or validated alert threshold."""
    if len(baseline)<2 or not current or not all(isinstance(x,(int,float)) and not isinstance(x,bool) for x in baseline+current):
        raise ValueError("numeric baseline (>=2) and current samples required")
    mean=sum(baseline)/len(baseline)
    sd=sqrt(sum((x-mean)**2 for x in baseline)/(len(baseline)-1))
    shift=abs(sum(current)/len(current)-mean)/(sd if sd>0 else 1)
    return {"standardized_mean_shift":round(shift,6),"heuristic_alert":shift>threshold,
            "threshold":threshold,"review_required":True,"notice":"Exploratory drift signal; not a safety or intrusion determination."}
