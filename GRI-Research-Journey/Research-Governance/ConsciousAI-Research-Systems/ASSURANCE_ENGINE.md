# GRI Institutional Intelligence and Assurance Engine — v1

**Status: executable research prototype, NOT a validated safety system, trained machine-learning model, continuous sensor network, security product, or certification service.**

## Purpose
A reproducible, evidence-first bridge between the GRI intelligence dashboard and an eventual institutional assurance platform. The central falsifiable hypothesis: systems can satisfy local objectives while generating globally unsafe, biased or institutionally illegitimate outcomes.

## Implemented
- `assurance_engine.py`: deterministic evidence gate; SHA-256 canonical record fingerprints; provenance and independent-publisher checks; fail-closed review of contradictions; no autonomous action.
- Classification performance: accuracy, precision, recall, false-positive and false-negative rates, group-level prediction rates.
- Probability evaluation: Brier score against externally labeled outcomes.
- Numeric distribution shift: exploratory standardized-mean drift heuristic.
- `test_assurance_engine.py`: synthetic regression tests.
- Dashboard and intelligence watchlist remain separate from this evaluation module until results are benchmarked and approved.

## Research-to-production roadmap
1. **TEVV:** versioned representative benchmark corpora, provenance and labeling protocols, baseline models, blind holdouts, uncertainty intervals, subgroup sizes, adversarial tests, reproducibility, red-team review.
2. **ML:** train a transparent classifier for evidence triage using independently reviewed historical cases. Compare to rules baseline; maintain separate train/validation/test splits and prevent temporal leakage. Never train on unverified dashboard entries as ground truth.
3. **OptiMirror-inspired independent evaluation:** compare claims, observed behavior and outcomes to independently sourced evidence; evaluate the evaluator for correlated error and disagreement. OptiMirror is a proposed GRI design concept here, not a claimed integrated external product.
4. **Monitoring:** source connectors, timestamps, deduplication, incident lifecycle, drift and bias monitoring, alert severity with false-alert tracking; publish freshness and coverage limitations.
5. **Controlled adaptation:** shadow deployment and human-reviewed updates; reinforcement learning only in bounded simulations with offline policy evaluation and rollback. Never optimize solely for alerts or engagement.
6. **Hardware/sensing:** opt-in, lawful and privacy-preserving sensor interfaces with independent validation; no unsupported claim that chips or phones can infer arbitrary wrongdoing.
7. **Governance:** Nelson Model (rules, actors, interests, power, legitimacy, options, adaptation), human approval, contestability, immutable audit records, security threat modeling and incident response.

## Evaluation principles
Do not confuse source count with independence, model agreement with truth, prediction disparity with proven discrimination, a drift heuristic with intrusion detection, or a passing test suite with deployed safety. Preserve direct links to primary evidence and separate hypotheses, allegations, verified events and attribution.

## Academic references
- NIST AI RMF: https://www.nist.gov/itl/ai-risk-management-framework
- NIST AI RMF Measure: https://airc.nist.gov/airmf-resources/airmf/5-sec-core/
- NIST AI 800-4 post-deployment monitoring: https://www.nist.gov/publications/challenges-monitoring-deployed-ai-systems-center-ai-standards-and-innovation
- NIST TEVV-Athlon: https://www.nist.gov/artificial-intelligence/ai-research/tevv-athlon-framework-evaluating-ai-systems

GRI interpretation of these sources does not imply endorsement by NIST, Thunderbird, ASU, or any named scholar.
