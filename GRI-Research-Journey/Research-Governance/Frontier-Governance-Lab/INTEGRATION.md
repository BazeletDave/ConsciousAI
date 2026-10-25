# Evidence, experiments, and assurance integration | v0.2

## Integration boundaries

This is an **offline adapter** to existing GRI research capabilities, not a replacement of them.

- **Executable Governance:** retains its event schema and intervention policies. This adapter's `decision` envelope records policy version and canonical digest; future schema mapping requires explicit field-by-field compatibility tests.
- **Inference Integrity:** already demonstrates SHA256 chained inference records. The new `EvidenceLedger` follows the same integrity pattern for policy evaluations and supports verification against a separately retained trusted tip. It does **not** import or alter that module.
- **Agentic Authorization Prototype:** continues to own tool-time intent and resource constraints. The lab's `authorized` and `human_approved` booleans are **synthetic flags**, not cryptographic authority.
- **Institutional intelligence dashboard:** no runtime or ingestion changes. Future read-only evidence integration requires source IDs, review status, retention controls, and provenance verification.

## Reproducible experiment

Run `python -m unittest discover -p 'test_*.py' -v` and `python experiment.py` from this folder. Fixed seed, sample size, confusion counts, false approval/block rates, review rate and ledger tip are produced. Synthetic reference labels use the same illustrative hard policy limits as the policy evaluator, so the reported classification metrics are **internal consistency checks**, not external validation.

## Assurance maturity and remaining gaps

1. Implemented: canonical policy decision digests, chained evidence envelope, tamper/reordering tests, trusted tip comparison interface, synthetic reproducibility.
2. Not implemented: durable append-only persistence, signed third-party anchors, verified actor identities, real tool interception, empirical benchmarks, adversarial distribution-shift datasets, consented participant data.
3. Before production: independent security review, signed approvals, separate evidence storage and cryptographic anchoring, cross-module contract tests, privacy threat modeling, incident response and rollback.

No claim of regulatory certification, official institutional endorsement, or measured production safety is made.
