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

## Evidence extension: Lazarus dormant-neuron model backdoor (11 November 2026)

**Classification:** External experimental cybersecurity evidence; bounded relevance to existing AI Paradox and Tiger Legacy assurance questions. Not a GRI reproduction, deployment finding, certification, or proof of the broader AI Paradox hypothesis.

Microsoft's Lazarus research describes targeted changes to a small number of model neurons that can conditionally redirect an AI agent's output when a specified trigger occurs. The published demonstration depicts an otherwise routine working-directory request producing a chained remote-script execution command. The example concerns model-weight integrity and downstream agent authority, rather than an ordinary prompt injection. Reported experimental attack and detection measurements are specific to the authors' models, configurations and evaluation conditions; they must not be generalized to all deployed agents.

**Institutional interpretation:** Correct responses on ordinary prompts cannot, by themselves, establish absence of dormant malicious behavior. This is convergent evidence for GRI's existing distinction between locally acceptable model performance and independently verified institutional control. It does not establish that GRI's own systems, Microsoft Foundry models or any production deployment have been compromised.

**Existing control crosswalk:**

| Existing assurance boundary | Lazarus relevance and evidence requirement |
| --- | --- |
| Supply-chain and build provenance | Record model source, version, checkpoint digest and custody; provenance attests origin but does not prove benign weights |
| Authorization and least privilege | Restrict shell, network and sensitive tool permissions; require explicit authorization for consequential actions |
| Independent review | Treat behavioral tests as incomplete; commission independent model integrity and trigger robustness evaluations where feasible |
| Evidence ledger and checkpoint custody | Preserve independently held model hashes, evaluation configuration, reviewer findings and subsequent corrections |
| Read-only public reporting | Publish only source-attributed, non-operational summaries; no live exploit payloads or unsupported security assurances |

**Limitations and follow-up:** No model-weight scanning, dormant-neuron detection, red-team reproduction or production controls are implemented by this documentation update. Existing synthetic regression results remain unchanged. Any proposed implementation requires separate scope, authorization and validation. Model provenance, runtime isolation and permissions are complementary controls, not guarantees against a hidden backdoor.

**External sources:** [Microsoft Research account](https://msft.it/6181ahpxW); [Microsoft Threat Intelligence mitigation guidance](https://msft.it/6180ahpxm); [Microsoft research overview](https://msft.it/6189ahpxl). The cited authors' findings are external evidence and are not attributed to GRI.
