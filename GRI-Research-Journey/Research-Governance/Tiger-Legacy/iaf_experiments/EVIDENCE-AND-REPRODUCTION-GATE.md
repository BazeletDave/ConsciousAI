# IAF V1.1 — Evidence and Reproduction Gate

**Status:** Executable synthetic evidence package; independent reproduction remains pending.

Run from this directory using only the Python standard library:

```sh
python3 verify_research.py > evidence-report.json
```

The script runs discovered unit tests, exits nonzero if any test fails, and emits a deterministic research report only after passing tests. It records fixture hashes, Python version, baseline and intervention decisions, and event-chain replay verification. Retain the commit SHA, command output, file hashes, and independent reviewer signoff.

The trace chain is **not** independently anchored. A privileged actor who can replace the full report could recompute the hashes. The experiment does not use real identity, real client data, a trained ML model, or an RL policy.

## Milestone acceptance gates

- [x] Synthetic fixture and stateful policy experiments committed.
- [x] Initial research workflows passed on the preceding commit.
- [ ] Latest commit CI green.
- [ ] Evidence report reproduced independently in a fresh environment.
- [ ] Separate reviewer validates expected labels and intentional tamper failures.
- [ ] Synthetic evidence-ledger integration and adversarial tests.
- [ ] Genuine ML/RL policy evaluation with held-out trajectories.
- [ ] Source-verified academic attribution and final human review.

Do not describe this package as independently certified, or merge/deploy without explicit review.
