# CISA 2030 | GRI Empirical Evidence Protocol v0.1

This is an **offline research prototype**, not CISA certification, a live data collector, or a publication authority. Six GRI research domains: defend (detection), harden (patch verification), prevail (recovery), human authority (override), evidence integrity (provenance), institutional legitimacy (remediation).

## Research workflow

1. Preregister the hypothesis, system boundary, success/failure criterion, sampling frame, consent and authorization, and experimental operator.
2. Capture an original primary artifact, timestamp, HTTPS source URL, and SHA256 hash of its **actual bytes**. Do not upload secrets, personal data, raw participant interviews, or sensitive logs to this public repository.
3. Require an independent reviewer and a separate source-hash verification. This version only validates **declarations** of these checks, not reviewer identity or actual artifact bytes. Preserve external audit documentation.
4. Label real controlled experiments and documented observations separately from simulations. Synthetic data must never be promoted to empirical results.
5. Validate with `validate(record)`; aggregate with `summarize(records)`. Rejected records are counted. Domains with no accepted records remain `unmeasured`.
6. Preserve append-only corrections and the full denominator and failed collection attempts in the future authenticated evidence ledger.

## Required evidence record

`record_id`, `case_id`, `domain`, `observation_type`, `observed_at`, `source_url`, `source_sha256`, `outcome`, `reviewer_id`, `reviewed_at`, `independent_review`, `consent_or_authority`, `source_verified`; mark `scenario_type` explicitly.

A boolean outcome means only that the **predefined test criterion** passed or failed. It does not demonstrate general effectiveness. Observed fractions are descriptive, not representative population estimates. No cross-domain score, causal claim, or institutional compliance determination is supported.

## Production boundary

Do not change dashboard metrics from `unmeasured` until the system has authenticated reviewers, verified artifact bytes, durable append-only storage, consent/privacy controls, source retention, and audited approval. This module performs no external collection, no writes, and no live system tests.

Run `python -m unittest -v test_evidence_validation.py` from this directory.
