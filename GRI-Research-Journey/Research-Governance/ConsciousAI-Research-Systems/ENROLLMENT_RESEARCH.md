# Live enrollment research and adaptive discovery

The dashboard at /dashboard#enrollment-research consumes GET /intelligence/enrollment-research?q=identity&country=USA. It displays an attributed classroom account and nine reviewed institutional references across the United States, United Kingdom, and Australia. The source comparisons include court reporting, parliamentary findings, a regulatory audit, policy guidance, and institutional descriptions. They do not all establish AI involvement or the same fraud mechanism. Counts are source records, not global prevalence estimates.

## What runs automatically

The gri-enrollment-research.yml GitHub workflow collects allowlisted official publisher metadata every six hours, with immediate runs on collector or source configuration changes. It retains up to 300 URL deduplicated titles for up to 365 days, records per source success or failure, and preserves previously collected records when a source request fails. An open dashboard rechecks published state every minute while visible; this does not launch extra collection jobs. The generated state and model are committed together. The existing Render deployment path publishes them to the dashboard. GitHub scheduled execution is best effort and can be delayed.

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


## AI Paradox: institutional verification and evidence integrity

Independent GRI analytical extension, October 30, 2026.

The hypothesis is that digital activity can satisfy administrative checks while identity, actual participation and entitlement remain inadequately established. Enrollment, participation, aid eligibility and payment authorization require separate evidence. Apparent compliance at one stage does not establish validity at the next.

Apply Roy C. Nelson's institutional framework to incentives, formal rules, organizational responsibility and enforcement capacity. This is GRI's analytical application, not a claim of faculty endorsement. Ask who can verify, suspend, contest and correct each decision, and whether institutional rewards favor processing volume over reliable verification.

### Official comparison and attribution limits

The [DOJ Operation Ghostbusters announcement, October 29, 2026](https://www.justice.gov/usao-edva/pr/justice-department-unveils-indictments-nationwide-ghost-student-fraud-scam-linked) reports charges concerning alleged identity misuse, enrollment and aid refund diversion. Charges remain allegations. It reports more than $32 million in FBI identified losses in similar schemes, 830,840 potentially fraudulent FSA IDs associated with nearly $130 million, and more than $750,000 in cryptocurrency seized. These measures must not be combined or described as adjudicated losses or restitution.

The release describes simulated participation and coursework with the phrase “super intelligence,” without identifying models, providing technical logs or offering reproducible attribution. This supports a research question about AI involvement, not a demonstrated generative AI mechanism. It does not corroborate any separate classroom report.

### Proposed study within the existing stream

| Stage | Research question | Proposed measurement |
| --- | --- | --- |
| Identity and enrollment | Which decisions establish identity rather than accept an application? | Resolved impersonation findings and corrected flags |
| Participation | What establishes who performed the activity? | Verified actor attribution and unresolved cases |
| Aid and payments | How does evidence pass between responsible institutions? | Attempted, awarded, disbursed and recovered amounts separately |
| Contestability | Who can reverse an unsupported decision? | Review time, reversals and restored access |
| Assurance collection | Can unavailable evidence be mistaken for a completed check? | Source coverage, failure duration and explicit unknown states |

These are proposed measures, not measured results. Independently reviewed, authorized evidence is required before evaluation or training. Separate identity theft, scripts, generative AI, provider misconduct and disengagement. Nonresponse and model similarity are not fraud evidence. Retain confidential evidence internally and disclose only approved metadata or findings.

Operational availability and evidence completeness require separate measurements. A collection success elsewhere cannot establish that every relevant source was checked. Failed or unavailable checks must remain unknown rather than count as successful verification. Repairing collectors and extending collection health coverage are follow up engineering tasks; this document does not claim those repairs are complete.

This addition extends the existing research stream. It changes no individual fraud labels, activates no predictive training and submits no scholarly manuscript.

## Collector recovery and health coverage

The DOJ Northern District of New York collector now uses the RSS endpoint advertised by its official press release index. RSS parsing retains titles, links and publication dates only, checks the expected document structure, rejects entity declarations, and applies the existing host and article path restrictions. A valid feed containing no relevant titles is distinct from an access wall or parsing failure.

Enrollment discovery is included in GET /health/collections. Each source exposes its latest attempt, last successful fetch, HTTP error code where available, failure streak since this instrumentation began, and intervention category. A recent collection attempt cannot hide a failed source. Successful collection clears the failure streak; retained records do not count as a successful fetch.

The six hour collection cadence and 18 hour stale threshold are separate. A successful but overdue snapshot is marked delayed after six hours, stale after 18 hours; missing, invalid and partial source states require attention. This diagnostic remains separate from server readiness, so a publisher failure does not take the dashboard offline.

Education OIG returned HTTP 406 during the October 30 repair check, including its public homepage. This is an unresolved publisher access limitation, not a repaired parser or an empty result. It remains enabled and visibly failed for subsequent scheduled checks. An accessible publisher approved endpoint or manual institutional review is required if access continues to be denied. Public access restrictions are not bypassed. Temporary upstream errors elsewhere are likewise retained explicitly.
