# GRI AI Paradox | Computational Reproduction and Institutional Cost Scenarios

**Status:** Exact-source-hash local computational reproduction completed; externally independent replication outstanding. Costs are assumed research units, not observed prices or monetary valuations. No real reviewer performance data were collected.

## Source provenance and reproducibility

Retrieved the committed `version_one/observation_resilience_monte_carlo.py` and `test_observation_resilience_monte_carlo.py` through the connected GitHub repository, recreated their UTF-8 contents locally, and verified SHA256 hashes match the previously recorded executed sources:

* Runner: `6bfda367966d3fbd1367547d9efebf965db86a7515e707f1981ce5564bf822c1`
* Tests: `f42e323bcf4181ace71b55d35c28398c40a3265193a8cfca3e56946b318f6cb1`

Executed `python -m unittest -v test_observation_resilience_monte_carlo`: **5 tests passed**. Executed the 20 seed by 5 setting sweep: 100 runs of 10,000 synthetic assignments each. The reproduced counts agree with the earlier Monte Carlo report. This is an internal reproduction by the same research assistance process, **not** independent academic or third party verification.

## Reproduced paired results

| Shared error mixture | Single hazard allowance | Dual hazard allowance | Single legitimate allowance | Dual legitimate allowance | Extra holds across 200,000 assignments |
| --- | ---: | ---: | ---: | ---: | ---: |
| 0 | 19.84% | 4.16% | 94.92% | 90.12% | 11,893 |
| 0.25 | 19.74% | 7.87% | 95.02% | 91.50% | 8,811 |
| 0.50 | 19.93% | 12.00% | 95.03% | 92.70% | 5,862 |
| 0.75 | 20.06% | 15.96% | 94.96% | 93.83% | 2,920 |
| 1.00 | 20.09% | 20.09% | 95.03% | 95.03% | 0 |

At shared error mixture 0.25, the dual policy prevented 4,026 synthetic hazard allowances but denied 4,785 additional legitimate actions relative to the single policy. The remaining extra holds include both categories; they are not all false holds.

## Incremental institutional cost model

For each policy comparison define:

`Net benefit = (additional hazard allowances prevented × loss per missed hazard) − (additional legitimate actions blocked × intervention cost) − (all attempted cases × additional observation cost)`.

The loss per missed hazard must be assessed with scenario dependent severity, likelihood of actual harm conditional on an allowed hazard, exposure, recovery cost, downstream harms, and uncertainty. The false hold cost may include delay, lost access, service interruption, dispute handling and institutional trust. Observation cost may include compute, staffing, latency and assurance maintenance. These costs are *not* empirically calibrated in this model.

An illustrative, explicitly hypothetical parameter set assigns 1,000 cost units per allowed hazard, 10 units per additional blocked legitimate action, and 0.1 units per additional observation. At shared error 0.25 and 200,000 assignments, incremental net benefit = 4,026,000 − 47,850 − 20,000 = **3,958,150 assumed units**. Under fully shared error, no hazards are prevented and net benefit is **negative 20,000 units** from extra observations alone. These are scenario calculations, not savings forecasts, valuations, or verified risk reductions.

The sweep spans hazard losses 100, 1,000, 10,000 units; false hold costs 1, 10, 100 units; and observation costs 0.01, 0.1, 1 unit, at five shared error settings: 135 parameter scenarios. A single net benefit value must never be presented without its assumptions and sensitivity range.

## Actual human review: evidence still required

No human review procedure was actually tested. Therefore effectiveness, interrater agreement, reviewer independence, turnaround time, escalation accuracy and cost remain **unmeasured**. A synthetic review oracle is not a substitute.

A prospective institutional review study should define: eligibility and referral criteria; separation of reviewer from model developer; access to case evidence and provenance; blinded ground truth; conflict of interest rules; escalation and appeal; revocation and remediation authority; audit trail; time to decision; and outcome adjudication. Recruit authorized reviewers and obtain necessary ethical, privacy and organizational approvals before any human participant study. For synthetic vignettes, record sensitivity, specificity, reversal accuracy, interrater reliability, review time, appeal rate, unresolved cases and reviewer cost. Compare assisted and unassisted review with randomized case assignment and preregistered stopping rules. Do not infer real reviewer effectiveness from software fixtures.

## Limitations and research integrity

The authorization truth is stipulated; observation errors follow a simplified mixture model, not measured real sensors. Dual decisions are mathematically a subset of single decisions. No malicious adaptation, human reviewer, end to end task outcome or production deployment was tested. Reproducing exact source hashes establishes code consistency but does not independently validate model assumptions. An external replication package should include source revision, SHA256, command lines, exact parameter grid, machine readable outputs and independently signed reviewer conclusions.

**Governance:** Preserve historical Training a Tiger research, confidential IP, dashboard operations and the existing verification access policy. No production or client integration is authorized.
