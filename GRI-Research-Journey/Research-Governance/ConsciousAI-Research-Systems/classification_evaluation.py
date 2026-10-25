"""Reproducible offline classification evaluation; no training or real-world performance claim."""
import hashlib,json,math
def classification_report(rows,min_samples=30):
 if not isinstance(rows,list):raise ValueError("rows must be list")
 if len(rows)<min_samples:return {"status":"insufficient_independently_labeled_data","samples":len(rows),"metrics":None,"release_authorized":False}
 seen=set();tp=tn=fp=fn=0
 for r in rows:
  if not isinstance(r,dict) or not all(k in r for k in ("record_id","actual","predicted","label_provenance","holdout")):raise ValueError("missing required fields")
  if r["record_id"] in seen:raise ValueError("duplicate ID")
  seen.add(r["record_id"])
  if r["actual"] not in (0,1) or isinstance(r["actual"],bool) or r["predicted"] not in (0,1) or isinstance(r["predicted"],bool):raise ValueError("binary labels required")
  if r["holdout"] is not True or r["label_provenance"]!="independent_review_attested":raise ValueError("independent holdout attestation required")
  a,b=r["actual"],r["predicted"]
  if a==1 and b==1:tp+=1
  elif a==0 and b==0:tn+=1
  elif a==0:fp+=1
  else:fn+=1
 def ratio(a,b):return round(a/b,6) if b else None
 return {"status":"offline_evaluation_not_certification","samples":len(rows),
  "metrics":{"accuracy":ratio(tp+tn,len(rows)),"precision":ratio(tp,tp+fp),"recall":ratio(tp,tp+fn),"specificity":ratio(tn,tn+fp),"f1":ratio(2*tp,2*tp+fp+fn),"false_positive_rate":ratio(fp,fp+tn)},
  "confusion_matrix":{"tp":tp,"tn":tn,"fp":fp,"fn":fn},
  "dataset_digest":hashlib.sha256(json.dumps(rows,sort_keys=True,separators=(",",":")).encode()).hexdigest(),
  "release_authorized":False,"limitations":["Attestation fields are not independently authenticated by this function","No fairness, calibration, drift or external replication assessed"]}
