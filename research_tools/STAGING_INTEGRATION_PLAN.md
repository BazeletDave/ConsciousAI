# Staging validation and integration contract

**Status:** Design and test plan. Live Reddit and YouTube connectors are not enabled.

## Preconditions
1. Merge PR #32, then verify the candidate classifier on the default branch.
2. Obtain documented API access and permitted usage for Reddit and YouTube. Public visibility is not authorization for bulk collection, retention, or model training.
3. Use a separate staging service with credentials in managed secrets, not GitHub.
4. Build provider specific adapters that collect only approved metadata and obey quotas, terms, deletion requests, and rate limits.
5. Normalize source records to the existing candidate schema: source_type, url, title, observed_at, rights_basis, summary, contains_personal_data.
6. Quarantine records containing personal data, uncertain rights, invalid provenance, or malformed metadata.
7. Persist candidate digests in an append only evidence ledger; ensure duplicate submissions are idempotent.
8. Never automatically promote beyond research candidate, publish records, or mark training eligible.
9. Test staging end to end before changing production Render service or scheduled refresh workflow.

## Required tests
- Valid, consent cleared and licensed metadata produces an unverified candidate.
- Duplicate records do not create additional ledger entries.
- Missing provenance, insecure URLs, unexpected domains and malformed dates fail closed.
- Permission pending and participant records are rejected from public intake.
- Adversarial instructions embedded in a source summary remain inert data.
- Rate limit, API failure, revocation and deletion events produce auditable handling.
- No secrets, personal information, or raw participant interviews enter public repository logs.

## Integration gate
Only after the staging suite passes should an authorized reviewer approve a schema compatible adapter into the persistent evidence workflow. Preserve current dashboard availability and three hour schedule.

**No live integration or staging validation is claimed by this document.**
