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
Completed: case expansion, source grounded comparative protocol, and registry documentation cross links.
Pending implementation: incident schema and validator, reviewed seed corpus, source adapters, dashboard rendering, staging validation, evaluated ML models, and any ongoing collection schedule.

## Implemented dashboard connection
October 28, 2026: The research service now implements GET /intelligence/enrollment-research, a dedicated dashboard panel, a validated curated source snapshot, and corpus fitted TF IDF document retrieval registered with platform capabilities. See [implementation and extension instructions](../../GRI-Research-Journey/Research-Governance/ConsciousAI-Research-Systems/ENROLLMENT_RESEARCH.md). The index contains only reviewed institutional summaries; the attributed incident remains outside fitting. Automated global collection, an independently evaluated predictive model, and expanded geographic coverage remain pending. Deployment status must be verified separately from repository implementation.

## Scheduled discovery and adaptive research implementation
October 28, 2026: Added an official publisher metadata collector, a six hour GitHub schedule, persistent source health and discovery history, and a versioned TF IDF title model that updates when its corpus changes. The dashboard now displays discovery status, candidate leads, reviewed comparisons across USA, GBR and AUS, and four proposed study protocols with live related source links. Statistical metadata adaptation does not establish fraud, AI attribution, causal findings or manuscript readiness. A daily GRI Enrollment Research Watch supplements the bounded collectors with primary and scholarly source research and meaningful development alerts. See the implementation instructions linked above for coverage, failure handling, evaluation limits and operational checks.
