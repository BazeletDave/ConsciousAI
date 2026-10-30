# Independent reproduction packet — reviewer instructions and disposition

**Status: PENDING EXTERNAL EXECUTION.** The authoring assistant is not an independent reviewer. GitHub green checks are automated engineering evidence, not independent reproduction.

## Fresh-checkout procedure
1. Have a reviewer with no role in authoring these experiments clone `BazeletDave/ConsciousAI` at the precise PR #94 head SHA.
2. Record the commit SHA, OS, Python version and complete command output.
3. From `GRI-Research-Journey/Research-Governance/Tiger-Legacy/iaf_experiments`, execute:
   ```sh
   python3 -m unittest discover -s . -p 'test_*.py' -v
   python3 validation_bundle.py > validation-bundle.json
   python3 -m json.tool validation-bundle.json >/dev/null
   python3 qlearning_governance.py > qlearning-report.json
   python3 ood_governance.py > ood-report.json
   sha256sum validation-bundle.json qlearning-report.json ood-report.json
   ```
4. Confirm nonzero failure on intentionally modified fixture expectations, a wrong ledger key, altered ledger payload, and mismatched checkpoint **in an isolated copy**.
5. Independently inspect all eight fixture labels, five trajectory events, six OOD probes, baseline comparator and the Q-learning reward/policy design. Check for author-defined evaluation bias.
6. Compare results with a second fresh checkout and record differences. Sign a reviewer report including limitations and any failures.

## Acceptance criteria
- All discovered tests execute and pass; test count and log retained.
- The consolidated bundle is valid JSON and includes Q-learning, OOD, ledger and fixture outputs.
- Repeated execution under a pinned environment yields the same deterministic report fields and input digests.
- Reviewer confirms a separate train/evaluation seed but does not describe it as distribution-independent validation.
- Reviewer confirms ledger checkpoint lacks independent custody; no external attestation claim.
- Academic claims use only the verified bibliography register and explicit GRI-inference labels.
- PR stays in draft until reviewer signoff and human merge approval.

## Evidence / limitations
- The GitHub workflows for prior head `58580083e1c30e83621d29c2cdf022a05e1222fa` reported success for Research rights and security checks and GRI Research Quality Gate.
- A fresh external clone was attempted in the assistant's execution environment, but failed due to DNS resolution of github.com. No fresh-checkout result was produced there.
- No independent reviewer has signed or submitted reproduction evidence.
- No claim of production readiness, real-world ML robustness, or independent academic certification.
