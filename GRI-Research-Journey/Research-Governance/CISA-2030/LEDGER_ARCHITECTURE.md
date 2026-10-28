# Authenticated Evidence Ledger | Prototype v0.1

An **offline, single-process, local SQLite prototype**. Does not enable production ingestion, public APIs, automatic collection, or publication.

## Design
- Distinct collector, reviewer, and auditor roles, authenticated by externally supplied 32+ byte HMAC keys.
- Collector submits authorized record plus original artifact bytes. Actual bytes are SHA256 checked against the claimed source digest. Artifact bytes are **not stored**; retain them securely elsewhere.
- Reviewer makes a separately attributed approve/reject decision with rationale. Auditor sees only approved records after integrity verification.
- SQLite append-only triggers and a chained SHA256/HMAC event log make accidental edits detectable. Not a tamper-proof database against privileged administrators, compromised keys, or deletion of the whole database.
- No real research records are bundled. No public dashboard indicator is promoted.

## Constraints before deployment
- Implement an external identity provider, secret rotation and protected key storage; this prototype trusts the caller-provided role map.
- Encrypt storage and independent offsite backups; test restore, concurrency, chain checkpoints, and disaster recovery.
- Implement reviewer access to the original artifact, legal authority/consent checks, retention and redaction policy, independent review proof, correction/supersession events, and auditable approval workflow.
- Add strict record-schema validation using `evidence_validation.py` before any empirical reporting. The ledger currently checks authorization presence and byte hash, **not** the full empirical schema or truthfulness.
- Never place private interview records, credentials, protected infrastructure logs, or sensitive data in GitHub.

Run from this directory: `python -m unittest -v test_evidence_ledger.py`.
