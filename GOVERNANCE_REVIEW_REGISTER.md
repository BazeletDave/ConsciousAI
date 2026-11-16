# GRI LLC Protection — Engineering Review Register

**Date:** 2026-10-28. **Scope:** BazeletDave public GitHub portfolio; preliminary README and root-file inspection, with targeted engineering guardrails. **Status:** Open actions; no certification.

| Priority | Issue | Evidence / risk | Required follow-up | Status |
| --- | --- | --- | --- | --- |
| P0 | Sensitive intake | CISA ledger prototypes have no production identity, encrypted live storage or offsite replication | Keep intake disabled until separately reviewed and tested | Open |
| P0 | Secrets and participant privacy | Public repos may contain history not covered by README review | Run GitHub secret scanning, dependency and full git-history checks; remediate privately | Not verified |
| P1 | Privacy notices | Root privacy files missing in reviewed repositories | Publish repository policy and deployment-specific notices after factual review | In progress |
| P1 | Security reporting | Root security files missing in reviewed repositories | Enable private vulnerability reporting; assign response owner | In progress |
| P1 | Licensing | MIT licenses present in ConsciousAI, THE-BACK-DOOR and from-code-to-consciousness | Inventory creative IP, images, datasets, music and third-party rights; legal review | Open |
| P1 | Substantiation | ZERO README references placebo-controlled trials and research collaborations | Verify primary records or qualify/remove unsupported assertions | Open |
| P1 | Government association | Treasury exercise repositories include historical stakeholder scenarios | Preserve explicit exercise/not-government endorsement labels | Reviewed at README level |
| P1 | International data processing | Actual geography and data processing unknown | Document applicability of GDPR/UK GDPR, EU AI Act and local laws as applicable | Open |
| P2 | Florida corporate compliance | Entity filings, registered agent, insurance, agreements and annual reports not examined | Verify Sunbiz standing and obtain counsel/accountant review | Open |
| P2 | Operational reliability | Latest deployment, tests, encrypted offsite restore not comprehensively verified | Run CI and independent recovery drill | Open |

## Scope limits
This register is not a full code audit, vulnerability scan, license clearance, regulatory opinion, certification, or review of private organizational records. Existing public history and deployed applications require independent inspection. Each remediation needs an owner, date, evidence and approval before closure.


## November 15, 2026 | Targeted repository governance review

**Reviewer:** ChatGPT-assisted preliminary source inspection on behalf of David Grand, Founder, Grand Research Institute. **Status:** Open and limited; not an independent legal opinion, university clearance, comprehensive security scan, code audit, or institutional certification. No confidential review material was requested or disclosed.

**Inspected directly:** root README, this register, RESEARCH_AND_IP_DISCLOSURES.md, GRI publication/IP policy, GRI academic integrity/rights policy, GRI IP/research security policy, confidential-review reconciliation, targeted mobility research and integrated research files. Repository code search was sampled for academic course identifiers, endorsement/approval language, secrets terminology, reviewer references, and historical institutional relationships. Code search matches are candidate locations, not proof of an actual violation. Full repository trees, all historical commits, binary/media contents, private configurations, GitHub security alerts, deployed services and contractual documents were **not** exhaustively reviewed.

| Priority | Review observation | Disposition / evidence needed |
| --- | --- | --- |
| P0 | No repository-wide historical secrets or PII scan was executed in this review | Keep open; enable and inspect GitHub secret scanning/push protection; perform authorized history, artifact and deployment-log audit; rotate any actually exposed credentials before cleanup |
| P1 | Existing MIT license scope across research, software, creative assets and third-party works remains unresolved | Keep open; inventory LICENSE files, ownership, contributor agreements, images, datasets, manuscripts, code and prior grants with qualified IP counsel; do not claim a new policy revokes historical licenses |
| P1 | Public founder biography has been updated to center David Grand; current 4.0 GPA is founder reported, and transcripts are not publicly available by default | Keep founder-centered language; verify graduation honors and academic claims through authorized records before describing them as independently confirmed |
| P1 | Thunderbird and faculty references appear in research lineage; existing policy appropriately disclaims institutional endorsement | Keep distinction between academic influence, published scholarship and university approval; no confidential coursework or faculty-only materials should be posted |
| P1 | Existing governance documents protect reviewer identities and unpublished findings; technical enforcement and historical exposure remain unverified | Keep review evidence private; audit prior issues, PRs, commits, logs and artifacts before making a blanket confidentiality assurance |
| P1 | Public institutional claims involving Cornell, FAMU, USDA, Bazelet and other historical organizations require case-specific documentary substantiation | Do not expand founder biography into unsupported organizational endorsement or partnership assertions; preserve authorized records outside GitHub |
| P1 | Public data collection, third-party content reuse, global privacy and AI regulatory applicability depend on actual processing and jurisdictions | Map actual controllers/processors, data categories, geographic reach, consent and lawful bases, retention, transfer and research exemptions with counsel |
| P1 | Public research contains observations, hypotheses and engineering assurance claims with different evidence maturities | Preserve existing status labels; confirm any independent reproduction, ethics determination, regulatory approval or certification against specific authorization records |
| P2 | Repository CI, deployed Render/Vercel instances, branch protections, dependencies and backup restoration were not executed or inspected in this review | Keep open; run technical controls separately and attach dated reproducible evidence |
| P2 | Repository-wide academic course identifier searches produced candidate matches in research and generated data, but no disclosure finding was established by excerpts alone | Inspect exact matching text and history before editing; do not publish or duplicate restricted academic content during remediation |

**Release rule for AI-assisted edits:** Treat user authorization to work on the repository as permission to perform only the scoped task, **not** blanket permission to disclose restricted information. Inspect the exact target file and proposed diff; apply least disclosure, rights and academic integrity checks; stop and seek specific approval on uncertain protected material. No automatic publication of reviewer names, confidential coursework, financial records, source data or unreleased methods. Preserve the public David Grand / GRI attribution and explicit institutional independence.

**Legal boundary:** U.S. copyright ownership and work-made-for-hire rules, open source license grants, confidentiality contracts, privacy law, export controls, sector rules and foreign laws cannot be conclusively assessed from a README or code search. Counsel must evaluate facts and jurisdiction. The existence of policies is not proof of enforcement or compliance.

**History warning:** Deleting a public file does not necessarily remove its content from Git history, forks, clones, pull requests or caches. If a true exposure is found, contain and rotate compromised secrets as appropriate, then use GitHub's documented sensitive-data-removal procedure with authorized coordination. Do not force-push or rewrite history merely to cosmetically improve the repository.

**Conclusion:** The inspected governance documents are directionally consistent with independent GRI research and founder-centered attribution. The open issues above prevent any assertion that the entire repository is legally cleared, academically cleared or free of confidential information.
