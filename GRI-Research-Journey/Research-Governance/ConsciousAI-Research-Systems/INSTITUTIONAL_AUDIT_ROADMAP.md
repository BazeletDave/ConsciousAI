# GRI institutional audit infrastructure — implementation record

Status: **research infrastructure provisioned; production assurance NOT certified**.

## Render database
- Instance: `gri-governance-audit-research`
- Resource ID: `dpg-dbf0a57b9u1s73b66ulg-a`
- PostgreSQL 18, Virginia, free plan.
- Created 2026-10-25; provider reports expiry **2026-11-24**. This is a **temporary evaluation database**, NOT durable archival storage. No HA or replicas.
- Do not ingest production evidence until a paid durable plan, retention, backups, access controls, restore testing and key management have been approved and verified.
- No database credentials belong in this repository. Keep all connection strings in a managed secret store.
- The existing public Render service is not connected to this database and must remain unchanged pending migration tests.

## Audit subsystem
`institutional_audit.py` is an isolated SQLite cryptographic research prototype. Its five adversarial tests run through `.github/workflows/gri-institutional-audit-tests.yml`. It intentionally does not power the public dashboard. JSON serialization is deterministic for a restricted data subset but **not RFC 8785**. Signing keys in tests are ephemeral; production key custody is not implemented.

## Acceptance gates
1. GitHub Actions tests independently confirmed passing; block production releases on failing tests (requires effective protected branch / deployment policy, not just a CI workflow).
2. Database upgrade to durable, backed-up service with verified restore, scoped credentials and retention.
3. Trusted external signing keys and registry, rotation and revocation; externally anchored chain checkpoints.
4. End-to-end migration and recovery tests against an isolated PostgreSQL test environment; no simulated evidence in operational tables.
5. Real labeled ML evaluation data with lineage, model version, sampling design, confidence intervals, fairness/drift where appropriate, independent review.
6. Security review, threat model, access controls, rate limits, resilience testing, and release approval.

## Governance classifications
- **implemented** = code exists, not necessarily operational
- **test_passed** = reproducible automated tests with recorded workflow evidence
- **operational** = observed in a running environment
- **independently_verified** = external reviewer and source evidence documented
- **not_connected** = absent operational source; must not be presented as verified

The GRI research platform must not assert independent certification, real-world ML accuracy, immutable evidence retention or production security solely because these components have been created.
