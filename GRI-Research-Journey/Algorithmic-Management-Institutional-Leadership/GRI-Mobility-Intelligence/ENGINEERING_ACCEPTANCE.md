# Mobility Intelligence | Consolidated engineering and assurance register

Grand Research Institute | 5 November 2026 | Existing research stream

## Institutional disposition

GRI leadership reports that the relevant confidential institutional assessments have already been conducted and has authorized consolidation of the public research record. This statement records leadership's disposition only; confidential reports, reviewer identities, methods and conclusions have not been inspected or independently reproduced through this repository. Do not publish or imply their contents.

The research and offline implementation remain in the existing GRI Mobility Intelligence directory. No new research program, production deployment, university endorsement, platform partnership or empirically demonstrated earnings improvement is claimed.

## Implemented public artifacts

* [Research specification](2026-10-23-research-proposal.md)
* [Offline scenario, economics and validation functions](mobility_core.py)
* [JSON command line interface](mobility_cli.py)
* [Trip event JSON Schema](trip_record.schema.json)
* [Synthetic unit tests](test_mobility_core.py)
* [Synthetic scenario](synthetic_scenario.json), [synthetic ledger](synthetic_ledger.json), and [synthetic forecast input](synthetic_forecast.json)
* [Data lifecycle and consent boundary](DATA_LIFECYCLE.md)
* [Mobility test workflow](../../../.github/workflows/mobility-intelligence-tests.yml)

## Acceptance status and outstanding gates

| Existing issue | Public implementation | Remaining verification |
| --- | --- | --- |
| [#11 M0–M1](https://github.com/BazeletDave/ConsciousAI/issues/11) | Accepted for offline research prototype: governance boundaries, scenario comparator, no drive, protected schedule, return deadline, sleep and duty constraints, uncertainty, JSON CLI and synthetic tests | Twelve representative M0/M1 checks executed successfully in isolated local verification on 5 November 2026 using reconstructed functions from reviewed repository source. This is not an execution of the repository CI workflow; CI remains unverified. CSV import/export belongs to issue #12 rather than the original #11 acceptance requirements. |
| [#12 M2](https://github.com/BazeletDave/ConsciousAI/issues/12) | Record validation, versioned schema, event distinctions, synthetic fixtures and lifecycle policy committed | Private operational consent registry, withdrawal, deletion/export, retention and security controls before real data collection |
| [#13 M3–M5](https://github.com/BazeletDave/ConsciousAI/issues/13) | Uncalibrated historical mean baseline and synthetic forecast CLI committed | Temporal backtesting, uncertainty calibration, out of distribution assessment, optimizer comparison, preregistered evaluation and prospective evidence |

**CI status:** The workflow is committed, but a passing GitHub Actions run has not been verified in this record. Unit test definitions and synthetic fixtures do not establish an independently reproduced result.

**Independent review:** Do not equate confidential GRI review with external independent reproduction or with an engineering acceptance check. Any separately frozen assurance work remains under its existing controls. Do not reopen it or imply a reviewer decision.

## Execution and governance

From this directory: `python -m unittest discover -p 'test_mobility_core.py' -v`. To exercise the offline interface: `python mobility_cli.py scenario synthetic_scenario.json`, `python mobility_cli.py ledger synthetic_ledger.json`, and `python mobility_cli.py forecast synthetic_forecast.json`.

All public example data are synthetic. No live ingestion, production credentials, platform automation or passenger identifying data are authorized. Keep #12 and #13 open until their distinct acceptance evidence is available. Issue #11 is accepted for its bounded M0/M1 offline prototype scope; no production or prospective performance assertion. Consolidation is a documentation and status reconciliation, not certification.
