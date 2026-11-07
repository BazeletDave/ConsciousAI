# Dataset 12: governed mobility intelligence integration

Status: implementation workstream initiated, research prototype only. No live data ingestion, deployed ML, platform integration, or verified driver earnings claimed.

## Components supplied October 24, 2026
1. Voluntary consent offer/trip ledger and scenario planner.
2. Dispatch optimizer with class, return-home, and sleep constraints.
3. Draft JSON Schema 2020-12 for RESEARCH_DATASET_12.
4. Raw telemetry transformation and H3 zone handling.
5. Two illustrative pilot fixtures (one accepted Uber offer, one declined Lyft offer). These are **unverified examples**, not independent field observations.

## Required corrections before ingestion
- Use H3 v4 latlng_to_cell and reject synthetic H3 fallback indexes. Apply aggregation and disclosure controls; H3 cells are not anonymous by themselves.
- Replace hardcoded salt and truncated plain SHA256 with protected HMAC, plus separately governed consent evidence, withdrawal and retention policy.
- Separate OFFER_ACCEPTED from TRIP_COMPLETED and PAYMENT_SETTLED. Declined offers have no realized earnings or incurred trip expenses by default; preserve hypothetical costs in distinct counterfactual fields.
- Distinguish incentives already included in payout to prevent double counting. Record currency, cost model, assumptions and version. $0.38/mile is a research assumption, not a verified IRS rate.
- Validate nonnegative finite numbers, timestamps, coordinates, platform enums, UUIDs, and computed arithmetic. Maintain raw-source provenance without publishing identifying records.
- Model return travel in full commitment time; use timezone-aware timestamps and uncertainty buffers for deadlines and sleep constraints.
- Keep source reports, simulations, and verified consented trip observations in distinct evidence classes.

## Engineering implementation sequence
1. Version schema, build typed validation and negative test fixtures, and run locally in CI.
2. Implement consent registry interface and private data processing boundary; no personal records in public repository.
3. Add ingestion adapters only for permitted public APIs and consented submissions, with source URL, license, timestamps, deduplication, and quality scoring.
4. Establish baseline statistical and ML models only after sufficient independent labeled data; use temporal holdouts, calibration, uncertainty and drift checks.
5. Add read-only aggregated mobility research endpoint to existing dashboard service behind feature flag after integration tests and deployment review. Preserve all existing services.

## Governance gates
Human review for publication, model promotion, source access expansion, and external actions. No automated offer acceptance or driver account access. No unapproved scraping of restricted communities. No production deployment authorized by this document.

## Research framing
Compare platform offer economics, driver decisions, counterfactual outcomes and institutional accountability under the GRI AI Compliance Paradox. Faculty frameworks are educational context, not endorsement. Report self-reported platform figures as claims rather than independent findings.


## November 7, 2026 | Institutional legitimacy and public perception research engineering specification
**Scope:** Extension of Dataset 12 and the [existing strategic mobility assessment](../../Uber-Lyft-Research/2026-11-07-strategic-mobility-transition-assessment.md) only. This is a prospective research specification, not a trained model, a deployed service, or validated findings.

**Core question:** Under which institutional conditions can mixed human/AV mobility maintain safety accountability, economically meaningful driver choice, legitimate public authority and public trust?

### Evidence dimensions
1. **Formal rules:** Jurisdiction, effective date, statutory authority, AV operating permissions, safety reporting duties, labor and consumer protection, public notice, appeals and incident accountability. Link primary legal text; classify proposed versus effective rules.
2. **Operational implementation:** Actual service domain, human fallback, fleet assignment rules, safety escalation, incident and complaint resolution, versioned software/hardware, and evidence access. Do not infer implementation from policy documents.
3. **Public perception:** Representative surveys when available; otherwise consented interviews, public testimony and public online discussions with explicit nonrepresentative sampling labels. Record sentiment target (safety, fairness, jobs, privacy, service), stakeholder role, geography, source date, sampling frame and uncertainty. Do not equate social-media volume with population support.
4. **Economic experience:** Consented driver offer, acceptance, trip and settlement records, net hourly earnings, unpaid time, incentives, operating costs, and geographic AV exposure; maintain the Dataset 12 distinctions already specified.
5. **Outcomes:** Service availability, wait time, completion, driver earnings, safety incidents with exposure denominators, public complaints and resolved appeals. Avoid causal conclusions without credible comparison groups.

### Proposed normalized records
`institutional_rule`: rule_id, jurisdiction, source_url, effective_date, legal_status, affected_actor, obligation, enforcement_authority, revision_id, reviewed_by.
`public_perception_observation`: observation_id, date, region_aggregate, stakeholder_category, question_or_topic, instrument_or_platform, sample_method, sample_size_if_known, sentiment_or_position, evidence_class, uncertainty, consent_or_public_basis, provenance_id.
`deployment_observation`: observation_id, operator_claim, service_zone_aggregate, time_window, driving_mode, ODD, source_type, independent_verification_status, vehicle_count_if_confirmed, provenance_id.
`decision_accountability`: decision_id, responsible_party, delegated_authority, contestation_channel, escalation_policy, documented_outcome, audit_reference.
`mobility_economic_observation`: reuse Dataset 12 trip/offer/settlement schema and its consent controls; link only via governed aggregate zone and time keys.

### Machine learning design and safeguards
**Phase 0: Deterministic baseline.** Validate schemas, dates, rule applicability, duplicate sources and contradiction flags. Produce transparent counts and source-weighted *coverage indicators*, not a synthetic institutional legitimacy score.

**Phase 1: Human coded research corpus.** Double-code sampled public perception evidence for target, stance, uncertainty, actor type and policy context. Document inter-rater agreement and disagreement adjudication. No unreviewed LLM sentiment outputs as ground truth.

**Phase 2: Bounded model evaluation.** Compare interpretable classifiers with an LLM-assisted annotation candidate using held-out geography, time and source splits. Report precision/recall, subgroup error, calibration, abstention, drift and label uncertainty. Model outputs are analytical classifications, not judgments of a person's legitimacy or trustworthiness.

**Phase 3: Institutional comparison.** Use preregistered descriptive panels and quasi-experimental designs only if sampling and pretrend checks permit. Model the relationship between deployment rules, driver economic outcomes, public perceptions and incident reporting. Publish negative and null results.

**Human oversight:** No automated regulatory decisions, driver ranking, worker targeting, persuasive personalization, platform dispatch access or production policy enforcement. Review source licensing, consent, protected characteristics, privacy, aggregation thresholds, access control and deletion obligations before any ingestion. Protect precise mobility traces and identifying social media data.

**Acceptance gates:** (A) all source claims trace to a timestamped primary artifact; (B) rule dates and jurisdiction validated; (C) no mixing of survey and self-selected social posts as equivalent samples; (D) model performance and error reviewed by humans; (E) independent reproduction on authorized deidentified data; (F) no dashboard or external deployment until separately approved.

**Research interpretation:** Institutional permission, perceived legitimacy and operational safety are distinct constructs. A lawful deployment may be unpopular; a popular service may lack adequate independent verification. The objective is to test their relationships, not presume alignment or a predetermined conclusion.
