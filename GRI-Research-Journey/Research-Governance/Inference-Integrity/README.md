# Inference Integrity and Institutional Accountability

**GRI research prototype v0.2 | October 2026 | Synthetic data only**

This module extends the engineering question raised by Uber Engineering's *Taming the ML Firehose: Scaling Feature Consistency* into an independent GRI research question: can consistent inference evidence improve institutional accountability, and what governance gaps remain?

## Implemented
- Deterministically serialized SHA-256 chained inference records with chain verification and optional trusted tip comparison.
- Model score and synthetic policy decision recorded with model and policy versions.
- Candidate proxy flags explicitly classified as **unvalidated screening signals**, not findings of unlawful discrimination.
- Score replay status that does not claim complete model reproducibility.
- Fail-closed input validation and immutable result objects.

Run `python3 governance.py` and `python3 -m unittest discover -s tests`.

## Limitations and governance boundaries
- In-memory hashes are **not** tamper-proof storage. Trusted external anchoring, signatures, access control, privacy protection, durable persistence and independent audit remain future work.
- The DTI policy is a **synthetic credit risk rule**, not a disparate impact assessment or a legal credit decision rule.
- Feature attributions alone cannot establish protected-class proxies, discrimination, causal recourse or human oversight.
- No automated loan decisions, human appeals, legally actionable advice, or production deployment are authorized by this module.
- Score replay alone cannot validate the exact model artifact, preprocessing, stochastic state, environment or complete output.
- Never log sensitive production personal information without an approved minimization, retention and access-control design.

## Research bridge
Technical feature consistency and replay evidence connect ML infrastructure to institutional leadership questions: who sets objectives, who approves interventions, how affected individuals contest decisions, and how organizations remediate harm. These are GRI hypotheses requiring empirical validation, not findings attributed to Uber or Thunderbird School of Global Management at Arizona State University.

## References
Uber Engineering, Paarth Chothani, Chirag Agrawal, and Amrith M, *Taming the ML Firehose: Scaling Feature Consistency* (company-reported engineering case; source text provided for research).
NIST AI Risk Management Framework 1.0 (2023).
OECD AI Principles (2019; updated 2024).
