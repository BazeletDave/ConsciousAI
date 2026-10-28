# Institutional decision episode measurement

David A. Grand | Grand Research Institute | 28 October 2026

This offline research instrument operationalizes selected measures proposed on pages 17 to 19 of [The AI Governance Paradox](../README.md). It extends the existing [claim lineage and assurance implementation](../../../Algorithmic-Management/Training-a-Tiger-AI-Paradox/Implementation/README.md): that package evaluates evidence records; this instrument measures recorded institutional decision episodes.

## Reproduce

Python 3.10 or newer. Standard library only. From this directory:

```bash
python -m unittest discover -v
python measurement.py synthetic_episodes.json --output synthetic_results.json
```

Eight test methods passed on 28 October 2026, including nine invalid record subcases. The delivered three episode fixture is entirely synthetic. Its calculated trace completeness is 2/3, false approvals among reviewed approvals 1/2, intervention completion 1/2, and median completed intervention latency 10 seconds. These deliberately imperfect results demonstrate measurement behavior, not GRI institutional performance.

## Measurement definitions

| Measure | Numerator | Denominator or observation rule |
| --- | --- | --- |
| Trace completeness | Episodes containing actor, accountable owner, policy version, system version and evidence references | All submitted episodes |
| Approval without recorded authority | Approved episodes marked authority invalid | All approved episodes |
| Adjudicated decision accuracy | Decisions agreeing with supplied authorization adjudication | Episodes with adjudication and reviewer identity |
| False approvals among reviewed approvals | Approved episodes adjudicated unauthorized | Approved episodes with adjudication |
| Intervention completion | Required interventions with recorded completion | All required interventions, including missing completions |
| Intervention latency | Time from trigger to intervention | Completed required interventions only; median, maximum and count reported |
| Verified remediation | Remediation marked verified with review and evidence references | Episodes explicitly evaluated for remediation |

Every proportion includes numerator and denominator. Empty denominators return null. Unknown adjudications are not correct decisions. Negative latency, naive timestamps, duplicate episode identifiers, ambiguous boolean values, and unsupported verified remediation are rejected. Synthetic and observational episodes cannot be pooled in one run. The input fingerprint detects content changes; it is not a digital signature or proof that the evidence is true.

## Record and review protocol

The fixture supplies the record structure. Each episode needs an id, evidence_status, decided_at, three explicit booleans (approved, authority_valid, intervention_required), and the available provenance fields. Optional adjudicated_authorized and remediation_verified accept true, false, or null. Nonnull adjudication requires adjudicator_id. Required interventions need triggered_at; a completion needs intervened_at. Verified remediation needs remediation_review_id and remediation_evidence_ref.

Before observational use, define the sampling frame, decision unit, observation window, permitted authority, exclusions and reviewer protocol. Retain incomplete episodes. Collect records only within the approved research scope and remove identifying participant information before publication. Reviewer identities may use stable confidential codes backed by a controlled registry. The instrument checks presence and consistency, not reviewer independence, policy validity, source authenticity, harm severity or completeness of the sampling frame.

## Testing the AI Learning Paradox

The engineering next step is a repeated decision exercise for executive education. Use comparable scenarios before and after instruction, retain policy and system versions, and have reviewers assess decisions independently of training assignment. Compare intervention completion, authorization errors and verified remediation alongside task quality and time cost. Randomize the order or assignment where feasible; document prior experience, task difficulty, attrition and organizational context. Prespecify outcomes and uncertainty analysis before examining results.

This module measures episodes. It does not estimate a learning effect. A separate study design and appropriate statistical analysis are required to test whether continued leadership learning improves governance. Increased intervention can reflect better detection or worse underlying systems; latency alone cannot resolve that distinction. This is the research connection to GRI's paradox: task optimization must be evaluated alongside authority, correction and institutional capacity.

## Integration boundary

The JSON output can serve as a candidate dashboard review artifact after schema review. No endpoint, production dashboard or autonomous controller is changed. External records should be supplied through a separately authorized adapter with observation windows and access controls. Do not use these metrics as a composite certification score or legal compliance decision.

The methodological basis is the report and existing GRI implementation linked above. No new external empirical finding is asserted in this engineering extension.
