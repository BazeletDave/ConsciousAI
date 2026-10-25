"""Strict benchmark gate. A metadata-only candidate dataset cannot generate model claims."""
import hashlib,json
def validate(rows):
 if not isinstance(rows,list):raise ValueError("rows must be list")
 ids=set();groups={};issues=[]
 for row in rows:
  rid=row.get("record_id")
  if not rid or rid in ids:issues.append("missing_or_duplicate_id")
  ids.add(rid)
  group=row.get("case_family")
  split=row.get("split")
  if not group or split not in ("development","holdout"):issues.append("invalid_group_or_split")
  if group in groups and groups[group]!=split:issues.append("group_leakage")
  groups[group]=split
  if row.get("rights_status")!="steward_approved_public_metadata":issues.append("rights_not_cleared")
  if row.get("independent_review_status")!="adjudicated":issues.append("independent_review_missing")
  if row.get("label") not in (0,1) or isinstance(row.get("label"),bool):issues.append("independent_label_missing")
 if not any(x.get("split")=="holdout" for x in rows):issues.append("holdout_empty")
 if not any(x.get("split")=="development" for x in rows):issues.append("development_empty")
 return {"eligible":not issues,"issues":sorted(set(issues)),"records":len(rows),"groups":len(groups)}
def majority_baseline(train,test):
 gate=validate(train+test)
 if not gate["eligible"]:return {"status":"blocked","validation":gate,"metrics":None}
 if any(x["split"]!="development" for x in train) or any(x["split"]!="holdout" for x in test):raise ValueError("split mismatch")
 majority=int(sum(x["label"] for x in train)>len(train)/2)
 from classification_evaluation import classification_report
 eval_rows=[{"record_id":x["record_id"],"actual":x["label"],"predicted":majority,
 "label_provenance":"independent_review_attested","holdout":True} for x in test]
 return {"status":"baseline_evaluated","baseline":"training_majority_class",
 "evaluation":classification_report(eval_rows),"release_authorized":False}
