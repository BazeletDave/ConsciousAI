# GRI AI Paradox | Computational Reproduction and Institutional Cost Analysis

**Status:** Author directed computational reproduction, not independent external validation or observation of actual human review. 30 October 2026.

## Reproduction evidence

The exact text of the GitHub source and test modules was fetched, saved locally and SHA256 checked. Source hash `6bfda367966d3fbd1367547d9efebf965db86a7515e707f1981ce5564bf822c1`; test hash `f42e323bcf4181ace71b55d35c28398c40a3265193a8cfca3e56946b318f6cb1`. Five tests passed. Twenty seeds (20261030–20261049) at each of five shared error settings, 10,000 cases per seed, reproduced 1,000,000 synthetic assignments. This is not a separate researcher's independent reproduction, a signed GitHub CI attestation or a production test.

## Explicit illustrative cost model

For each shared error setting, calculate the **incremental value of dual observation versus single observation**:

`net benefit = (additional authorized hazards blocked × cost per missed hazard) − (additional legitimate actions blocked × cost per unnecessary intervention) − (number of additional observations × cost per observation)`.

These illustrative shadow prices are **assumptions**, not measured dollars: missed hazard consequence $1,000, unnecessary legitimate hold $20, extra observation $0.10 per simulated case. There are 200,000 additional observation attempts per setting. No reviewer decisions are simulated; human review effectiveness, reviewer wages, escalation time, delayed decisions, remediation success and distributional harms are unmeasured. This is a decision analysis, not an operational cost accounting model.

| Shared error mixture | Additional hazards blocked | Additional legitimate holds | Net illustrative benefit (USD) | Hazard cost break even (USD) |
| --- | ---: | ---: | ---: | ---: |
| 0% | 5,360 | 6,533 | $5,209,340 | $28.11 |
| 25% | 4,026 | 4,785 | $3,910,300 | $28.74 |
| 50% | 2,689 | 3,173 | $2,605,540 | $31.04 |
| 75% | 1,394 | 1,526 | $1,343,480 | $36.24 |
| 100% | 0 | 0 | −$20,000 | Not attainable with positive sensor cost |

Break even assumes $20 per extra legitimate hold and $0.10 per additional observation; it solves for the missed hazard consequence at which the incremental net benefit is zero. These outputs are not estimates of GRI savings, losses or client impact.

## Actual review procedure evaluation: not yet possible

The current model contains **no actual reviewers or recorded review decisions**. An effectiveness claim requires a separately authorized study with a predeclared reviewer protocol, independently adjudicated synthetic ground truth, blinded assignment, reviewer accuracy and disagreement, time to disposition, reversals, escalation rate, documented authority, and interrater agreement. Reviewers must be real consenting participants under appropriate ethics and privacy safeguards; a scripted oracle must never be described as a human reviewer. No such evaluation was executed in this phase.

## Methodological constraints and next gates

The simulated authorization truth is stipulated and perfect. The dual gate is designed to be a subset of the single gate; differences are model consequences rather than discovery of general institutional causality. Hazard prevalence and observation errors are chosen rather than estimated. Correlated errors are modeled as a mixture of copied errors, not real sensor covariance. Real impacts may be nonlinear, fat tailed, delayed or borne by different stakeholders. Costs should therefore be elicited and bounded through documented expert judgments and sensitivity ranges before any policy recommendation.

Next: independent external execution of the exact revision; predeclared cost ranges and sensitivity thresholds; prospective human review protocol subject to ethics and authorization; adversarial common cause and time dependent failure models. No production systems, confidential evidence or historical experiments were modified.
