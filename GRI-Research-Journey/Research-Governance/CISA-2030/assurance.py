"""Offline synthetic CISA 2030 assurance experiment; no live infrastructure actions."""
import hashlib
import json

DOMAINS = ("defend", "harden", "prevail", "human_authority", "evidence_integrity", "institutional_legitimacy")
REQUIRED = ("case_id", "scenario_type", "source_id", "observations")
MEASURES = {
    "defend": "detected",
    "harden": "patch_verified",
    "prevail": "recovery_verified",
    "human_authority": "override_success",
    "evidence_integrity": "provenance_verified",
    "institutional_legitimacy": "remediation_documented",
}

def assess(case):
    if not isinstance(case, dict) or any(k not in case for k in REQUIRED):
        raise ValueError("missing case fields")
    if case["scenario_type"] != "synthetic":
        raise ValueError("only synthetic scenarios permitted")
    if not all(isinstance(case[k], str) and case[k].strip() for k in ("case_id", "source_id")):
        raise ValueError("invalid case identity")
    obs = case["observations"]
    if not isinstance(obs, dict):
        raise ValueError("observations must be an object")
    scores = {}
    for domain, key in MEASURES.items():
        value = obs.get(key)
        if value is not None and type(value) is not bool:
            raise ValueError("measure must be boolean or absent: " + key)
        scores[domain] = "unmeasured" if value is None else ("pass" if value else "fail")
    canonical = json.dumps(case, sort_keys=True, separators=(",", ":"), allow_nan=False)
    return {"case_id": case["case_id"], "classification": "synthetic_only",
            "measures": scores, "record_sha256": hashlib.sha256(canonical.encode()).hexdigest(),
            "production_validated": False}
