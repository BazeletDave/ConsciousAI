# AI Paradox | Initial Synthetic Fixture Assessment and Execution

**Status:** Initial local reproduction of the declared comparison logic, not independent verification or a full repository CI run. Research extension approved by GRI on 30 October 2026.

## Existing fixture assessment

The existing Tiger Legacy tests cover cross tenant denial, purpose scoped grants, expiry, revocation, forged grants, event tampering and replay. Ledger tests additionally cover mutation, truncation, backup, checkpoints and concurrency. Training a Tiger's frozen assurance experiment covers trustworthy, biased and missing observation concerns. These tests support a limited synthetic governance comparison, **not** a production safety claim. The new comparison does not yet integrate the historical putting simulator, ledger attack runner, live human reviewers or real time latency measurements.

## Reproduced comparison

A separate local Python reconstruction of the GitHub comparison runner and its relevant Tiger Legacy authorization methods was executed. This is a preliminary execution check; exact source checkout, latest commit CI and independent reproduction remain outstanding.

| Metric | Denominator | Deliberately permissive baseline | Governed synthetic condition |
| --- | ---: | ---: | ---: |
| Unauthorized actions allowed | 4 | 4 | 0 |
| Legitimate actions allowed | 2 | 2 | 2 |
| Hidden change actions allowed | 3 | 3 | 1 |

The nine fixtures include two legitimate normal tasks, four unauthorized tasks and three hidden change tasks. The governed condition denies the trustworthy positive hazard observation and missing observation but **still allows the biased observation case**. Its synthetic event chain verifies successfully. These are fixture outcomes, not estimates of population safety, empirical risk reduction, or causal effectiveness in deployed systems.

## Limitations and next verification

The baseline is intentionally allow all, not GRI's existing security posture; the comparison therefore favors the governed condition by design. No inferential confidence interval is justified from nine deterministic, author selected cases. The governed condition uses an observation gate with additional information, so resources are not equivalent. No task execution, recovery success, latency, human review costs, real identity authentication, independent sensor validity or adversarial generalization was measured. The local execution was a reconstruction, not a byte identical repository checkout.

**Reproduction command from the repository's `version_one` directory:** `python -m unittest test_comparative_evaluation -v` and `python comparative_evaluation.py`. Verify against the latest committed source and capture CI evidence before elevating result status. Do not alter frozen Training a Tiger results or the operational GRI dashboard.

## Governance

This is an extension of the existing GRI AI Paradox research. No confidential records, client information, production access, autonomous operational actions or external certification are involved. External verification requests follow GRI's private verification policy.
