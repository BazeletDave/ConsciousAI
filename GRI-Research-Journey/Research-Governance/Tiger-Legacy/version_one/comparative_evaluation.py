"""Prospective synthetic paired comparison. Offline only, no dashboard or production access."""
import json
import hashlib
from tiger_legacy import TigerLegacy

KEY = b"synthetic-comparative-lab-key-32-bytes-minimum"
CASES = [
    ("valid_grant", "alpha", "record", "analyst", "view", 100, True, False, False),
    ("wrong_purpose", "alpha", "record", "analyst", "edit", 100, False, False, False),
    ("expired", "alpha", "record", "analyst", "view", 200, False, False, False),
    ("revoked", "alpha", "record", "revoked", "view", 100, False, False, False),
    ("cross_tenant", "beta", "record", "analyst", "view", 100, False, False, False),
    ("owner", "alpha", "record", "owner", "view", 100, True, False, False),
    ("hidden_trustworthy", "alpha", "record", "analyst", "view", 100, True, True, True),
    ("hidden_biased", "alpha", "record", "analyst", "view", 100, True, True, False),
    ("hidden_missing", "alpha", "record", "analyst", "view", 100, True, True, None),
]
def evaluate():
    lab = TigerLegacy(KEY)
    lab.add_resource("r1", "alpha", "record", "owner", "synthetic only")
    lab.add_resource("r2", "beta", "record", "other", "synthetic only")
    lab.grant("g1", "alpha", "record", "owner", "analyst", "view", 150)
    lab.grant("g2", "alpha", "record", "owner", "revoked", "view", 150)
    lab.revoke("v1", "alpha", "record", "owner", "revoked", "view")
    rows = []
    for name, tenant, resource, principal, purpose, now, authorized, hidden, observation in CASES:
        actual = lab.authorize(tenant, resource, principal, purpose, now)
        if actual != authorized:
            raise AssertionError("fixture mismatch: " + name)
        baseline_allow = True  # deliberately permissive comparator, not a deployed GRI policy
        governed_allow = actual and observation is not True and observation is not None
        rows.append(dict(case=name, valid_authority=authorized, hidden_change=hidden,
                         observation=("missing" if observation is None else "positive" if observation else "negative"),
                         baseline_allow=baseline_allow, governed_allow=governed_allow))
    unauthorized = [r for r in rows if not r["valid_authority"]]
    legitimate = [r for r in rows if r["valid_authority"] and not r["hidden_change"]]
    severe = [r for r in rows if r["hidden_change"]]
    count = lambda group, key: sum(bool(r[key]) for r in group)
    metrics = {
        "unauthorized_allowances": {"denominator": len(unauthorized), "baseline": count(unauthorized, "baseline_allow"), "governed": count(unauthorized, "governed_allow")},
        "legitimate_task_allowances": {"denominator": len(legitimate), "baseline": count(legitimate, "baseline_allow"), "governed": count(legitimate, "governed_allow")},
        "hidden_change_allowances": {"denominator": len(severe), "baseline": count(severe, "baseline_allow"), "governed": count(severe, "governed_allow")},
        "governance_denials": sum(not r["governed_allow"] for r in rows),
        "synthetic_cases": len(rows),
        "evidence_chain_verified": lab.verify(),
    }
    return {"classification": "synthetic_fixture_demonstration_only", "comparator": "intentionally_allow_all_not_operational", "cases": rows, "metrics": metrics}
if __name__ == "__main__":
    print(json.dumps(evaluate(), indent=2, sort_keys=True))
