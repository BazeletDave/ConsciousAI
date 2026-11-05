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


## Software and model update records

For the existing [AI Paradox framework](accelerating-ai-governance-paradox-living-research-framework.md#open-source-systems-software-updates-and-institutional-authority), record each material change as a versioned decision episode. Material changes include model or dependency versions, data provenance, classification rules, permissions, source access, and consequential workflow behavior. Record which categories apply; a documentation correction need not be represented as a production model change.

The proposed record contains: system and jurisdiction; change identifier and timestamps; previous and proposed versions; component rights and dependency inventory; responsible maintainer and authorized decision owner; evidence needed for the affected claims; tests and their precise scope; independent review status; deployment observations; unresolved dependencies; acceptance or deferral decision; correction responsibility; and recovery procedure with separate evidence of any completed recovery test. Preserve restricted evidence under appropriate custody rather than copying it into public records.

Report software verification, deployment verification, source availability, model evaluation, governance authorization, and institutional outcomes as separate statuses. Unknown or unmeasured values remain explicit. Record availability of review and appeal routes separately from observed use or effectiveness. A signed build or digest supports provenance; it does not establish model validity or fair outcomes.

For comparative studies, define the starting event and endpoint of each interval. Patch publication to independently verified runtime closure differs from deployment to completion of governance review, or a source failure to restoration of validated collection. Pending episodes are right censored, not zero duration and not automatically successful. Use incident grouped comparisons, account for severity and organizational capacity, and report missing evidence. Do not combine these intervals into an unvalidated institutional ranking.

This section defines research documentation and future evaluation requirements. It introduces no automatic approval, release, enforcement, fraud labeling, or scholarly publication mechanism. Existing frozen review baselines remain outside this extension.


## Ecosystem control and infrastructure comparison records

For the existing [national and enterprise ecosystem inquiry](accelerating-ai-governance-paradox-living-research-framework.md#from-open-source-opportunity-to-national-and-enterprise-ecosystem-control), record the following separately for models, application code, data pipelines, storage, compute, identity, encryption keys, monitoring, backups, and distribution platforms: legal owner; operator; location and relevant jurisdiction; dependency provider; maintainer; update authority; administrative access; audit and export rights; retention and deletion behavior; incident responsibility; and recovery owner. Mark unverified contractual or technical assertions explicitly.

Use the same task, data permissions, service requirements, observation window, and outcome definitions when comparing external platforms, cloud hosted open models, institution operated systems, and hybrid arrangements. Record actual contracts and deployed versions. Compare recurring operating expenses, transition costs, specialist staffing, infrastructure, security, and exit costs. Do not substitute published pricing for measured lifecycle cost.

Distinguish design documents from executed tests. A data export is not proof of portability until integrity and usability at the destination are checked; a backup is not verified recovery until restoration is exercised; domestic data location is not proof of exclusive administrative control. Report recovery time and recoverable data loss against predefined requirements. Keep unresolved episodes and missing observations visible. Any future independent evaluation must define its own approved scope and access before execution.
