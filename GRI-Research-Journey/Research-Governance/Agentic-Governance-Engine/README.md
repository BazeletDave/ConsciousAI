# GRI Agentic Governance Engine v2

**Grand Research Institute | Independent research and education prototype | 22 October 2026**

This module demonstrates how delegated agent authority can be constrained before a simulated action is accepted, and how an external reviewer can reproduce the decision and verify an in-memory SHA-256 hash chain.

**No production authorization, live transaction execution, penetration testing, or security certification is claimed.** No credentials, financial accounts, or government infrastructure are accessed.

## Research design

Institutional rules → signed and scoped capability → deterministic policy evaluation → atomic volume reservation → append-only event evidence → independent verification.

The Nelson institutional approach informs the research questions about rules, actors, interests, enforcement and institutional adaptation. This independent GRI implementation is not an endorsement by Thunderbird or faculty.

## Implemented

* HMAC-signed scoped research capabilities; agent and asset identity matching; validity windows and revocation
* Decimal monetary validation and per-action, global rolling-hour, and per-capability rolling-hour limits
* Lock-serialized authorization and reservation to prevent concurrent overspending within one process
* Token-bucket velocity breaker and explicitly approved manual reset
* Idempotency rejection by action ID
* Canonical SHA-256 linear hash-chain ledger with a verification routine
* Loopback-oriented FastAPI simulation endpoints and regression tests

## Run locally

From the repository root:

```bash
python -m pip install -r GRI-Research-Journey/Research-Governance/Agentic-Governance-Engine/requirements.txt
cd GRI-Research-Journey/Research-Governance/Agentic-Governance-Engine
python -m unittest test_engine
uvicorn api:app --host 127.0.0.1 --port 8000
```

Run the commands from the module directory. The API is restricted to local demonstration.

## Important limits and remaining work

This is an **initial backend research implementation**, not a complete production platform. The in-memory ledger is not durable or independently anchored; a privileged attacker could rewrite and rehash it. The HMAC key is for local demonstration, not an institutional signing service. A single process lock does not protect multiple replicas. The demo API has no production identity provider or operator RBAC. A live frontend integration, persistent transactional datastore, external ledger anchoring, secure key management, container hardening, CI and deployment verification remain necessary.

The API must not be exposed to the public internet without authentication and deployment hardening. The demo capability issuance endpoint is intentionally insecure outside a controlled laboratory.

## Evidence classification

| Evidence | Classification |
| --- | --- |
| Source code and unit tests | Implemented, subject to CI execution |
| Cryptographic hash chain | Locally verifiable, not independently anchored |
| Real world attack detection | Not tested |
| Independent audit certification | Not performed |
| Performance or latency benchmarks | Not established |
| Production security authorization | Not granted |

## Case study scope

Research cases can compare certificate authority randomness failures, PHP remediation assurance, and delegated banking agent access. Each case requires independent primary source evidence and explicit separation of confirmed facts, claims and hypotheses.
