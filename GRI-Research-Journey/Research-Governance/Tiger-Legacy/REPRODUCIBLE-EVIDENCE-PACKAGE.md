# GRI Tiger Legacy — Reproducible Evidence Package

**Classification:** Synthetic research; not production cybersecurity certification.  
**Research lead:** David A. Grand, Grand Research Institute.  
**Branch:** `research/tiger-legacy-foundation-2026`  
**Independent review status:** Ready for third-party reproduction; not independently audited.

## Historical verified evidence (29 October 2026)

- Successful full-repository GitHub Actions quality run: https://github.com/BazeletDave/ConsciousAI/actions/runs/40971762357
- Source commit tested: `98e4dd901fc52b5d23d5bad43b06e29bebf7dcd2`
- Quality workflow logs: Tiger Legacy **16/16** tests passed; dashboard suite **217/217** tests passed (dashboard suite executed twice).
- Existing Training a Tiger HTTP assurance route: 200 for retained valid evidence; 503 for simulated integrity failure, as verified by `test_original_tiger_assurance_route_retains_contract`.
- GitHub Actions provenance step **succeeded**, attestation https://github.com/BazeletDave/ConsciousAI/attestations/61527064
- Sigstore Rekor transparency log index **3578807002**, https://search.sigstore.dev/?logIndex=3578807002
- Note: Successful publication to GitHub and Rekor was observed in the GitHub job logs. **A separate verifier result was not available at the time of this record**; do not confuse attestation publication with signature verification.

## Reproduction procedure

From a complete checkout of the exact reviewed commit:

```bash
python GRI-Research-Journey/Research-Governance/Tiger-Legacy/verify_release.py
gh attestation verify GRI-Research-Journey/Research-Governance/ConsciousAI-Research-Systems/tiger_legacy_synthetic_snapshot.json --repo BazeletDave/ConsciousAI
```

The first command checks the pinned snapshot SHA-256 and fail-closed classification, runs the complete dashboard suite (including the Training a Tiger endpoint contract), and runs the Tiger Legacy security and reporting suite. The second asks the GitHub CLI to verify a GitHub attestation against the named repository identity. Record tool versions, tested commit, exit codes and full logs.

The research quality workflow also runs these steps in GitHub-hosted CI on eligible same-repository PRs. **New verification steps must pass before the new commit is classified as verified.**

## Evidence boundaries

The snapshot contains synthetic fixture results only; it does not contain production authorization outcomes or independent security audit evidence. Its self-digest and repository manifest detect unexpected changes under the assumed repository trust boundary. GitHub's signed attestation binds an artifact digest to an authenticated workflow identity, not to the truth of research conclusions.

## Preservation of original Training a Tiger results

The existing `Training-a-Tiger-AI-Paradox` research artifacts and source-frozen experiment remain unmodified by this package. The pre-existing `/institutional/tiger-assurance` endpoint retains its separate bridge and classification. Tiger Legacy's endpoint `/institutional/tiger-legacy` is an additional, synthetic-only read-only interface; it does not promote, replace, or reinterpret the original experiment. Historical research results must remain independently attributable to their original source and limitations.

## Independent review checklist

1. Confirm exact Git commit and compare checkout to reviewed PR.
2. Run both full test suites, retain complete stdout/stderr and exit codes.
3. Verify SHA-256 manifest and GitHub signed attestation, inspect certificate identity and source workflow.
4. Confirm 200/503 behavior of original Training a Tiger route and new Tiger Legacy route.
5. Confirm synthetic-only classification and absence of secrets/client data in public summaries.
6. Challenge trust assumptions: compromised repository, compromised CI, signed-but-false results, and non-durable HMAC evidence.
7. Record independent findings and unresolved risks; do not equate passing tests with certification.

**Release control:** No production merge or Render deployment is authorized by this evidence package.

## Subsequent verified checkpoint

**Run:** https://github.com/BazeletDave/ConsciousAI/actions/runs/40972028096  
**Commit verified:** `8f1e4fe3a2dffeb3e181ba557345721b72ac232b`  
**Outcome:** GitHub Actions research quality job completed successfully. The full-checkout `verify_release.py` step and GitHub CLI `gh attestation verify ... --repo BazeletDave/ConsciousAI` step both completed with success. Original Training a Tiger HTTP regression, synthetic report integrity, 16 Tiger Legacy tests and 217 dashboard tests passed. This closes the prior *signature verification pending* checkpoint for the tested commit.

**Important provenance distinction:** This package was subsequently edited on the same branch, so the verified run does not automatically attest to later documentation commits. New commits require their own CI results. GitHub identity verification is independent of the in-repository manifest but is not a third-party security audit or validation of experimental truth.
