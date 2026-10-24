# GRI v1.2: reproducible ML evaluation foundation

This release implements deterministic, offline numeric prediction evaluation and a read-only capability endpoint. **No trained model, consented dataset, deployed inference service, validated accuracy, or independent certification is claimed.**

## Evidence path
1. Obtain separately consented, licensed, purpose-limited observations and document provenance.
2. Validate schema, duplicates, temporal ordering, leakage, retention, and privacy controls.
3. Define a baseline and temporal holdout before training; use adequate sample sizes for the use case.
4. Train and evaluate in an isolated environment with reproducible environment/seed/artifact digests.
5. Evaluate accuracy, calibration, subgroup fairness, drift, security, and operational utility; record failures.
6. Obtain independent review and explicit human release approval before any model promotion.

## Supported now
- `evaluate_numeric_predictions(rows)`: finite-value checks, minimum sample gate, MAE/RMSE, deterministic evaluation digest; never returns raw observations.
- `/platform/evaluation`: static public metadata, **not a data ingestion endpoint**.
- Unit tests with synthetic inputs; tests must be executed in CI before a release is certified.

## Next release requirements
- Versioned consented dataset registry and access controls
- Automated CI test execution and signed evaluation artifacts
- Real data quality checks and independent holdout assessment
- Dashboard visualization of *verified* metrics with sample sizes and limitations

No private mobility telemetry, interview participant data, or credential is to be committed to GitHub.
