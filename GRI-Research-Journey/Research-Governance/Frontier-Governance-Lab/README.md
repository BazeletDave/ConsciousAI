# GRI Frontier Governance Lab | Research Prototype v0.1

This independent Grand Research Institute module explores how institutional policies can be translated into inspectable, deterministic AI decision rules. It is **not** an EU regulatory sandbox, a certified compliance system, a production guardrail, or authorization to operate autonomous agents.

## Run

From this directory, using Python 3.10 or newer:

```bash
python -m unittest discover -p 'test_*.py' -v
```

No third party dependencies or network access are required.

## Research design

Inputs are synthetic bias, hallucination, unauthorized escalation risk, and autonomy measurements. The policy engine first rejects hard threshold violations, then routes high autonomy borderline cases for review. Missing authorization denies regardless of human approval. A review can only be approved when all hard thresholds pass. The assessment function returns a deterministic SHA256 digest of a canonical record, but **a digest is not an immutable, independently anchored audit log**.

## Evidence and validation limitations

Thresholds are illustrative, not empirically calibrated. The module does not measure real model behavior, intercept real tool calls, implement isolation, verify human identity, persist tamper resistant logs, or establish legal compliance. Real deployment requires identity and permission verification, fail closed enforcement, external audit storage, attack simulations, calibrated datasets, and independent security review.

## Research questions

1. How does policy evaluation latency compare with agent decision latency?
2. What is the false approval rate under adversarial and distribution shifted inputs?
3. How does human review affect governance outcomes and throughput?
4. Can institutions reconstruct, contest, and correct decisions using independently verified evidence?

## Academic integrity and source governance

Maintain separation between public institutional sources, original GRI hypotheses, copyrighted teaching materials, and independently collected empirical observations. Do not claim endorsement by Thunderbird, Arizona State University, regulators, or research participants.

## Deployment boundary

This branch adds offline research code only. No changes to the existing Render dashboard, scheduled ingestion, production policy, or external services are included.
