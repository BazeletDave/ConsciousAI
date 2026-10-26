# GRI Engineering Assurance and ML Evaluation — 26 October 2026

**Status:** independent GRI research acceptance review; **NOT** production release approval.  
**Scope:** ConsciousAI public repository and GitHub workflow metadata. No production mutation, no private storage access, no live database access, no faculty or institutional endorsement implied.

## 1. Release reconciliation — VERIFIED
- PR #38 and PR #39 have **13 identical changed paths and identical patch text** at review time. They must not both be merged.
- PR #39 is the preferred clean integration candidate; PR #38 is redundant at the patch level.
- Both PRs remain open and were based on `c6b3a9e9bef825c341b65155f6646ee9f7b16c27`. The observed current main SHA was `cd65d0c9f8b1d04f3eed86e1aca5a6917c05b27d`. Rebase/recreate release from current main and rerun required checks; do not force push or infer merge readiness from old checks.
- Successful GitHub workflows were observed for staging evidence validation on PR #39 head `58554de0538b30663a6a2f0a4bb36dfb9ad5306a` and research quality gate on main `cd65d0c9f8b1d04f3eed86e1aca5a6917c05b27d`. Successful workflow conclusions do not establish independent production recovery.

## 2. Encrypted independent recovery — CONDITIONAL / BLOCKED
Existing staging implementation includes AES-256-GCM encrypted exports, SQLite backup/integrity verification, portability export, tamper and wrong-key tests, and an explicit recovery runbook. GitHub CI passing establishes automated test execution, **not** independent offsite custody.
**Required before release:**
1. Confirm an independently administered encrypted offsite destination and approved data classification, retention, access and deletion policy.
2. Generate and protect a production-grade backup key in an approved secret manager; never put it in a public repository or logs.
3. Using synthetic data first, create a SQLite staging backup and restricted portable export; record SHA-256 manifest.
4. Encrypt, transfer ciphertext offsite, retrieve from a separate recovery environment, decrypt, verify hashes and SQLite integrity, and restore into an empty staging database.
5. Record UTC times, environment, operator/reviewer, source and restored row counts, recovery duration, and explicit PASS/FAIL. Redact secrets, identifiers, and restricted data.
6. Repeat for real restricted staging data only with authorization. Do not claim PostgreSQL backup, live production integration or disaster recovery until tested.

## 3. End-to-end governed intake — PARTIALLY VERIFIED
The PR contains offline source normalization, deduplication, persistent SQLite candidate/event ledger, quarantine flags, a draft-only research schema bridge, portability export, and automated negative tests.
**Important boundary:** the bridge returns a draft representation and does not establish a write into the deployed GRI production evidence store.
**Required acceptance scenario (synthetic only):**
- Input: rights-cleared synthetic Reddit/YouTube metadata, timestamp with timezone, no personal data.
- Assert HTTPS/domain restrictions, SHA-256 deduplication, ledger persistence, review status `HUMAN_REVIEW_REQUIRED`, `publication_approved=false`, `training_eligible=false`.
- Convert only eligible quarantined candidate to research draft; assert `publication_authorized=false` and source-report claim type.
- Verify export classification `RESTRICTED_STAGING_NOT_PUBLIC`, manifest integrity, tamper rejection, restart/replay deduplication.
- Assert rejection for missing rights, personal data, forged URL, naive timestamp, wrong digest, premature approval and training promotion.
- Production acceptance requires a separately authorized adapter, schema migration, authenticated persistent write, idempotency, reviewer approval, rollback and observed live traces. Do not represent the offline bridge as production-connected.

## 4. ML baseline and scientific validity — PROTOCOL READY / EXPERIMENTS PENDING
Hypothesis: governance checks can improve evidence integrity and prevent unauthorized publication/training while preserving usable research intake.
Pre-register:
- **Unit:** synthetic intake candidate; split by source identity/time, not duplicated record.
- **Outcomes:** invalid acceptance rate (false approval), valid quarantine recall, duplicate-detection precision/recall, evidence trace completeness, policy rejection coverage, processing latency p50/p95, restoration RTO, export hash agreement.
- **Robustness:** tampered content, malformed timestamps, Unicode/URL variants, source update, duplicate replay, missing authorization, missing key, invalid signature.
- **Controls:** rules-only baseline vs rules plus proposed ML classifier; report confusion matrices and uncertainty intervals. No performance claim until experiments run.
- **Drift:** compare feature distributions across time and source domains, alert for provenance or rejection-rate shifts; require human review before policy changes.
- **Ethics:** no participant data or live platform collection in synthetic baseline; distinguish GRI independent work from Thunderbird coursework and endorsement.
- **Gate:** do not deploy an ML decision or claim measured accuracy without reproducible data version, code revision, evaluation report, model card and approval.

## Decision
**GO** for isolated research/staging development and additional tests. **NO-GO** for merging the staging release or asserting independently validated recovery until offsite custody and recovery test are evidenced. Preserve live Render services and The Back Door unchanged.

Links: [PR 38](https://github.com/BazeletDave/ConsciousAI/pull/38) · [PR 39](https://github.com/BazeletDave/ConsciousAI/pull/39) · [GitHub Actions](https://github.com/BazeletDave/ConsciousAI/actions).
