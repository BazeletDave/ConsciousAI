# Independent Inspection Register — Frontier Governance v0.2.0
**Inspection date:** 2026-10-25  
**Disposition:** RESEARCH CANDIDATE — NOT PRODUCTION APPROVED

## Inspection basis
- GRI candidate Rego and Python implementations in the v0.2.0 research archive; inspected source rather than relying only on previous summaries.
- GOPAL `AGENTS.md` (upstream authoring contract): versioned package path, matching Rego test, `# METADATA`, `default allow := false`, `report` via shared reporting helper, OPA check and Regal lint.
- Microsoft agent-governance-toolkit README and MIT license.
- GOPAL README and Apache-2.0 license claims; full license notice and contribution compliance still require release-time confirmation.

## Inspection findings
| ID | Severity | Finding | Evidence / required action | State |
| --- | --- | --- | --- | --- |
| FG-01 | Critical | Elevated-risk action can be allowed by any highest-authority `allow` instruction. Risk escalation is only applied when no instructions exist. | `rego/policy.rego` result branch and `python/frontier_governance/policy.py` `if instructions` branch precede elevated-risk fallback. Define an explicit risk-priority policy and test it. | OPEN |
| FG-02 | High | Four priority levels are declared but not fully resolved. Most instruction-driven cases return `organizational` without computing competing priority applicability. | Rego `priority` map is unused for selection; Python has no priority input or resolution algorithm. | OPEN |
| FG-03 | High | Input trusts authority, effect and constraint status without authenticated source or applicability evidence. | Both engines accept caller-supplied classifications. Require signed/attested facts and host-level identity binding. | OPEN |
| FG-04 | High | Rego is not proven GOPAL-drop-in compatible. | GOPAL requires matching directory/package, policy metadata, `allow` and reporting helper output, OPA/Regal CI. Candidate uses `gri.frontier.v1` and `result`. Build a separately tested adapter. | OPEN |
| FG-05 | High | OPA parse/check/test, Regal lint and cross-language equivalence have not been executed. | Environment lacks OPA; prior Python tests do not validate Rego. | OPEN |
| FG-06 | High | Audit SHA-256 is an integrity fingerprint, not a signature or immutable audit log. | Python `audit_record` hashes input; no trusted signer, verifier, key management, storage retention or append-only ledger. | OPEN |
| FG-07 | Medium | Reported Python test count is limited and not comprehensive coverage. | Earlier 14 passing tests do not establish branch/decision coverage, adversarial inputs, or production acceptance. | OPEN |
| FG-08 | Medium | The `reasoning_obstruction` rule must not imply disclosure of private chain-of-thought. | Define auditable decision explanations and policy evidence without protected internal reasoning disclosure. | OPEN |
| FG-09 | Medium | Integration with AICertify, Microsoft runtime and regulatory policy conjunction is not end-to-end demonstrated. | Design documentation only; adapter contracts and test harness required. | OPEN |
| FG-10 | Medium | Repository branch contains integration documentation but not the full candidate source package. | Publish source, tests and CI in a dedicated PR after remediation; avoid claiming upstream contribution. | OPEN |

## Cross-reference and authority map
| Source | What it actually establishes | Does not establish |
| --- | --- | --- |
| [GOPAL](https://github.com/Principled-Evolution/gopal) `AGENTS.md` | Expected Rego layout, tests, report contract and CI gates | Candidate compatibility or acceptance |
| [AICertify](https://github.com/Principled-Evolution/aicertify) | Companion assessment project identified by GOPAL documentation | Tested GRI integration |
| [Microsoft Agent Governance Toolkit](https://github.com/microsoft/agent-governance-toolkit) README | Public-preview runtime governance capabilities and SDK orientation | Implemented GRI adapter or certification |
| [OPA](https://www.openpolicyagent.org/docs) | Deterministic policy engine and test tooling | Truthfulness of caller-supplied facts |
| [NIST AI RMF](https://www.nist.gov/itl/ai-risk-management-framework) | Voluntary risk-management framework | Formal regulatory certification |
| [EU AI Act](https://eur-lex.europa.eu/eli/reg/2024/1689/oj) | Binding legal instrument within applicable scope | Universal applicability to all candidate use cases |
| GRI v0.2.0 candidate | Research implementation and limited Python test evidence | Independently verified lab policies or production security |

## Release gates — all mandatory
1. Resolve FG-01/FG-02 with a written policy specification and negative tests.
2. Verify schema validation, trusted attestation and instruction applicability.
3. Execute OPA check/test, Regal lint, Python tests and differential parity fixtures in pinned CI.
4. Implement and validate GOPAL adapter output and independent mandatory-policy conjunction.
5. Demonstrate runtime interception, revocation, interruption and failure behavior.
6. Create signed append-only audit events, retention rules, verifier and replay tests.
7. Verify SPDX licensing, upstream contribution process, attribution and source metadata.
8. Publish coverage matrix with test evidence, versions, hashes and reviewer sign-off.

## Inspection conclusion
The work is a legitimate GRI research contribution but **must not be described as production-grade, drop-in compatible, fully audited, or upstream accepted**. FG-01 is a substantive behavioral flaw; release is blocked pending remediation and re-testing. Independent inspections should prefer this exception register to unqualified promotional language.
