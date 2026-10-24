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
