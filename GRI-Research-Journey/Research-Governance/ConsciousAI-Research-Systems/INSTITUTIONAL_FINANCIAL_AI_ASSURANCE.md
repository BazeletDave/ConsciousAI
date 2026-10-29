# Institutional Financial AI Assurance | GRI v0.1

**Status:** Research prototype specification; not audited, certified, connected to live financial systems or authorized for autonomous decisions. **Owner:** Grand Research Institute / David A. Grand.

## Purpose
Translate the October 16, 2026 Warsh–Georgieva IMF dialogue into testable controls for AI use in financial institutions. Link to Training a Tiger as a subordinate assurance application, not a claim of regulatory endorsement.

## Assurance domains and evidence
| Domain | Required evidence | Failure trigger |
|---|---|---|
| Provenance | Dataset owner, source URL/identifier, observation date, retrieval date, vintage, license | Missing source or vintage |
| Measurement | Units, population, lag, uncertainty interval, revisions | Unstated lag or unsupported precision |
| Scenario coverage | Inflation, productivity, financial-stability downside, energy shock, cross-border spillover | No downside scenario |
| Model validation | Baseline, holdout period, out-of-sample results, calibration, drift | No independent validation |
| Institutional challenge | Independent reviewer, disagreement record, alternatives considered | Reviewer absent |
| Human authority | Named decision owner, escalation threshold, override and rollback | Automated consequential decision without human gate |
| Resilience | Grid/cyber/provider concentration, recovery objectives, stress tests | Critical dependency untested |
| Accountability | Audit trail, remediation owner, status and retest | Unresolved high-risk finding |

## Deterministic control gates
Each domain is **not measured**, **evidence pending**, **pass**, or **fail**. A pass requires a linked, reviewed evidence record, not merely a narrative claim. Missing evidence cannot be silently scored as pass. Aggregate status is **blocked** if any high-criticality gate fails or if human authority/provenance is not measured. No overall numerical assurance score without a validated scoring rubric.

## Three-scenario minimum
1. AI capital expenditure rises before productivity, increasing power demand, prices and financing exposure.
2. AI valuations reverse; concentrated creditors and suppliers face correlated losses.
3. Long-run productivity gains emerge unevenly across countries owing to energy, debt, compute and institutional constraints.

For each: state shock, horizon, transmission channel, exposure, counterevidence, leading indicators, owner, mitigation and residual risk. Treat each as a hypothesis until measured.

## Training a Tiger mapping
Tiger's assurance model may reuse the provenance, challenge, escalation, adverse-scenario and audit controls. It remains subject to the same independent review and evidence requirements; this framework does not import or publish confidential insurance, family, donor or client information.

## Research and governance boundaries
Sources: [GRI Warsh–Georgieva case study](../../Integrated-Research-Journey/2026-10-16-warsh-georgieva-ai-investment-policy-signals.md) and [energy-finance/AI divide case study](../../Integrated-Research-Journey/2026-10-28-energy-finance-ai-divide-resilience.md). Author's analysis is independent of the Fed, IMF, World Bank and named faculty. Partial transcript is not a certified official transcript.

**Next acceptance criteria:** implement schema and validation tests; record at least one fully traceable, human-reviewed example per gate; compare AI nowcasts to vintage-correct baselines; perform independent audit before any production assurance claim.
