"""Deterministic research reference policy. Classifications must come from a trusted host."""
CONSTRAINTS=("cbrn","csam","cyber_attack","ncii","shutdown_resistance","reasoning_obstruction","mass_manipulation")
AUTHORITY=("root","system","developer","user","untrusted")
EFFECT=("deny","escalate","allow")
def evaluate(payload):
    rid=payload.get("request_id","invalid") if isinstance(payload,dict) else "invalid"
    def out(d,c,p,a,j): return dict(decision=d,constraint=c,priority=p,authority=a,justification=j,request_id=rid)
    if not isinstance(payload,dict): return out("deny",None,"broadly_safe","root","Invalid input; fail closed.")
    fs=payload.get("findings"); ins=payload.get("instructions")
    valid=(payload.get("schema_version")=="1.0" and isinstance(rid,str) and bool(rid)
        and isinstance(fs,list) and isinstance(ins,list) and payload.get("risk") in ("low","elevated","high"))
    if valid:
        valid=(len(fs)==7 and all(isinstance(f,dict) and f.get("id") in CONSTRAINTS and f.get("status") in ("clear","violation","unknown") for f in fs)
            and {f["id"] for f in fs}==set(CONSTRAINTS)
            and all(isinstance(i,dict) and isinstance(i.get("id"),str) and i.get("authority") in AUTHORITY and i.get("effect") in EFFECT for i in ins))
    if not valid: return out("deny",None,"broadly_safe","root","Invalid input; fail closed.")
    violations=sorted(f["id"] for f in fs if f["status"]=="violation")
    if violations: return out("deny",violations[0],"broadly_safe","root","Absolute constraint violation; action denied.")
    if any(f["status"]=="unknown" for f in fs): return out("escalate",None,"broadly_safe","root","Unknown constraint classification; review required.")
    if payload["risk"]=="high": return out("escalate",None,"broadly_safe","system","High risk requires authorized review.")
    if payload["risk"]=="elevated": return out("escalate",None,"broadly_ethical","system","Elevated risk requires authorized review regardless of instruction authority.")
    if ins:
        rank=min(AUTHORITY.index(i["authority"]) for i in ins)
        effects={i["effect"] for i in ins if AUTHORITY.index(i["authority"])==rank}
        return out(next(e for e in EFFECT if e in effects),None,"organizational",AUTHORITY[rank],"Resolved by highest applicable instruction authority.")
    return out("allow",None,"helpful","user","No constraints or elevated risk; default helpful behavior.")
