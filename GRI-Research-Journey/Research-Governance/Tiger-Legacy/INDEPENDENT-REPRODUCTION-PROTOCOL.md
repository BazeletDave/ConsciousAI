# Independent Reproduction Protocol — Tiger Legacy Version One

**Author:** David A. Grand | Grand Research Institute  
**Status:** Reviewer-ready protocol; **no independent external reviewer has yet attested to completing it**.

## Reviewer independence

The reviewer must not be the implementation author or rely solely on the developer's local environment. Use a separately controlled workstation/account, record reviewer identity/affiliation (with consent), conflicts of interest, date, OS, Python, SQLite and GitHub CLI versions, and commit SHA. Do not request client access or client data.

## Steps

1. Obtain an exact checkout of the review commit from `BazeletDave/ConsciousAI`; compare commit SHA and changed files with the draft PR.
2. Inspect `FORMAL-THREAT-MODEL.md`, `version_one/evidence_ledger.py`, `version_one/tests/test_evidence_ledger.py`, and `REPRODUCIBLE-EVIDENCE-PACKAGE.md`.
3. Run `python GRI-Research-Journey/Research-Governance/Tiger-Legacy/verify_release.py` from the repository root. Record exact exit status, all stdout/stderr and test counts.
4. Run `gh attestation verify GRI-Research-Journey/Research-Governance/ConsciousAI-Research-Systems/tiger_legacy_synthetic_snapshot.json --repo BazeletDave/ConsciousAI`; capture verified identity, artifact digest, attestation subject and workflow.
5. Independently run `cd GRI-Research-Journey/Research-Governance/Tiger-Legacy/version_one && python -m unittest discover -s tests -p 'test_*.py' -v`.
6. Test separate original `/institutional/tiger-assurance` and new `/institutional/tiger-legacy` endpoints for expected 200 and simulated-integrity-failure 503 responses using the repository HTTP test suite.
7. Create a fresh synthetic SQLite ledger, export checkpoint to an **independently held file or system**, delete/alter the local ledger using a test fixture, and verify mismatch against the independently retained checkpoint.
8. Confirm absence of client data, actual authentication, production security claims, or autonomous operational authority. Record unresolved issues.

## Independent review result template

- Reviewer / affiliation / conflict disclosure:
- Review date and source commit:
- Python / SQLite / OS / gh CLI:
- Exact commands and exit codes:
- Signed attestation ID and verified signer identity:
- Original Training a Tiger unchanged (yes/no/evidence):
- Ledger tamper/replay/truncation tests (results):
- Residual security risks and unverified claims:
- Exceptions / failed tests:
- Conclusion (reproduced, partially reproduced, not reproduced):
- Reviewer signature or independently verifiable record:

## Interpretation rule

An external review cannot be claimed until an actual independent reviewer completes the protocol and provides their evidence. CI is third-party-hosted execution but **not** an independent academic or security review. This document is a protocol and handoff package, not an invented endorsement.
