# AI Policy Tracker | Research specification

**Status:** A public research dashboard and a configured scheduled U.S. Federal Register metadata intake exist. This is not an independently verified global legal-update or compliance-monitoring service.

## Purpose
Track the legal and institutional environment surrounding AI systems without conflating enacted law, proposed legislation, guidance, technical standards, and company policy.

## Proposed policy fields
`jurisdiction`, `issuing_authority`, `instrument_title`, `instrument_type`, `official_source_url`, `publication_date`, `adoption_date`, `effective_date`, `status_as_of`, `obligations`, `affected_actors`, `enforcement_authority`, `last_verified_at`, `reviewer`.

## Update and verification protocol
1. Ingest primary government or regulator publications.
2. Distinguish proposed, enacted, effective, amended, repealed and advisory status.
3. Record source snapshot, retrieval date and the precise provision relevant to an obligation.
4. Require human verification before publishing consequential interpretations.
5. Version corrections and notify subscribers only when a future notification system has actually been deployed.

## GRI research applications
Compare how rules governing automated decisions, employment, privacy, contestability and enterprise accountability vary across jurisdictions. Institutional comparisons should consider implementation capacity and enforcement, not only written legal text.

**No legal advice:** This research specification does not provide jurisdiction specific compliance determinations. The repository includes a scheduled official-source metadata collector and an unreviewed candidate queue; successful individual runs and current freshness require operational verification. It does not verify legislation in real time or provide legal compliance determinations.
