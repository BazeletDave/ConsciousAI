# Global policy and event intelligence: ingestion controls

The visual graph and API are implemented locally. **No continuously running ingestion job, verified policy feed, or production database exists yet.** The initial official source candidate registry is in [policy_sources.json](policy_sources.json). Candidate homepages are not authenticated ingestion endpoints.

## Two layers

**Layer 1: global policy monitoring.** Prioritize official records from the European Union (Commission and EUR-Lex), ASEAN, United States (Federal Register and White House), then expand to additional jurisdictions. Distinguish legislative proposal, enacted instrument, executive action, regulation, guidance, technical standard, speech and press statement. A political figure's statement is not an enacted legal obligation.

**Layer 2: event intelligence.** User nominated events are recorded in [events.json](events.json) with a title, event date, location, named participants and roles, primary sources, evidence status, verbatim statement references, policy implications, competing interpretations and GRI research connections. The system can link events to the graph only after reviewing sources. Trump administration officials, David Sacks, ASEAN representatives, EU officials and technology leaders may be indexed as subjects of documented public events, without assuming their participation in a particular event.

## Verified ingestion acceptance rules

1. Retrieve an official primary document through an authorized endpoint and record canonical URL, title, publication timestamp, retrieval timestamp and document identifier.
2. Preserve source type and distinguish publication date from effective date.
3. Check duplicate document identifiers and version amendments.
4. Validate claims against source text and log reviewer identity and review date.
5. Mark a record `verified_primary_source` only after a reviewer has inspected the source; ingestion alone is `unreviewed_primary_source`.
6. Track superseded and corrected entries without overwriting history.
7. Never convert event reporting or commentary into legal requirements.
8. Protect privacy and avoid speculative claims of personal influence.

## Production backlog

A scheduled official source collector, source snapshots, immutable change log, human verification queue, event enrichment, authenticated API, persistent database, secure hosting, monitoring and public interactive dashboard are necessary before claiming a real time global tracker. The present dashboard is a local research interface and reflects its checked in datasets.
