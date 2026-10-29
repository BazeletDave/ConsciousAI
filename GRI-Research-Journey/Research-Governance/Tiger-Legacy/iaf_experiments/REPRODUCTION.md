# IAF V1.1 — Synthetic evaluation and independent reproduction

**Status:** Implemented experiment fixtures and scripts, awaiting CI and independent execution. No live client information or external access. These are deliberately small deterministic policy experiments, not a trained ML model, RL agent, cybersecurity product, or external audit.

## Run without dependencies

From this directory:

```sh
python3 runner.py --output results.json
python3 -m unittest discover -s . -p 'test_*.py' -v
sha256sum fixtures.json runner.py test_runner.py results.json
```

`results.json` is generated locally, not checked in; record interpreter version, platform, commit SHA, hashes and full command output in the reviewer report. For portability on systems without `sha256sum`, compute SHA-256 using Python's hashlib.

## Design and ML/RL governance boundaries

- **Baseline:** technical-only checks accept token and consent, ignoring mandate, revocation, conflict, separation of duties and changed action.
- **Intervention:** checks all of those properties on each proposed action; denies any action except synthetic `read`.
- **Adaptive-agent surrogate:** the fixture `adaptive_agent_escalation` simulates a policy-relevant action change from read to export. It does **not** implement learning, optimization, a trained ML classifier, or RL policy.
- **Metrics:** unsafe blocked (true positive), false approval (false negative), safe allowed (true negative), and false denial (false positive). The expected decision is hand-labeled and visible.
- **Interpretation:** zero errors on these eight hand-authored fixtures cannot establish general security performance or external validity.

## Independent reproduction procedure

1. Reviewer who did not author the experiment checks out the exact proposed Git commit.
2. Confirm fixtures are explicitly synthetic, contain no external identifiers, and review each expected label without consulting implementation output.
3. Run commands above in a fresh Python standard-library environment. Preserve SHA-256, exit codes and results.
4. Mutate one scenario at a time (revoke consent, remove mandate, introduce conflicting authority, change action to export), rerun and compare expected behavior.
5. Record discrepancies, false approvals, any ambiguous labels, Python version, UTC timestamp, reviewer role, and commit.
6. Publish a signed review record only with reviewer authorization. Do not describe self-run CI as an independent audit.

## Follow-on work (not yet implemented)

- Seeded, stateful multi-step agent trajectories and action-by-action policy re-evaluation.
- A genuine ML model / RL agent with constrained training, out-of-distribution tests, and transparent policy snapshots.
- Evidence-ledger integration and tamper/replay detection, without modifying existing immutable research.
- Source-verified faculty attribution and research-methods review.
- CI integration, cross-platform replication, and reviewed dashboard publication.

This directory supplements the IAF traceability matrix and existing Tiger Legacy work. It does not modify existing authorization code or production routes.
