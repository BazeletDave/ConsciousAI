# Tiger Legacy Version One — Research Methods and Results

**Research lead:** David A. Grand, Grand Research Institute  
**Academic affiliation:** Thunderbird School of Global Management, Arizona State University (independent work; no sponsorship or endorsement).

## Research question and hypotheses

Does a synthetic institutional assurance architecture distinguish locally compliant decisions from end-to-end trustworthy evidence, particularly under identity spoofing, consent revocation, event tampering, ledger truncation and CI artifact substitution?

- **H1 (testable):** Specified synthetic authorization and evidence-integrity invariants hold under declared deterministic fixture tests.
- **H2 (testable):** A separately retained checkpoint detects a ledger truncation that a locally self-consistent hash chain cannot detect alone.
- **H3 (testable):** A version-controlled report digest and signed CI provenance enable reproducible artifact attribution, without establishing truth or operational security.
- **Null interpretation:** Passing these tests does not imply real-world security or effectiveness outside their stated fixtures.

## Method

**Design:** Deterministic synthetic, non-human-subject software experiments with positive/negative controls and adversarial fault injection.  
**Population:** No real clients, people, accounts or production datasets.  
**Inputs:** Fixed synthetic resource identifiers, tenants, grants, consent expiry, event IDs, ledger mutations and report digests.  
**Dependent measures:** Test pass/fail; fail-closed authorization, HTTP status, event-chain verification, checkpoint comparison, signed artifact verification.  
**Environment:** Python standard library, SQLite, GitHub-hosted Actions; exact versions should be recorded by independent reviewer.  
**Replication:** `verify_release.py`, `INDEPENDENT-REPRODUCTION-PROTOCOL.md`, and CI quality workflow.  
**Analysis:** Counts and binary invariants, not inferential statistics; no generalization beyond enumerated scenarios.  
**Bias controls:** Fixed fixtures and explicit negative tests; developer-authored tests can omit important attacks. Independent review is therefore a separate gate.

## Historical results and new unverified work

**Previously verified:** GitHub Actions run 40972028096 completed 16 Tiger Legacy tests and 217 dashboard tests, signed attestation publication, full-checkout reproduction and GitHub CLI attestation verification. These findings pertain to commit `8f1e4fe3a2dffeb3e181ba557345721b72ac232b`.

**Newly implemented, awaiting fresh CI verification:** SQLite durable evidence ledger; 12 adversarial tests (including replay, concurrent appends, backup/restore, mutation, privileged truncation and external checkpoint mismatch); formal threat model; independent review protocol. No claim of passing these new tests until the new commit's workflow is checked.

## Limitations and negative results

- No trusted principal authentication or operational security controls.
- Local SQLite triggers are bypassable by a privileged database operator; externally retained checkpoint is required for truncation detection.
- No externally operated checkpoint custodian or independent academic reviewer yet exists for this research.
- GitHub signed provenance attests workflow identity and artifact digest, not correctness of the code, experiment or conclusions.
- No empirical evidence of real client remediation, production availability, media security, recovery-time objectives, ML/RL learning, or generalization.

## Preservation and attribution

The original Training a Tiger experimental results are preserved as separate, unmodified source research. Its recorded limitations and metrics cannot be represented as Tiger Legacy cybersecurity outcomes. Source links and reproducibility steps are maintained in the evidence package. Do not overwrite frozen experiments to align with new findings.

## Release standard

Document source revision, code and tests, test execution, signed provenance, negative findings, threat-model assumptions, independent reviewer evidence and publication limitations before upgrading claims. Production deployment and external integration require separate authorization and review.
