# GRI Institutional AI Intelligence Framework

Status: Research engineering release candidate. Not production certified.

## Integrated architecture
Evidence intake and content fingerprints -> persistent local evidence ledger -> provenance-aware typed intelligence graph -> benchmark and model evaluation -> candidate registry -> capability-scoped agent decisions -> collector observability -> independent release assurance.

## Institutional governance
1. Frame the research question and record scope, jurisdiction and evidence rights.
2. Preserve source attribution and distinguish verified facts from inferred links.
3. Evaluate models using independently reviewed datasets and leakage controls.
4. Assess uncertainty, adverse outcomes, drift and failure modes.
5. Require authenticated approvals for consequential actions and model promotion.
6. Stage, verify rollback and monitor before any production release.
7. Document independent review, scientific limitations, and correction mechanisms.

## Operational constraints
No prototype in this directory automatically trains, deploys, publishes, calls external tools, or modifies production. SQLite is an application-level append interface, not tamperproof storage. Evidence digests do not authenticate sources. Human approval flags in tests are not authenticated approvals. Model accuracy is not scientific validation. A green CI check does not certify production readiness.

## Release acceptance
All automated tests pass; source rights and licensing verified; independent benchmark adjudication completed; security and privacy reviewed; authenticated institutional approval recorded; staging rollback demonstrated; live monitoring verified. Any missing requirement blocks production promotion.

## Deployment pathway
The Render services are configured to auto deploy on commits to main. This research directory is additive and not imported by the current dashboard server. Merging documentation and isolated modules does not itself activate new production features. Operational integration requires a separate, reviewed implementation and staging evidence.
