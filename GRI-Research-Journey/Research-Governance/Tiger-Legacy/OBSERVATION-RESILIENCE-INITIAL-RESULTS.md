# GRI AI Paradox | Observation Resilience Initial Results

**Classification:** GRI authored synthetic fixture experiment; not independent validation, deployed governance, or real sensor performance.  
**Execution:** Locally executed 30 October 2026 using Python standard library. Four regression tests passed. The source and tests were subsequently committed to GitHub. GitHub CI and exact checked-out commit reproduction have not yet been verified.

## Protocol relationship

Extends [the approved prospective observation resilience protocol](AI-PARADOX-OBSERVATION-RESILIENCE-NEXT-STAGE.md) without modifying the initial nine-case comparison, Training a Tiger's frozen research, or the live dashboard.

## Paired fixture results

| Outcome | Denominator | Single observation allows | Dual observation allows |
| --- | ---: | ---: | ---: |
| Unauthorized action | 4 | 0 | 0 |
| Legitimate action | 3 | 3 | 1 |
| Hidden hazard | 5 | 2 | 1 |

Five of twelve synthetic cases trigger simulated review referral. These referrals are *not* decisions made by a human reviewer. The dual gate holds two legitimate actions with contradictory or missing observations. The second observation detects the deliberately authored primary biased case, but **both observations conceal the correlated failure case and it remains allowed**. This is a negative finding retained explicitly.

## Method and reproducibility

Source: [observation_resilience.py](version_one/observation_resilience.py)  
Tests: [test_observation_resilience.py](version_one/test_observation_resilience.py)

From `version_one`, execute `python -m unittest test_observation_resilience -v` and `python observation_resilience.py`. The local run returned four passing tests and the counts above. Source SHA256 for local script: `f4baf49e6d75eb463eb1df9032645aae4d3cc8991b0d99a91a4891814e9c6209`. Test SHA256: `f58e3d9059271f7b68e16e55c76fab10839c6dd7ebf668e321e6da3391c0633a`. The output was also generated as JSON locally.

## Interpretation and constraints

This is a demonstration of deterministic gate logic using twelve authored fixtures. It is **not** a direct integration of the Tiger Legacy grant engine or original Training a Tiger physical simulator; the authorization truth labels are explicitly stipulated. The two readings are separately provided values but are not empirically independent sensors. There is no statistical sampling, no confidence interval, no inference about real-world rates, no measured latency or review costs, and no operational human intervention. The dual gate's additional observation constitutes an unequal information budget. The selected case composition affects the displayed ratios.

The central observation is conditional: more checks can reduce selected concealed hazards, while false holds increase and correlated failure remains. Further work should test independent fixture generation, realistic correlated sensor error models, false-positive cost and actual end-to-end task outcomes before any generalized claim.

**Preservation:** No client data, confidential IP, operational endpoints, historical evidence or production system modifications.
