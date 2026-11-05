# Mobility Intelligence engineering acceptance register

Grand Research Institute | 5 November 2026 | Offline research implementation

## Scope and evidence maturity

This is a bounded implementation inside the existing GRI Mobility Intelligence research stream. The module `mobility_core.py` has no network, platform API, credentials, driver account access, or automated offer acceptance. It provides manual hypothetical scenario comparison, a consent gated nonidentifying research record validator, realized net contribution calculations, and a simple historical mean forecasting baseline. All supplied test records are synthetic.

## Milestone mapping

| Issue | Implemented now | Still required before closure |
| --- | --- | --- |
| #11 M0–M1 | Offline rules comparison, no drive option, hard return, sleep, schedule and duty constraints, uncertainty disclosure, net economics, unit tests | Full CLI or dashboard, CSV import/export, governance review and verified test run |
| #12 M2 | Consent flag, explicit event states, source field, prohibited extra fields, timezone and finite numeric checks, synthetic fixture | Versioned JSON Schema, actual consent registry, withdrawal, deletion/export, retention and security controls |
| #13 M3–M5 | Simple pre-horizon mean baseline with explicitly uncalibrated uncertainty proxy | Temporal backtesting, calibration, OOD, optimizer comparison, preregistered outcomes, prospective evaluation and independent reproduction |

## Local execution

From this directory run `python -m unittest discover -p 'test_mobility_core.py' -v`. No external dependencies. A passing test suite is evidence of the specified synthetic unit behavior only, not empirical effectiveness or independent assurance.

## Research governance

No personal, passenger or location telemetry is required or included. No actual consented trip ingestion is authorized. Do not promote this prototype to production, close milestone issues, or claim forecast performance until the outstanding gates are demonstrated and reviewed.
