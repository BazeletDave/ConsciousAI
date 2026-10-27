# Evolving research, governed learning and public presentation

## What changes every collection cycle

The Official Policy Monitor is configured for three hour intervals. Scheduler delays, upstream failures and deployment delays can extend the time between visible updates. A successful workflow is not proof that every source was fetched; source health and successful collection times remain separate. The browser checks the committed country snapshot every minute while visible.

`research_evolution.py` rebuilds a content fingerprinted catalog of public Markdown research in four configured ConsciousAI research scopes: Integrated Research Journey, Algorithmic Management, Institutional Governance and Living AI Ecosystem. The catalog records additions, revisions and removals, with a maximum of 500 documents. Symbolic links, oversized documents and filenames identifying syllabi, assignments, exams or answer keys are excluded. This is a scoped public repository index, not access to private conversations, ASU systems, unpublished course work or every repository in the GRI ecosystem.

TF-IDF weights are recalculated from document titles. Country evidence is connected to up to three research documents using cosine similarity, at least two shared terms and a threshold of 0.12. A small declared Portuguese and Spanish term mapping supports retrieval; it does not establish multilingual model validity. The displayed links are proposed research connections, never corroboration or causal findings. Matches apply only when the evidence ID and content digest still agree with the indexed record.

New public GRI research added within the configured scopes can therefore change retrieval results on the next successful cycle. David Grand's research informed by Thunderbird and ASU study may be indexed when published in those scopes, with its own attribution and limitations. University endorsement and unrestricted rights to teaching materials are not implied. Other repositories require explicit source registration and an appropriate access and rights review; they are not silently searched or incorporated.

## What learns and what remains fixed

The retrieval index adapts to the current research corpus. The active country topic classifier remains the existing instructional Naive Bayes baseline. Evidence refresh, changing retrieval weights and a new topic model release are different events and are displayed separately.

A separate learning candidate can be fitted from `country_intelligence/topic_feedback.json`. Each example must identify a current record and matching content digest, a valid topic, a training or holdout split, approved review status, a named recorded reviewer and cleared training rights. Duplicate IDs and invalid feedback are rejected. Fitting requires ten accepted training records and five accepted holdout records for every topic, distinct sources and normalized text across splits, separate recorded holdout reviewers and a chronologically later holdout. These are engineering defaults, not a claim that this sample size provides scientific adequacy.

When eligible, the candidate is trained and compared with the baseline on held out accuracy. The candidate parameters are isolated from the active model and are not automatically persisted or promoted. Recorded review fields do not authenticate reviewer identity, rights clearance or independence. A production change still requires separately verified review, broader metrics, language and subgroup evaluation, security review and an authorized release. No feedback is approved or fabricated by this build. The current feedback registry is empty, so candidate fitting is correctly blocked.

This provides the ability to develop governed learning while preventing unreviewed news, self generated labels or changing repository text from silently altering production decisions.

## Data quality correction

The previous Brazil MDIC feed exposed directory entries such as year folders. Collection now uses the ministry's latest news feed and an explicit article path constraint. Existing directory candidates are excluded from the current feed with an auditable exclusion record; Git history preserves the prior snapshot. Empty or failed sources remain visible. The change does not reinterpret a folder date as an article publication or a political event.

## Public presentation

The existing institutional header, colors and research identity are preserved. Country evidence is presented eight records per page with publisher links visible and technical provenance in expandable details. Suggested links back to GRI research appear with each matched record. A status line distinguishes the research catalog update, connected evidence, fixed active model and blocked or evaluated learning candidate. Changing countries clears the previous country's results while the next request loads.

The existing public desktop page was inspected directly in the browser, including its header and country controls. Local DOM checks cover pagination, research connections and country switching. A rendered mobile viewport was not available from the current browser interface; mobile layout remains a separate visual acceptance check. No image assets or unrelated game site content are changed.

## Verification and operational boundaries

Run `python -m unittest discover -v`, `node --check country-intelligence.js`, and `python research_evolution.py` from this directory. The read only `/institutional/research-evolution` endpoint exposes catalog, connection and candidate provenance. The country API includes the compact status and digest matched links.

All local tests use synthetic data or committed research snapshots. Real source retrieval is exercised separately by the collector. Public GET health and country navigation were verified before the change. Management API deployment metadata and resource metrics remain unavailable until an intended Render workspace is selected; public endpoint responses alone do not verify those internals. Newly implemented changes require merge and post deployment acceptance before being described as live.

The final local verification passed 129 service tests, including document change tracking, proposed connections, review and source digest rejection, isolated candidate fitting, source leakage prevention, directory exclusions and the research evolution API. DOM checks passed for eight record pagination, expandable provenance, linked research, country switching cleanup and Israel loading. The development index contains 44 research documents and 17 proposed evidence connections. These are snapshot counts, not independently verified findings.
