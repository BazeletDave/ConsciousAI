# GRI Tiger Legacy | Security Governance and Institutional Assurance

**Research lead:** David A. Grand | **Grand Research Institute (GRI)**  
**Academic affiliation:** Thunderbird School of Global Management, Arizona State University. Independent GRI research; no Thunderbird/ASU endorsement, sponsorship, certification, or institutional validation implied.  
**Project:** Tiger Legacy Version One | **Research status:** synthetic research implementation, full-repository CI-tested, signed provenance verified in GitHub Actions. No production deployment or client-specific access.

## Research question

Can institutional cybersecurity assurance distinguish nominal compliance from demonstrated, traceable and contestable outcomes under authorization, revocation, evidence integrity and failure conditions? Tiger Legacy extends the GRI AI Paradox and Training a Tiger research architecture while preserving the original experiments as separate, frozen evidence.

## Current demonstrated implementation

- Synthetic in-memory tenant/resource authorization lab with scoped consent, expiration, revocation and HMAC hash-chained events; caller-provided principal strings are **not** authenticated identities.
- Deterministic offline synthetic reporting adapter with fail-closed classification and integrity validation.
- Separate read-only `GET /institutional/tiger-legacy` research reporting endpoint, independent from the original `/institutional/tiger-assurance` endpoint.
- Full-repository GitHub CI execution: 16 Tiger Legacy tests and 217 dashboard/research-system tests passed, including original Training a Tiger HTTP regression and integrity-failure checks.
- Signed GitHub provenance generated, uploaded to Sigstore Rekor and verified through GitHub CLI in CI.

## Evidence and independent review

- [Current engineering and research status](DEVELOPMENT-STATUS.md)
- [Reproducible evidence package](REPRODUCIBLE-EVIDENCE-PACKAGE.md)
- [Release reproduction script](verify_release.py)
- [Research and engineering quality standards](ENGINEERING-RESEARCH-STANDARDS.md)
- [Mission and integration guardrails](MISSION-AND-INTEGRATION-GUARDRAILS.md)
- [Version One scope](VERSION-ONE.md)
- [Original baseline](COMPATIBILITY-BASELINE-2026-10-29.md)
- [CI run with independent GitHub CLI attestation verification](https://github.com/BazeletDave/ConsciousAI/actions/runs/40972028096)
- [Draft integration pull request #92](https://github.com/BazeletDave/ConsciousAI/pull/92)

## Research component boundaries

| Source | Reuse boundary |
| --- | --- |
| Training a Tiger assurance experiment | Preserved original experimental findings; methods inform negative tests, **not** production cybersecurity efficacy |
| Agentic Governance Engine | Canonicalization and evidence-chain research patterns; no automatic integration of its capability policy |
| Agentic Authorization Prototype | Research authorization model; no trusted production identity |
| CISA 2030 evidence ledger | Existing collector rejects synthetic records; not reused as Tiger Legacy evidence store |
| PHP2Shell research | Vulnerability-evidence methodology, not certification of remediation |
| GRI dashboard | Read-only synthetic reporting; not a security operations or authorization control plane |

## Explicit limits

No client identifiers, confidential audit details, private media, secrets, scans, real remediation or external system access are part of this project. Signed provenance authenticates artifact lineage under the GitHub trust model; it does not certify scientific correctness, operational effectiveness or independent security review. Production security remains **unmeasured**. A general-purpose assurance layer cannot replace fixes in a vulnerable underlying application.

## Next release gates

Independent external reproduction; threat model and trusted identity boundary; durable and independently anchored synthetic evidence; expanded adversarial testing; formal methods and limitations for peer review; explicit human authorization before any production merge or deployment.

**All results are to be classified by evidence: proposed, implemented, CI-tested, independently reviewed or deployed.** This research is independently conducted by GRI.

## Next research milestone: threat model and durable evidence

The following additional research artifacts have been committed on the **same development branch**:

- [Formal synthetic STRIDE threat model](FORMAL-THREAT-MODEL.md)
- [SQLite durable synthetic ledger](version_one/evidence_ledger.py) and [12 adversarial ledger tests](version_one/tests/test_evidence_ledger.py)
- [Independent reproduction protocol](INDEPENDENT-REPRODUCTION-PROTOCOL.md)
- [Research methods, hypotheses and limitations](RESEARCH-METHODS-AND-RESULTS.md)

**Verification scope:** These newly added artifacts must pass their own latest-commit CI before their test results can be marked verified. External independent reproduction requires an actual reviewer outside the implementation team and remains uncompleted until documented. Do not equate GitHub-hosted CI with independent peer review.
