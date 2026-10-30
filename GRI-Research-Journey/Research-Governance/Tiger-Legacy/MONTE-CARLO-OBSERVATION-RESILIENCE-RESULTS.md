# GRI AI Paradox | Seeded Observation Resilience Simulation Results

**Classification:** Synthetic computational experiment; GRI authored, not independent verification or production assurance.  
**Execution date:** 30 October 2026.  
**Code:** [observation_resilience_monte_carlo.py](version_one/observation_resilience_monte_carlo.py) and [regression tests](version_one/test_observation_resilience_monte_carlo.py).  
**Source code SHA256 of locally executed copy:** `6bfda367966d3fbd1367547d9efebf965db86a7515e707f1981ce5564bf822c1`.  
**Test SHA256 of locally executed copy:** `f42e323bcf4181ace71b55d35c28398c40a3265193a8cfca3e56946b318f6cb1`.  
**Verification:** Five local unittest checks passed. GitHub CI and independently executed repository checkout have not been verified.

## Research design

Twenty deterministic seeds, integers 20261030 through 20261049, were run at each of five shared error mixture values (0, 0.25, 0.50, 0.75, 1). Each seed and setting generated 10,000 paired synthetic cases. This is 100 simulation runs and 1,000,000 **case assignments**, not a million independent empirical observations. Hazard prevalence was 0.20, unauthorized probability 0.15, hazard miss probability 0.20 and false alarm probability 0.05. The shared error mixture selects whether the second observation copies the first observation's error; it is not an empirically estimated sensor correlation coefficient. Gate definitions: single allows only if authorized and primary alarm is false; dual allows only if authorized and both alarms are false. No reviewer actions or physical latencies were simulated.

## Aggregated outcomes

The following rates use *authorized hazard* or *authorized nonhazard legitimate* cases as denominators. Values pool the 20 seeds within each error condition.

| Shared error mixture | Single hazard allowed | Dual hazard allowed | Single legitimate allowed | Dual legitimate allowed | Additional holds (per 200,000 cases) |
| --- | ---: | ---: | ---: | ---: | ---: |
| 0% | 19.84% | 4.16% | 94.92% | 90.12% | 11,893 |
| 25% | 19.74% | 7.87% | 95.02% | 91.50% | 8,811 |
| 50% | 19.93% | 12.00% | 95.03% | 92.70% | 5,862 |
| 75% | 20.06% | 15.96% | 94.96% | 93.83% | 2,920 |
| 100% | 20.09% | 20.09% | 95.03% | 95.03% | 0 |

Unauthorized action allowances were zero under both policies by construction of the authorization gate. This does **not** test authentication compromise, policy specification failure or identity forgery. The 100% shared error case gives identical decisions, a negative control. At zero shared error the dual policy reduces permitted synthetic hazards but increases legitimate holds.

## Interpretation

The synthetic model exhibits a safety versus availability tradeoff. Additional observation is useful when errors are not shared, but its incremental benefit collapses as failures become common. The model is intentionally simple: observation errors are random under stipulated distributions, the second gate adds information and work, the authorized decision is given as ground truth, and no end to end task completion or reviewer effectiveness is measured. The rates cannot be generalized to actual AI systems or institutional settings. The deterministic gate architecture itself mathematically guarantees that dual allowed cases are a subset of single allowed cases; the simulation tests magnitude under assumed errors, not whether the subset relation is surprising.

## Reproduction

From `version_one` run `python -m unittest -v test_observation_resilience_monte_carlo`. Run the CLI with `python observation_resilience_monte_carlo.py --seed 20261030 --n 10000 --shared-error 0.5`. To reproduce the reported sweep, loop seeds 20261030 through 20261049 and shared error values 0, 0.25, 0.5, 0.75, 1; aggregate each policy's `hazards_allowed` over `hazard_authorized` and `legitimate_allowed` over `legitimate_authorized`. Counts are in `counts`, denominators in `denominators`. All cases use the same seeded random stream within each run and are paired across policies. Python standard library only.

## Next research gates

1. Exact committed checkout and CI verification, with run identifiers and retained machine readable outputs.
2. Sensitivity analysis over hazard prevalence, miss and false alarm rates, and explicit cost functions for false holds, hidden hazards and reviewer load.
3. Adversarial and time dependent failure models rather than solely a copied error mixture.
4. Independent replication and methodological review before any external claims of validated assurance.

**Preservation:** No production integration, confidential research disclosure, client data, autonomous operational control, or modification of frozen Training a Tiger evidence.
