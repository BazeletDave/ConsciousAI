# GRI Intelligence Engine 2.0 | Engineering Milestone

Status: proposed research engineering milestone; not production validated.
Owner: Grand Research Institute.
Scope: additive development; preserve existing dashboard, scheduled ingestion, and Render deployments.

## Scientific objective
Test whether a provenance-aware intelligence pipeline can improve evidence classification, detect distribution drift, and produce reproducible, governed recommendations without conferring autonomous decision authority.

## Workstreams
1. Evidence pipeline: immutable source identifiers, capture timestamps, jurisdiction, claim-to-source links, evidence status, deduplication, human verification queue.
2. ML evaluation: versioned datasets, train/validation/test separation, time-based holdouts, baseline comparisons, calibration, subgroup evaluation where justified, drift alerts, abstention on low confidence.
3. Institutional knowledge graph: typed edges for observed versus inferred relationships, provenance on every edge, source conflict handling, graph versioning.
4. Agent control plane: explicit capability scopes, least privilege, approval gates, deterministic policy enforcement, replayable audit events, rollback.
5. Research reproducibility: experiment manifests, deterministic seeds, dependency locks, test fixtures, CI quality gates, documented limitations.
6. Dashboard observability: display source freshness, collector success, model version, last validated experiment, alerts and verification status. Never label a scheduled job successful without run evidence.

## Acceptance criteria
- Existing dashboard and collector behavior remain unchanged until separately reviewed.
- Tests pass on isolated fixtures and CI; no secrets or personal data in fixtures.
- Every inference is linked to source evidence and a model/version identifier.
- Evaluation reports compare against a documented baseline; no unsupported accuracy claims.
- Drift alerts do not automatically retrain or deploy a model.
- High-impact decisions require authorized human approval; denied actions leave auditable records.
- Rollback and recovery are demonstrated in a staging environment.
- Security, privacy, licensing and academic integrity review precede any public promotion.

## Proposed implementation sequence
Phase A: inventory architecture, CI, data sources, and existing tests.
Phase B: evidence schema and offline benchmark harness.
Phase C: model registry, drift detection, calibration, and governance gates.
Phase D: staged dashboard integration and independent review.

## Research integrity
Distinguish conceptual models, synthetic experiments, observed measurements, and externally validated results. This roadmap does not assert that continuous model learning or operational governance controls are currently validated.
