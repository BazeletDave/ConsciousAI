# Tiger Legacy Version One — Formal Synthetic Threat Model

**Research lead:** David A. Grand, Grand Research Institute  
**Academic context:** Thunderbird School of Global Management, Arizona State University; no sponsorship or certification implied.  
**Method:** Assets, actors, boundaries, STRIDE threat classification, security invariants, negative-test traceability.  
**Scope:** Offline synthetic reference lab, SQLite evidence ledger, signed CI provenance, read-only public research dashboard. No real client system or real media.

## Assets and security invariants

| Asset | Required invariant | Evidence |
| --- | --- | --- |
| Tenant/resource ownership | Cross-tenant access denied by default | `test_security.py` |
| Scoped consent | Purpose, expiry, revocation and owner approval enforced in fixture | `test_security.py` |
| Synthetic event history | Monotonic sequence, unique IDs, chain integrity, valid HMAC | `test_evidence_ledger.py` |
| Durable local record | Transactional SQLite commits, re-open and backup/restore | `test_evidence_ledger.py` |
| Public research summary | Synthetic only; no authority, secrets or private content | `test_reporting.py`, `test_tiger_legacy_bridge.py` |
| Build provenance | Artifact digest linked to GitHub CI identity | Signed attestation + `gh attestation verify` |

## Actors and trust boundaries

- **Untrusted caller:** Can provide arbitrary tenant, principal, resource, purpose and timestamp inputs. In-memory lab does not authenticate them.
- **Research operator:** Can generate synthetic fixtures and run local tests. Local operator is not an independent auditor.
- **Local process / filesystem:** SQLite and HMAC key reside under local execution control. Database administrator or compromised host can bypass SQLite triggers, replace database, or steal signing key.
- **CI and repository:** GitHub Actions signs workflow provenance. A compromised repository or CI administrator may generate signed but misleading artifacts.
- **Independent reviewer:** Must retrieve evidence from independently controlled custody and verify source revision, digest, signature, reproducibility and scientific interpretation.
- **Public dashboard visitor:** Can read synthetic summary only; no client authorization, mutation or remediation privileges.

## STRIDE analysis

| Threat | Attack scenario | Mitigation demonstrated / remaining gap |
| --- | --- | --- |
| Spoofing | Caller claims to be resource owner | **Gap:** no trusted authentication; never deploy as real authorization |
| Tampering | Event payload altered, report digest replaced | HMAC and pinned manifest detect certain changes; privileged compromise can replace both |
| Repudiation | Operator denies action or rewrites history | Signed CI provenance and external checkpoint improve accountability; operator identity for individual events unverified |
| Information disclosure | Tenant content or private identifiers leak to public dashboard | Synthetic aggregate contract; no real client data; real media boundary not implemented |
| Denial of service | Database locked or malformed input exhausts resources | SQLite bounded busy timeout; no quotas, rate limiting or resilience testing |
| Elevation of privilege | Owner string spoofed; grant authorization bypass | Default-deny fixture only; real principal trust boundary missing |
| Rollback/truncation | Ledger tail removed then re-signed | External checkpoint comparison detects mismatch **only if checkpoint is held outside attacker control** |
| Supply-chain compromise | Malicious CI produces valid signed artifact | Signature proves workflow identity, not semantic correctness; independent code review required |

## Risk ranking

**Critical before real integration:** authenticated identity, tenant context derived from trusted session, key management, operational authorization and approval boundaries.  
**High:** independent checkpoint custody, immutable backups, rollback detection, media access controls, audit retention and recovery drills.  
**Medium:** malformed-input hardening, concurrency stress, denial-of-service controls, dependency pinning and monitoring.  
**Residual:** Compromised CI/repository and insider threats require independent oversight and separate custody.

## Explicit negative findings

- In-memory consent lab cannot verify a human principal.
- SQLite triggers are not tamper-proof against a database administrator.
- HMAC chain integrity alone cannot detect an attacker deleting the entire chain without a separately held checkpoint.
- GitHub provenance is independent of the local snapshot digest but is not a third-party cybersecurity certification.
- A successful synthetic regression suite does not establish security of an external application.

## Acceptance criteria for next independent review

Reproduce exact CI test results; verify GitHub attestation and signer identity; independently retain and later challenge a checkpoint; demonstrate tamper/replay/rollback detection; document unmitigated spoofing and privileged-host attacks. Publish failures as well as successes. No production release without a separate security assessment and explicit approval.
