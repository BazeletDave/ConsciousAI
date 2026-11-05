# Global Enrollment and Identity Fraud: GRI Research Stream

Date: October 28, 2026
Status: Research design and dashboard integration contract. Global collection, dashboard display, and ML training for this stream are not implemented by this document.

## Purpose
Extend the [Synthetic Student Paradox](synthetic-student-paradox-2026.md) into comparative institutional research on identity misuse, automated enrollment, simulated participation, financial aid exposure, and the effects of institutional responses. The scope is global, with jurisdiction specific interpretation. GRI does not investigate individual students or substitute for institutional IT investigations.

## Research proposition
AI may lower the cost of producing signals that institutions accept as legitimate participation, while automated defenses may create additional verification burdens for legitimate people. This is a hypothesis for comparative testing, not a universal finding. Distinguish human impersonation, scripted automation, generative AI, and mixed operations. Preserve beneficial outcomes, including expanded access and effective fraud prevention, alongside harms.

## Initial evidence base
1. Participant supplied October 24, 2026 classroom account attributed to Professor Mansour Javidan: spring 2026 enrollment incident. Not independently authenticated or an official ASU finding. Aggregate claims belong in the case narrative and must not become verified training labels.
2. California Community Colleges Chancellor's Office, Fraud Frequently Asked Questions: primary institutional description of scripts, stolen identities, recruited participants, and AI assisted simulated attendance. https://www.cccco.edu/About-Us/Chancellors-Office/Divisions/Information-Services-Technology-Innovation/fraud-prevention/fraud-faq/
3. California Community Colleges Chancellor's Office, August 30, 2021 memorandum DII 21-200-03: bot mitigation, reporting categories, machine learning feedback, and false positive concerns. https://www.cccco.edu/-/media/CCCCO-Website/Files/DII/dii-21-200-03-important-application-and-financial-aid-fraud-a11y.pdf
4. Federal Student Aid, APP-26-09, updated September 21, 2026: identity confirmation, review, and resolution procedures. https://fsapartners.ed.gov/knowledge-center/library/electronic-announcements/2026-07-17/real-time-fafsa-fraud-detection-and-identity-confirmation-frequently-asked-questions-updated-sept-21-2026

Sources 2 through 4 were reviewed October 28, 2026. Their evidence concerns their own systems and jurisdictions; they do not corroborate the specific ASU incident. The initial coverage is United States only. Global is the intended collection scope, not current geographic coverage.

## Record design
Maintain one incident record with separately versioned source and claim records. Multiple publications about one incident must not inflate incident counts.

| Field group | Required information |
| --- | --- |
| Identity and geography | Stable incident ID, country, jurisdiction, institution type, sector |
| Dates | Event interval, publication date, retrieval date, review date; unknown values remain null |
| Provenance | Source URL or restricted source reference, issuing body, document title, source type, version |
| Claims | Claim text, supporting source IDs, attribution, verification state, contradictory evidence |
| Mechanism | Human impersonation, scripts, generative AI, mixed, or unknown; separate evidence for AI attribution |
| Stage | Application, admission, enrollment, participation, aid application, approval, disbursement, recovery |
| Quantities | Reported numerator and denominator, unit, approximate flag, currency and period; no invented precision |
| Institutional response | Control introduced, human authority, review and appeal routes, documented outcomes |
| Consequences | Losses, recoveries, workload, access delays, false positives; unknown differs from zero |
| Governance | Rights basis, personal data flag, reviewer, publication approval, training eligibility |

Claim verification states: attributed report, independent corroboration, official finding, adjudicated finding, disputed, withdrawn, unresolved. Official publication alone does not establish every claim in it. Model confidence must remain separate from evidence verification.

## Continuing learning process
Collect permitted primary institutional sources and peer reviewed studies; preserve dated versions; identify duplicate incidents; extract candidate claims; obtain human review; compare mechanisms and responses; record corrections and outcomes. Reevaluate analyses when evidence changes. Do not infer global incidence rates from a convenience sample of reported incidents. Account for reporting delays, changing definitions, missing denominators, and different national funding systems.

Machine learning research can begin with document relevance classification, duplicate detection, topic clustering, and assisted extraction of mechanisms and institutional responses. These outputs are suggestions requiring review. A public document corpus cannot identify fraudulent individual students.

For model evaluation, use reviewed labels, documented data rights, incident grouped and temporal splits, and jurisdiction held out evaluation where sample size permits. Compare with a simple retrieval or rules baseline. Measure precision, recall, extraction error, duplicate detection error, and reviewer correction rate. Report sample size, uncertainty, geographic coverage, and performance changes over time. Prevent duplicate articles about the same incident leaking across evaluation partitions. Administrative nonresponse, unreviewed model flags, and expired review deadlines are not ground truth fraud labels.

## Dashboard connection
Connect through the existing [Governance Intelligence Registry](../../GRI-Research-Journey/institutional-ai-governance-assurance/intelligence-registry/README.md) and [governed intake](../../research_tools/GOVERNED_SOURCE_INTAKE.md), respecting their actual schemas and staging requirements.

Proposed stream ID: global_enrollment_identity_fraud.
Map reviewed public records into existing registry fields: id, title, domain, source_url, source_type, verification, governance_risk, safeguard, opportunity, review_status, last_reviewed. Keep detailed claims and jurisdiction metadata in a separately validated incident extension rather than silently changing the registry schema.

Proposed dashboard views:
* Incident timeline and geography with explicit coverage limits.
* Mechanism comparison, including unknown AI involvement.
* Evidence and review status with links to primary sources.
* Institutional responses, documented outcomes, and unresolved questions.
* ML evaluation results with model version and evaluation sample.

No autonomous enforcement, individual fraud scores, or automatic evidence promotion. Publication and training eligibility remain explicit human decisions. Classroom material stays within its attributed research boundary and is excluded from public intake and training unless separately cleared.

## Delivery status
As of November 5, 2026, the validated curated source corpus, bounded publisher adapters, scheduled metadata collection, dashboard rendering, and collection health diagnostics are implemented. Their operational limitations are recorded below. Independently evaluated predictive models and causal studies remain pending. The dated sections below preserve the implementation sequence.

## Implemented dashboard connection
October 28, 2026: The research service now implements GET /intelligence/enrollment-research, a dedicated dashboard panel, a validated curated source snapshot, and corpus fitted TF IDF document retrieval registered with platform capabilities. See [implementation and extension instructions](../../GRI-Research-Journey/Research-Governance/ConsciousAI-Research-Systems/ENROLLMENT_RESEARCH.md). The index contains only reviewed institutional summaries; the attributed incident remains outside fitting. The later scheduled discovery section supersedes the initial collection planning status. Collection remains bounded to configured publisher indexes; an independently evaluated predictive model and comprehensive global coverage remain pending. Deployment status must be verified separately from repository implementation.

## Scheduled discovery and adaptive research implementation
October 28, 2026: Added an official publisher metadata collector, a six hour GitHub schedule, persistent source health and discovery history, and a versioned TF IDF title model that updates when its corpus changes. The dashboard now displays discovery status, candidate leads, reviewed comparisons across USA, GBR and AUS, and four proposed study protocols with live related source links. Statistical metadata adaptation does not establish fraud, AI attribution, causal findings or manuscript readiness. A daily GRI Enrollment Research Watch supplements the bounded collectors with primary and scholarly source research and meaningful development alerts. See the implementation instructions linked above for coverage, failure handling, evaluation limits and operational checks.

## Collection reliability and evidence integrity

The November 5, 2026 operational review identified persistent Australian retrieval failures and Education OIG HTTP 406 responses. A workflow could finish successfully while its saved source health showed incomplete coverage. These observations concern research infrastructure, not an increase or decrease in enrollment fraud.

The repair updates the Australian publisher index locations using their public navigation: [Commonwealth Fraud Prevention Centre news](https://www.counterfraud.gov.au/about-us/news) and [ASQA latest news](https://www.asqa.gov.au/newsroom/latest-news). Article paths remain separately bounded because index and article locations differ. A corrected configuration does not establish successful live retrieval; verify the resulting source history.

Temporary network and server failures receive at most three requests with bounded backoff. Access denials and rate limits receive no automatic retry. Each run saves request outcomes and retains a bounded source history, including the previous failure summary when migrating older snapshots. Endpoint corrections do not erase earlier failures or promote retained records into fresh coverage. Git history preserves older snapshots beyond the in-memory history window.

Any incomplete source collection now produces a failed collection workflow after persisting its diagnostic state. The workflow summary, dashboard source cards, and collection health endpoint distinguish source availability from successful software tests. The DOJ district feed covers Northern New York only; its successful fetch cannot replace unavailable OIG coverage or establish nationwide completeness.

Operational acceptance requires passing regression tests, a completed real collection attempt, saved source outcomes, and confirmation that the deployed dashboard exposes those same outcomes. A publisher rejection or outage remains an unresolved external dependency. Human review of permitted institutional sources can supplement collection but must not be represented as automated recovery.

Within the existing AI Paradox research, this supplies an observed example of the dependency between analytical capability, institutional evidence access, and verification. It does not prove causal institutional improvement, predictive model accuracy, or fraud prevalence. Those require independently evaluated outcomes.


## Institutional review summary: November 5, 2026

The deployed repair and saved collection snapshot were checked against the public research endpoint and collection health endpoint. The timestamps agreed. Four of seven configured sources fetched successfully; both Australian sources remained unavailable after bounded attempts, and Education OIG returned HTTP 406. Software validation comprised 244 local regression tests, with repository research systems, research quality, and rights and security checks passing. The collection workflow separately reported failure because source coverage remained incomplete. These are distinct results.

The deployed system adapts a title retrieval index. It is not a validated predictive fraud classifier. Passing software tests does not establish model accuracy, institutional effectiveness, or complete evidence collection. The classroom account remains attributed and independently unverified. No fraud labels or training eligibility decisions were changed.

The following comparative sources were reviewed as additions to the research discussion, not as automatic amendments to the curated case registry:

| Source | Research relevance | Evidence boundary |
| --- | --- | --- |
| [DOJ Michigan sentencing, September 30, 2026](https://www.justice.gov/usao-edmi/pr/three-fraudsters-sentenced-combined-235-months-federal-prison-16m-student-loan-ppp) | Distributed straw student scheme across more than 100 schools; comparison of institutional vulnerabilities and adjudicated outcomes. | More than $16 million awarded differs from more than $10 million collected. Education restitution of $10,521,189.05 is an order, not proof of recovery. Separate unemployment benefits remain separate. Neither scripts nor generative AI are established in this release. |
| [South African Department of Higher Education and Training, July 16, 2026](https://www.gov.za/news/media-statements/deputy-minister-yusuf-cassim-steps-assist-students-facing-nsfas-challenges-16) | Study opportunity concerning verification delays, institutional data exchange, and funding restoration. | The statement reports funding restored for 2,361 cases and 4,138 awaiting academic data. These administrative counts do not establish fraud prevalence, AI involvement, or a measured false positive rate. |
| [Stemmer and colleagues, JMIR, October 8, 2026, DOI 10.2196/93951](https://www.jmir.org/2026/1/e93951) | Peer reviewed empirical study of staged verification and operational costs in remote health research; a methodological comparison for prospective assurance evaluation. | Different sector, temporal comparison, evolving classifications, and possible wrongful exclusions limit transfer and causal inference. Three flagged participants verified their identities; unresolved cases must not be treated as independently confirmed fraud. |

A bounded extension within this research stream would prospectively measure review costs, resolution times, independently confirmed outcomes, and wrongful exclusion. Such a study requires an approved protocol and appropriate data access. It has not been conducted, and no scholarly submission has been published through this repair.
