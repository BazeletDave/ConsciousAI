# Executable Governance | Working Research Implementation

**Status: implemented offline reference code, synthetic experiments and automated unit tests.** No production safety system, real-world validation, Apple/Uber integration or fleet deployment is claimed.

This package implements the bounded engineering milestones described in the [October 21 research synthesis](../../Integrated-Research-Journey/2026-10-21-algorithmic-governance-living-research.md).

## Run

Requires Python 3.9+ and standard library only.

```bash
cd GRI-Research-Journey/Research-Governance/Executable-Governance
python -m unittest discover -p 'test_*.py' -v
python experiment.py
```

The experiment writes `results/synthetic_events.csv`, `results/synthetic_metrics.json`, and `results/synthetic_confusion_matrix.svg`. It uses a fixed random seed for reproducibility. Outputs are **synthetic demonstration results**, not estimates of real-world driver safety or model accuracy.

## Implemented

- Versioned deterministic governance policy; separates classification inputs from authorized action.
- JSON event schema and input validation; synthetic-only gate.
- SHA-256 audit record digest (integrity fingerprint, **not** an authenticated tamper-proof log).
- Unit tests for intervention boundaries, confidence, attribution, invalid inputs and repeatability.
- Synthetic dataset, confusion matrix counts, precision, recall, false-positive rate and SVG chart generation.
- Governance decision outcomes limited to no action, review evidence, and nonpunitive warning permitted.

## Research integrity

The synthetic reference label is artificially generated and is **not** ground truth. Precision and recall here test internal behavior of an illustrative model under artificial assumptions. A confidence threshold of 0.90 is unvalidated. No personal data, phone message content, vehicle actuation, enforcement or automatic adverse employment action is involved.

## Institutional crosswalk

NIST AI RMF functions: **Govern** (policy version, authorization), **Map** (driving context and potential harms), **Measure** (simulation metrics and tests), **Manage** (review, permitted warning, versioned changes). The RMF is voluntary guidance, not a certification.

## Evidence and NSA advisory

See [source and evidence register](EVIDENCE_REGISTER.md). The earlier NSA/PHP advisory discussion is treated as an **unverified advisory reference** pending original source identifiers. No service has been declared secure based on this package.

## Published governance decision contract | 31 October 2026

The existing [synthetic event schema](event.schema.json) is complemented by the [versioned governance decision JSON Schema](governance-decision.schema.json) and [provenance and decision record specification](GOVERNANCE-DECISION-CONTRACT.md). These are published interface contracts only; executable validation, authenticated signatures, immutable storage and independent replay remain separate engineering and verification milestones.
