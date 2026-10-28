# Live enrollment research and adaptive discovery

The dashboard at /dashboard#enrollment-research consumes GET /intelligence/enrollment-research?q=identity&country=USA. It displays an attributed classroom account and nine reviewed institutional references across the United States, United Kingdom, and Australia. The source comparisons include court reporting, parliamentary findings, a regulatory audit, policy guidance, and institutional descriptions. They do not all establish AI involvement or the same fraud mechanism. Counts are source records, not global prevalence estimates.

## What runs automatically

The gri-enrollment-research.yml GitHub workflow collects allowlisted official publisher metadata every six hours, with immediate runs on collector or source configuration changes. It retains up to 300 URL deduplicated titles for up to 365 days, records per source success or failure, and preserves previously collected records when a source request fails. The generated state and model are committed together. The existing Render deployment path publishes them to the dashboard. GitHub scheduled execution is best effort and can be delayed.

Each successful collection fits a TF IDF vocabulary and normalized document vectors to publisher titles. The model version increments only when the title corpus changes. Its digest, vocabulary size, document count, and recent update history are visible. Query cosine similarity and proposed study links update with that corpus. This is unsupervised document retrieval adaptation, not continuous training of a predictive fraud model, independent claim verification, or autonomous scholarly judgment. Independent relevance precision and recall remain unmeasured.

Reviewed source retrieval remains a separate index of GRI authored institutional summaries. Participant material is excluded from both fitting paths. No article bodies or individual student records are collected. Discovery titles are visibly unreviewed and cannot automatically become verified claims or fraud training labels. Sources are fetched with timeouts, bounded response sizes and same host redirects; URL destinations are constrained to institutional hosts.

## Research opportunities

The versioned opportunity registry defines four proposed study directions: evidence for AI attribution; fraud control and student access; incentives and fragmented oversight; administrative label quality. Each includes source IDs, a research question, proposed method, measures and a possible paper type. Live title matches are appended as research leads. These are proposed studies, not findings or submission ready manuscripts.

A separate daily GRI Enrollment Research Watch checks authoritative primary and scholarly sources for meaningful new findings and persistent collector failures. It notifies David only when there is a substantive development. It does not submit manuscripts or publish findings autonomously.

## Operations and verification

Run:

```bash
python -m unittest discover -v
python enrollment_discovery.py
```

Inspect enrollment_discovery.json for last run, last successful fetch, source failures, history, and corpus digest. The dashboard marks snapshots older than 18 hours as stale. If all sources fail, the workflow persists failure status and retained records, then fails visibly. Public access restrictions and source format changes are reported rather than bypassed.

To expand discovery, add an approved institutional endpoint to enrollment_sources.json within the fixed host allowlist in enrollment_discovery.py; review its metadata rights and schema and add a parser test. To add a reviewed comparison, edit enrollment_research.json with explicit attribution, evidence detail and unknowns. Do not infer a financial loss from a suspicious activity amount or an AI mechanism from identity fraud alone.

The separate intelligence registry retains its existing schema and source schedule. This module adds its own bounded research stream and does not change existing collectors or operational enforcement.
