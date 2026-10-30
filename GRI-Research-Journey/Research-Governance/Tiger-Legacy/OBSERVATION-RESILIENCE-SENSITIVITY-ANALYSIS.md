# GRI AI Paradox | Observation Resilience Sensitivity Analysis

**Status:** Local author executed synthetic sensitivity analysis, 30 October 2026. Not independently replicated. No production validation.

## Method

Reproduced the existing [seeded Monte Carlo model](version_one/observation_resilience_monte_carlo.py) in an isolated Python standard library script, varying one parameter at a time. Ten seeds (20261030 through 20261039), 5,000 cases per seed and ten scenarios produced 500,000 synthetic case assignments. The default scenario uses hazard prevalence 0.20, unauthorized probability 0.15, hazard miss probability 0.20, false alarm probability 0.05 and shared error mixture 0.25. The second observation copies the first error with probability equal to the mixture parameter; this is not an observed correlation coefficient.

The original committed Monte Carlo source was not modified. This analysis uses a locally reconstructed model; exact committed checkout execution and independent replication remain open verification gates.

## Results

Rates are conditional on authorized hazard cases or authorized nonhazard cases, respectively.

| Scenario | Single hazard allowed | Dual hazard allowed | Single legitimate allowed | Dual legitimate allowed |
| --- | ---: | ---: | ---: | ---: |
| Baseline | 19.74% | 8.24% | 95.03% | 91.56% |
| Hazard prevalence 5% | 19.02% | 7.92% | 94.94% | 91.43% |
| Hazard prevalence 40% | 19.62% | 7.88% | 94.99% | 91.52% |
| Hazard miss 5% | 5.28% | 1.54% | 95.03% | 91.56% |
| Hazard miss 40% | 39.41% | 22.19% | 95.03% | 91.56% |
| False alarm 1% | 19.74% | 8.24% | 98.93% | 98.19% |
| False alarm 15% | 19.74% | 8.24% | 84.88% | 75.24% |
| Shared error 0% | 19.73% | 4.24% | 94.67% | 89.90% |
| Shared error 50% | 20.50% | 12.54% | 94.94% | 92.61% |
| Shared error 100% | 20.39% | 20.39% | 95.04% | 95.04% |

At baseline, 2,159 additional holds occurred across 50,000 synthetic assignments. Under 15% false alarm, additional holds rose to 4,256. With fully shared observation errors, dual and single policies made identical decisions. Unauthorized allowance is zero by construction of the stipulated authorization truth and therefore cannot establish protection against compromised identity or incorrectly specified authorization rules.

## Interpretation

The results are consistent with a tradeoff between hazard detection and legitimate task availability. Observation diversity helps only insofar as failures are not shared. Increasing false alarms makes an always-hold-on-disagreement rule potentially costly. Prevalence changes total counts but has limited influence on conditional rates under the current independent random assumptions.

The gate construction guarantees dual allowances are a subset of single allowances. Thus the direction of the tradeoff is a property of the specified policy, not a surprising empirical discovery. The simulation does not model actual reviewer decisions, adversarial adaptation, time delays, real sensor independence, end to end task completion, or monetary costs.

## Reproduction

Use the source implementation's `simulate` function with ten seeds 20261030 to 20261039, 5,000 cases each. Pool counts for `hazards_allowed` over `hazard_authorized` and `legitimate_allowed` over `legitimate_authorized`. Change one parameter at a time from the default setting above. The scenario values are: hazard prevalence 0.05 and 0.40; miss rate 0.05 and 0.40; false alarm rate 0.01 and 0.15; shared error mixture 0, 0.5 and 1. The baseline shared error mixture is 0.25. An exact committed checkout rerun, retained machine readable evidence, independent verification and CI evidence should be completed before any external assurance claim.

**Preservation:** This analysis does not modify frozen historical research, operational services, client systems or confidential GRI records.
