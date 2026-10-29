# Institutional Source Registry | GRI Global Governance Intelligence

**Grand Research Institute · 26 October 2026 · Research source registry v0.1**

This is an inspectable, public-source registry intended to support the [GRI governance dashboard](https://gri-global-intelligence.onrender.com/dashboard) and the [continuous research intake protocol](../ConsciousAI-Research-Systems/CONTINUOUS_RESEARCH_INTAKE.md). **A GitHub source registry is not proof of ingestion by the running dashboard**. No scheduler, database, model or production integration is changed by this release.

## Primary institutional anchors

| Institution | Research use | Boundary |
| --- | --- | --- |
| [European Commission AI Office](https://digital-strategy.ec.europa.eu/en/policies/ai-act-governance-and-enforcement) | AI Act governance, enforcement and institutional oversight | Separate binding law from guidance and phased implementation |
| [EU AI Act framework](https://digital-strategy.ec.europa.eu/en/policies/regulatory-framework-ai) | Statutory obligations, categories and applicability dates | Confirm current legal status for each obligation before asserting compliance |
| [Council of Europe AI Framework Convention](https://www.coe.int/en/web/artificial-intelligence/the-framework-convention-on-artificial-intelligence) | Human rights, democracy, contestability, remedies | Do not assume all signatories have ratified or are bound identically |
| [OECD AI Policy Observatory](https://oecd.ai/en/ai-principles) | Intergovernmental principles, comparative AI policy | OECD recommendations are not national law |
| [OECD semiconductor value chain](https://www.oecd.org/en/publications/mapping-the-semiconductor-value-chain_4154cdbf-en.html) | Infrastructure concentration, global trade and dependencies | Not evidence of electoral or hiring effects |
| [NIST AI RMF](https://www.nist.gov/itl/ai-risk-management-framework) | Risk mapping, measurement and governance | Voluntary framework unless incorporated by other authority |
| [US Treasury AI](https://home.treasury.gov/policy-issues/financial-markets-financial-institutions-and-fiscal-service/treasury-and-artificial-intelligence) | Agency AI use-case governance and disclosures | Does not independently establish AI-based applicant screening |

**[Machine-readable source registry (CSV)](institutional_sources_2026-10-26.csv)**

## Intake adapter contract (proposed, not deployed)

`source_id, institution, jurisdiction, source_class, topic, source_url, claim_scope, reviewed_date, status`

The dashboard integration should consume only allowlisted institutional domains, record retrieval timestamps and content digests, distinguish **source discovered** from **claim verified**, preserve version history, and expose source failures as degraded—not successful—refreshes. External agency feeds or APIs should be used only if terms and licenses permit. No live ingestion or source freshness claim is made here.

## Research integration and quality gates

1. **Source identity:** canonical institutional URL, issuing body, jurisdiction, publication date and legal force.
2. **Evidence maturity:** primary source, independent academic evaluation, interpretive commentary or GRI hypothesis.
3. **Comparative mapping:** politics, hiring, education, public administration, platform work, cybersecurity, chips and global trade.
4. **Human verification:** documented reviewer and disposition before claims enter validated research summaries.
5. **Governance constraints:** public information only; source licensing, privacy, academic integrity and reproducibility preserved.
6. **Production gate:** run offline schema/link checks, then integration tests and an explicit release review before changing Render or the three-hour collector.

**Ambiguity control:** 'ACN' was not identified with confidence as a specific regulator. It is not represented as a verified institutional source pending clarification.

## Links to GRI research

- [Algorithmic politics evidence review](../../Integrated-Research-Journey/2026-10-26-algorithmic-politics-decade-evidence-review.md)
- [Cross-sector institutional research atlas](../../Integrated-Research-Journey/2026-10-26-cross-sector-algorithmic-authority-institutions.md)
- [Reproducible evidence baseline](../../Integrated-Research-Journey/2026-10-26-evidence-maturity-baseline.md)
- [Academic integrity and AI-assisted learning](../Academic-Integrity/README.md)

The GRI dashboard remains an independent research system. Listing an institution does not indicate partnership, endorsement, direct access or regulatory authority.

## Landry Signé public scholarship

[Landry Signé public research register](LANDRY_SIGNE_PUBLIC_RESEARCH.md) indexes publicly identifiable publications and proposes a rights-aware, human-reviewed pathway to GRI institutional governance research, AI agent analysis and future ML evaluation. This is an indexed research candidate, not evidence of a live dashboard feed or trained model. Retain the spelling **Landry Signé** and preserve attribution and endorsement boundaries.
