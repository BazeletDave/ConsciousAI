# Secure Evidence Infrastructure v0.2 — deployment gate

This milestone implements **offline controlled intake, consistent SQLite backup, signed backup manifests, and independent restore verification**. It does **not** implement production identity federation, encryption, offsite replication, or network ingestion. A signed manifest provides integrity, **not confidentiality**.

## Implementation boundaries
- `secure_evidence.intake` performs basic preflight validation and delegates artifact byte hashing and collector role enforcement to the existing ledger. Full schema checks and verified identity remain required.
- `export_backup` uses SQLite's online backup API, refuses overwrite, and emits SHA256/HMAC manifest. Keep signing keys out of source control and backups.
- `restore_backup` verifies manifest authenticity and payload integrity, refuses overwrites, and verifies restored ledger signatures and chain head.
- A privileged database administrator can delete a database, manipulate local files, or access data; local role keys are not an external identity provider.
- **No artifacts are stored** by the ledger; only their digest is retained. Backups are local until an independent, encrypted offsite target is explicitly provisioned.

## Before enabling real intake
1. Choose identity provider and authenticated role mapping with separation of duties.
2. Provision encrypted persistent storage with managed secrets, key rotation, and least-privilege access.
3. Set an independent offsite encrypted backup target and recovery schedule; run documented restore drills.
4. Add complete evidence schema validation, source retention and privacy/consent review, rate limiting and signed audit checkpoints.
5. Keep Render dashboard read-only and all six assurance domains `unmeasured` until independent validation of real authorized data.

Tests: `python -m unittest -v test_evidence_ledger.py test_evidence_validation.py test_secure_evidence.py` from this directory.
