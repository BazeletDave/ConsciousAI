# Tiger Legacy Version One | Engineering Reproduction Baseline
**Baseline initiated:** 2026-10-30  
**Classification:** Synthetic research only; no client access, production deployment, or independent certification.  
**Candidate branch:** `tiger-legacy-identity-hardening-20261030`  
**Status:** Historical CI confirmed; current candidate branch verification and independent external reproduction **pending**.

## Confirmed historical evidence
- Reviewed source commit: `8f1e4fe3a2dffeb3e181ba557345721b72ac232b`.
- GitHub Actions run: https://github.com/BazeletDave/ConsciousAI/actions/runs/40972028096 ; completed successfully.
- Successful job steps include Tiger Legacy synthetic tests, dashboard regression, release reproduction script, signed provenance publication, and GitHub CLI attestation verification.
- Recorded historical counts: 16 Tiger Legacy tests and 217 dashboard tests. Counts describe the historical tested revision only.

## Current candidate and evidence maturity
- The branch `tiger-legacy-identity-hardening-20261030` exists, but this baseline does **not** claim a successful CI run for its current HEAD.
- Latest source commit SHA, environment/tool versions, complete test output, dependency inventory, and independent attestation must be captured before promoting this candidate to a verified baseline.
- Existing research describes a SQLite ledger and 12 additional adversarial tests; their current execution outcome is **not verified in this record**.
- No external independent reviewer has yet supplied a signed reproduction result.

## Reproduction instructions for an independent reviewer
1. Record the immutable HEAD SHA of the candidate branch and clone that exact commit on a separately controlled machine.
2. Record OS, Python, SQLite, GitHub CLI versions, reviewer identity/affiliation and any conflicts.
3. From repository root run: `python GRI-Research-Journey/Research-Governance/Tiger-Legacy/verify_release.py`.
4. From `GRI-Research-Journey/Research-Governance/Tiger-Legacy/version_one` run: `python -m unittest discover -s tests -p 'test_*.py' -v`.
5. Capture full stdout, stderr, exit codes, test counts, failures, and exact reviewed commit.
6. Verify the relevant signed artifact with `gh attestation verify GRI-Research-Journey/Research-Governance/ConsciousAI-Research-Systems/tiger_legacy_synthetic_snapshot.json --repo BazeletDave/ConsciousAI`, recording signer identity, artifact digest, and associated workflow/commit. Do not treat an attestation for an earlier revision as evidence for the current candidate.
7. Execute the independent checkpoint custody, tamper, replay and truncation challenge from `INDEPENDENT-REPRODUCTION-PROTOCOL.md`, preserving failures.
8. Verify that all data are synthetic and that original Training a Tiger findings and HTTP regression behavior remain separate and intact.

## Acceptance gates
- [x] Historical CI and provenance verification observed for the specified historical commit.
- [x] Reproduction script and independent review protocol exist.
- [ ] Exact current candidate HEAD and full current CI evidence recorded.
- [ ] Fresh complete regression and adversarial suite independently reproduced.
- [ ] Independent custody and rollback challenge documented.
- [ ] Third-party reviewer signs findings and residual-risk register.
- [ ] Production identity, client isolation, key custody, recovery and authorization assessed before any client pilot.

**Security interpretation:** Successful tests prove only the enumerated synthetic assertions in the reviewed environment. Signed provenance authenticates build lineage, not security efficacy or research validity. No real client data or production access is authorized by this document.
