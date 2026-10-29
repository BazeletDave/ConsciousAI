# GRI Tiger Legacy | Verified Initial Compatibility Baseline

**Date:** 29 October 2026  
**Scope:** Repository source inspection and local execution of synthetic Tiger Legacy regression tests. No dashboard changes or deployment.

## Executed regression suite

The Tiger Legacy Version One `tiger_legacy.py` and `tests/test_security.py` source were retrieved from the existing `research/tiger-legacy-foundation-2026` branch, reconstructed into a temporary local Python test directory and executed with `python -m unittest discover -s <temporary-directory> -p test_security.py -v`.

**Result:** 8 tests run, 8 passed, 0 failures, exit code 0. This is a local reconstruction of retrieved source, not a GitHub Actions CI execution, an independent security audit, or a production validation. An unrelated optional spreadsheet runtime initialization warning appeared in stderr; unittest still exited successfully.

Covered: cross tenant grant rejection, forged grant rejection, grant expiry and revocation, default deny, tamper detection, missing event detection, event identifier replay rejection, synthetic summary.

## Dashboard interface inspection

Inspected the `main` branch:
- `GRI-Research-Journey/Research-Governance/ConsciousAI-Research-Systems/server.py`
- `tiger_assurance_bridge.py`
- `tiger-assurance.js`
- `operational_health.py`
- Research Systems `README.md`

**Existing endpoint:** `GET /institutional/tiger-assurance` calls `tiger_assurance_bridge.snapshot(ROOT)`. On specified integrity errors, the server returns HTTP 503 with `tiger_assurance_integrity_unavailable` and `model_promoted: false`. This is an existing Training a Tiger experimental reporting interface, not a Tiger Legacy security endpoint.

**Integrity contract:** The bridge checks an exact artifact manifest and SHA-256 digests, verifies retained result and summary agreement, reproduction record and source freeze provenance, and asserts zero authorized operational actions and no promoted model. It returns an explicit status indicating artifact matching is not independent validation.

**Presentation contract:** `tiger-assurance.js` fetches the endpoint with no-store, renders synthetic metrics and limitations, and falls back to an integrity-unavailable message. Preserve this behavior.

**Health contract:** `GET /health` validates required local JSON files, not source freshness or independent research accuracy. `GET /health/collections` checks collection timestamps with a six-hour freshness window and is not an authorization gate.

**Deployment contract:** Render `gri-global-intelligence` service runs the Python standard-library server from `ConsciousAI-Research-Systems`, auto-deploying `main`; the Tiger Legacy development branch is not deployed by this service. Do not change the existing server or scheduled collection jobs until integration tests are available.

## Compatibility disposition

**Compatible in principle:** A separate read-only, synthetic aggregate snapshot adapter with explicit provenance, scope, integrity status and limitations can follow the established dashboard pattern.

**Not yet verified:** Import compatibility, adapter code, endpoint integration, data schema, client authentication, persistence, full dashboard regression, CI, independent audit, production safety and live endpoint response.

**Proposed adapter:** a separate Tiger Legacy synthetic report builder produces an offline, versioned JSON artifact containing test run ID, commit SHA, Python version, executed test count, pass/fail, scope, synthetic-only flag, evidence digest and limitations. The dashboard may consume it read-only after verifying an expected manifest and integrity digest. Never expose raw client data, HMAC keys, grant identities or media.

## High-priority findings

1. The prototype accepts caller supplied principal strings and does not authenticate identities; it is **not production authorization**.
2. The in-memory HMAC chain has no durable storage or independent trust anchor.
3. The tests cover eight selected cases, not complete threat modeling, cross-process isolation, concurrency or restoration.
4. Existing Tiger Assurance findings concern synthetic ML experiment outcomes and must not be interpreted as security assurance scores.
5. A green Render deployment only establishes deployment status, not verified operation of Tiger Legacy.

## Next gate

Add a deterministic, offline Tiger Legacy verification report generator and test it; inspect existing dashboard tests and route expectations; implement a separate read-only adapter on the development branch; run complete dashboard regressions before any merge or deployment. Preserve Training a Tiger source and findings unchanged.
