# GRI Global Intelligence 2.0 | Institutional Intelligence Architecture

Status: proposed architecture and acceptance criteria. This document does not claim capabilities that are not implemented.

## Institutional analytical model

The Nelson Model is the organizing analytical lens. For each institutional development, analysts record jurisdiction, formal and informal rules, principal actors, interests, sources of power, implementation capacity, competing interpretations, institutional legitimacy, decision options, and observed adaptation. The model is an analytical framework, not a deterministic prediction engine.

## Evidence contract

Each published intelligence record must distinguish:
- **Observed fact:** direct primary source, exact URL, issuing institution, document identifier, publication date, retrieval date, and verbatim excerpt or locator.
- **Reported claim:** attributed statement with author, publication, date, and explicit independent verification status.
- **Analytical inference:** author, method, assumptions, source dependencies, competing explanations, and limitations.
- **Hypothesis:** falsifiable proposition, test design, and no implication of empirical confirmation.
- **Forecast:** target, horizon, baseline, methodology, calibration history, and uncertainty interval.

Missing or contradictory primary evidence remains in the review queue and must not be represented as verified. A source URL alone does not constitute independent verification. Record both effective dates and publication dates when they differ. Corrections must preserve previous versions and a reasoned change log.

## Five connected workstreams

1. **Institutional intelligence:** jurisdictional events, policy intake, institutional comparison, economic context, source review.
2. **Nelson Model assessment:** actors, rules, interests, power, capacity, legitimacy, options, and adaptation, linked to evidence IDs.
3. **Algorithmic and agentic management:** delegation, operational incentives, authorization boundaries, human review, observed performance.
4. **Governance assurance:** provenance, reproducible tests, technical control evidence, risk ownership, exceptions, remediation, audit trails.
5. **Research publication:** review status, authorship, reproducibility, versioned datasets, citations, and editorial approval.

Research connections in the graph represent relationships for investigation; they are not causal findings.

## Delivery gates

**Gate A — Source integrity:** stable record identifiers; explicit evidence type; primary-source metadata; duplicate detection; reject invalid or unreviewed material from verified views.

**Gate B — Analytical discipline:** separate evidence from inference; Nelson Model fields optional until supported; no unsupported institutional scores; human approval for interpretation.

**Gate C — Operational quality:** automated schema checks, API contract tests, keyboard-accessible dashboard controls, functional route tests, no secrets in client code, observable runtime errors.

**Gate D — Controlled release:** develop on a branch; require passing CI; inspect the diff and deployment target; deploy to the existing Render service only after merging validated changes; confirm live commit, GET /health, GET /dashboard, and core data endpoints. Retain rollback capability.

## Current implementation boundaries

The existing Python standard-library server, HTML dashboard, event registry, graph, and Federal Register candidate ingestion form a useful prototype. Existing policy candidate feeds must not be described as independently verified laws. The current Render free instance may sleep after inactivity. A successful deployment or HTTP 200 response does not establish the correctness or freshness of all intelligence records.

## Reference frameworks for future mapping

Use primary institutional publications and original standards where applicable, including NIST AI RMF 1.0, NIST AI 600-1 Generative AI Profile, ISO/IEC 42001, OECD AI Principles, and official jurisdictional legal texts. Record standard versions and applicability before asserting conformity. These are reference frameworks, not claims of certification or endorsement.

## First implementation increment

Add a read-only machine-readable intelligence summary with record counts classified by their actual verification status, a clear non-certification notice, and tests for the response contract. Improve HEAD support for operational probes without changing GET semantics. Subsequent increments can add richer provenance metadata and analytical views after evidence migration and review.
