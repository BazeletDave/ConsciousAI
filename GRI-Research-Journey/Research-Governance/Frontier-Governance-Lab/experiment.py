"""Deterministic synthetic agentic governance evaluation and confusion metrics."""
from dataclasses import replace
import json
import random

from governance import Metrics, Policy, Request
from evidence import Evidence, EvidenceLedger, digest, verify_chain


def run_experiment(seed=20261025, n=500):
    if type(n) is not int or n <= 0:
        raise ValueError("n must be a positive integer")
    rng = random.Random(seed)
    policy = Policy()
    ledger = EvidenceLedger()
    confusion = {"TP": 0, "TN": 0, "FP": 0, "FN": 0}
    review_count = 0
    for i in range(n):
        metrics = Metrics(
            bias=round(rng.uniform(0, 0.24), 6),
            hallucination=round(rng.uniform(0, 0.09), 6),
            escalation=round(rng.uniform(0, 0.30), 6),
            autonomy=rng.randint(1, 5),
        )
        authorized = rng.random() > 0.10
        approved = rng.random() > 0.50
        request = Request(f"synthetic-{i}", "offline-agent", "simulated-action", authorized, metrics)
        ev = Evidence(f"synthetic-{i}", "synthetic-generator", "SYNTHETIC", f"seed:{seed};index:{i}", digest({"seed": seed, "index": i}))
        entry = ledger.append(request, policy, ev, approved)
        outcome = entry["decision"]["decision"]
        # Independent synthetic reference: hard limits or absent authorization are unsafe.
        reference_block = (not authorized or metrics.bias > policy.max_bias or metrics.hallucination > policy.max_hallucination or metrics.escalation > policy.max_escalation)
        predicted_block = outcome == "DENY"
        confusion[("TP" if predicted_block else "FN") if reference_block else ("FP" if predicted_block else "TN")] += 1
        review_count += outcome == "REVIEW"
    entries = ledger.export()
    tip = entries[-1]["entry_digest"]
    if not verify_chain(entries, tip):
        raise AssertionError("synthetic chain integrity failed")
    tp, tn, fp, fn = (confusion[k] for k in ("TP", "TN", "FP", "FN"))
    return {
        "schema_version": "gri.experiment.v1", "mode": "SYNTHETIC_ONLY",
        "seed": seed, "sample_size": n, "policy_version": policy.version,
        "confusion": confusion,
        "false_approval_rate": fn / (fn + tp) if fn + tp else None,
        "false_block_rate": fp / (fp + tn) if fp + tn else None,
        "review_rate": review_count / n,
        "ledger_tip": tip, "chain_verified": True,
        "limitations": "Reference labels derive from the same illustrative hard limits; results are consistency tests, not empirical safety estimates.",
    }


if __name__ == "__main__":
    print(json.dumps(run_experiment(), indent=2, sort_keys=True))
