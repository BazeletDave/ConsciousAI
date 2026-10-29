# GRI Tiger Legacy | Engineering and Research Quality Standard

**Research lead:** David A. Grand | Grand Research Institute  
**Academic context:** Thunderbird School of Global Management, Arizona State University. This is independent GRI work; no Thunderbird or ASU sponsorship, endorsement, institutional review, or validation is implied.

## Governing principle

Claims follow evidence. A local component pass, a high model score, or a successful simulation does not establish system-level security, real-world generalization, or institutional legitimacy. Preserve negative results and limits.

## Software quality gates

- Explicit architecture and trust boundaries, typed public interfaces, minimal dependencies, documented assumptions and failure behavior.
- Deterministic unit tests, integration tests, negative/adversarial tests, linting, formatting, static analysis, dependency and secret scans, reproducible CI artifacts.
- Versioned changes, reviewable diffs, immutable reference experiment inputs and results, no fabricated pass counts or deployment claims.
- No production release without security review, reliable rollback, monitoring, and independently verified acceptance evidence.

## Security and assurance gates

- Default-deny, least privilege, independently authenticated identities and human approvals; never trust caller-supplied identifiers or approval flags as credentials.
- Tenant-isolation tests at every boundary; consent scope, purpose, expiry, revocation and auditable access decisions.
- Threat model, secrets management, cryptographic key lifecycle, trusted verification anchors, replay and tamper detection, transactional durability, recovery testing.
- Synthetic-only research fixtures. No client data, live scans, client integrations, operational remediation, or public disclosure of confidential findings without authorization.
- Report unmeasured controls as unmeasured. Cryptographic hashes and HMACs do not by themselves prove independent attestation.

## Machine learning and reinforcement learning gates

- Every ML experiment must document task definition, dataset provenance and rights, data splits, leakage checks, baseline models, metrics, uncertainty, seed control and reproducibility.
- Every RL experiment must document environment, observation/action spaces, reward and constraint design, termination, train/evaluation separation, random seeds, compute budgets, and safety/shift tests.
- Include ablations, counterfactual and out-of-distribution evaluation, independent monitoring and failure-case analysis where justified.
- Do not claim learning, autonomy, security, or generalization from deterministic policy code or simulated pass rates without an actual trained/evaluated model and supporting results.
- Record negative findings and the distinction between local validation and end-to-end outcomes.

## Academic provenance and attribution

- Attribute David A. Grand and GRI accurately. Thunderbird is an educational affiliation/context, not a project sponsor.
- Separate original GRI contributions, cited external work, reused code, hypotheses, observations and independently replicated findings.
- Preserve the original Training a Tiger research record; reference it without retroactively changing its methods or metrics.
- Include methods, limitations, exact commit identifiers, test commands and environment records with each new experimental result.

## Required release evidence

A milestone is **proposed** until implemented; **implemented** until tests execute; **tested** until independently reviewed; **validated** only within its documented test scope. Security certifications and production readiness require separate substantiation.

This charter governs future Tiger Legacy changes and cross-references to Training a Tiger and Tiger Assurance. It does not certify current code.
