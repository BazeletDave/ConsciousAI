# Comparative Evidence and Methods Protocol

**Status:** Proposed research protocol; adoption does not imply that any case has completed data collection, ethics review, or independent validation.

## Evidence classification

- **PRIMARY_DOCUMENT:** Official source, dated engineering artifact, policy, source code, or authenticated record; preserve URL, version, date, and exact claim supported.
- **DIRECT_OBSERVATION:** Firsthand observation with time, context, observer, and limitations recorded.
- **PARTICIPANT_REPORT:** Consent-based interview or testimony; separate participant perception from verified system behavior.
- **SECONDARY_SOURCE:** Reporting or scholarly literature; attribute assertions and distinguish allegations from findings.
- **SYNTHETIC_TEST:** Simulated inputs, unit tests, or benchmark runs; never extrapolate to production effectiveness without validation.
- **HYPOTHESIS:** Interpretive or causal proposition awaiting testing.
- **UNVERIFIED:** Unsupported, conflicting, or insufficiently documented claim; exclude from confirmed findings.

## Minimum case record

| Field | Requirement |
| --- | --- |
| case_id | Stable identifier and version |
| research_question | Narrow, falsifiable or explicitly exploratory |
| institutional_setting | Actors, rules, authority, incentives, affected stakeholders |
| source_register | Source ID, date, locator, author, claim, evidence class |
| methods | Sampling, measurement, comparison, collection protocol |
| governance | Consent, privacy, approval, conflicts, retention |
| results | Separate observed results, prototype output, and interpretation |
| limitations | Missing evidence, confounders, alternative explanations |
| remediation | How errors, corrections, and contested conclusions are recorded |

## Cross-case workflow

1. Frame a specific decision and the institution authorized to make it.
2. Identify decision makers, affected people, incentives, and appeal pathways.
3. Build a source register before drafting conclusions.
4. Classify each substantive claim by evidence type and verification status.
5. Specify observable variables: decision time, override rate, error rate, appeal access, trace completeness, stakeholder-reported fairness, and verified recovery status as relevant.
6. Document alternative explanations and disconfirming observations.
7. Review privacy, consent, security, and publication boundaries.
8. Publish findings only at the strength warranted by the evidence; version corrections and unresolved questions.

## Case-specific next data needs

- **001:** Original assignment requirements, code/version history, test fixtures, policy provenance, human-review workflow, and whether label rules are authoritative or illustrative.
- **002:** Consent-controlled driver interviews, de-identified trip offers, compensation and cost assumptions, and alternative explanations for apparent dispatch patterns.
- **003:** Capability schemas, approval/revocation events, controlled error scenarios, and independently reproducible audit traces.
- **004:** Inventory, upstream advisory verification, deployed image digest, active runtime inspection, worker recycle evidence, and post-remediation test results.

## Publication safeguards

Do not claim IRB approval, institutional sponsorship, government access, or measured causal effects without supporting documentation. De-identify participants and minimize personal information. Keep source citations and method details reproducible while withholding credentials, secrets, and exploit-enabling operational data.
