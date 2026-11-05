# Mobility Intelligence engineering acceptance register

Grand Research Institute | 5 November 2026 | Offline research implementation

## Scope and evidence maturity

This is a bounded implementation inside the existing GRI Mobility Intelligence research stream. The module `mobility_core.py` has no network, platform API, credentials, driver account access, or automated offer acceptance. It provides manual hypothetical scenario comparison, a consent gated nonidentifying research record validator, realized net contribution calculations, and a simple historical mean forecasting baseline. All supplied test records are synthetic.

## Milestone mapping

| Issue | Implemented now | Still required before closure |
| --- | --- | --- |
| #11 M0–M1 | Offline rules comparison, no drive option, hard return, sleep, schedule and duty constraints, uncertainty disclosure, net economics, unit tests | CSV import/export, governance review and verified test run (offline JSON CLI now committed) |
| #12 M2 | Consent flag, explicit event states, source field, prohibited extra fields, timezone and finite numeric checks, synthetic fixture | Actual private consent registry, operational withdrawal and deletion/export controls, retention and security controls (JSON Schema and policy document now committed) |
| #13 M3–M5 | Simple pre-horizon mean baseline with explicitly uncalibrated uncertainty proxy | Temporal backtesting, calibration, OOD, optimizer comparison, preregistered outcomes, prospective evaluation and independent reproduction (synthetic forecast CLI now committed) |

## Local execution

From this directory run `python -m unittest discover -p 'test_mobility_core.py' -v`. No external dependencies. A passing test suite is evidence of the specified synthetic unit behavior only, not empirical effectiveness or independent assurance.

## Research governance

No personal, passenger or location telemetry is required or included. No actual consented trip ingestion is authorized. Do not promote this prototype to production, close milestone issues, or claim forecast performance until the outstanding gates are demonstrated and reviewed.


## November 5 continuation

The repository now includes an offline JSON CLI, versioned JSON Schema, synthetic scenario, ledger and forecasting fixtures, a data lifecycle policy, and a GitHub Actions workflow for synthetic tests. These additions are implementation evidence, **not proof that CI passed**. GitHub's combined commit status returned no reported statuses at the time of review. The three issues remain open because operational consent controls, complete evaluation, and independent verification have not been demonstrated.
