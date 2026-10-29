# Tiger Legacy Version One — Synthetic Security and Evidence Lab

**David A. Grand | Grand Research Institute**  
**Status:** Implemented and GitHub CI-tested synthetic reference implementation; not a deployed cybersecurity service.

## Components

- `tiger_legacy.py`: in-memory scoped consent, expiry, revocation, resource ownership, cross-tenant denial, HMAC-chained synthetic events.
- `reporting.py`: deterministic offline synthetic research report and integrity classification.
- `evidence_ledger.py`: SQLite transactional synthetic evidence ledger, unique event IDs, canonical SHA-256 chain, HMAC integrity, append-only triggers, backup/restore and exportable checkpoint.
- `tests/test_security.py`, `tests/test_reporting.py`, `tests/test_evidence_ledger.py`: **28 tests** total (8 + 8 + 12), including tampering, truncation, concurrency and rollback scenarios.

## Reproduction

From this directory: `python -m unittest discover -s tests -p 'test_*.py' -v`.

For the full research/dashboard suite, use `../verify_release.py` from a complete repository checkout and `gh attestation verify` as documented in [the evidence package](../REPRODUCIBLE-EVIDENCE-PACKAGE.md).

**Verified CI:** [GRI research quality run 40972535075](https://github.com/BazeletDave/ConsciousAI/actions/runs/40972535075) — 28 Tiger Legacy tests and 217 dashboard tests passed, full-checkout reproduction and signed provenance verification passed.

## Trust boundaries and limitations

- Caller-provided identities are not authenticated; no production authorization is possible.
- SQLite append-only triggers do not withstand privileged database control. An exported checkpoint detects truncation only if held independently and compared with the local ledger.
- HMAC keys are local research secrets, not managed operational credentials; no key rotation or independent escrow.
- The ledger is **not** integrated with real client data or live security operations; no independent checkpoint custodian is deployed.
- Signed GitHub provenance attests the synthetic snapshot's workflow lineage, not production security or scientific truth.
- No real client access, private media, scans, autonomous remediation or deployment is authorized.
- Original Training a Tiger experimental evidence remains separate and unmodified.

See [formal threat model](../FORMAL-THREAT-MODEL.md), [research methods](../RESEARCH-METHODS-AND-RESULTS.md), and [independent reproduction protocol](../INDEPENDENT-REPRODUCTION-PROTOCOL.md).
