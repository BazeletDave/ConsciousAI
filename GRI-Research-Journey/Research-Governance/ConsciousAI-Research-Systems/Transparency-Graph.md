# Transparency Graph | Research specification

**Status:** Data model and initial machine readable evidence registry, not an operational enterprise graph.

## Purpose
Represent the path from organizational objectives through engineered systems and automated decisions to observed outcomes, human consequences and correction. Explicit provenance and uncertainty are mandatory.

## Node types
`organization`, `technical_system`, `engineering_publication`, `decision`, `observation`, `actor_role`, `policy`, `research_hypothesis`, `source`.

## Edge types
`describes`, `observed_in`, `governed_by`, `authorized_by`, `affects`, `derived_from`, `compared_with`, `challenges`, `requires_verification`.

Every edge must have an `evidence_status`. A `compared_with` edge denotes an analytical comparison, **not** a technical integration or causal relationship.

## Initial graph examples
- Uber Software Factory — `described_by` → supplied Uber engineering article.
- Uber MCP Gateway — `compared_with` → Lyft Chicago case, **analytical comparison only**.
- Lyft Chicago case — `requires_verification` → final payout and platform fee records.
- GRI AI Compliance Paradox — `tested_against` → operational accountability and correction indicators.

## Evidence design
Each record includes an ID, claim, organization, date context, source pointer, classification (`observation`, `company_report`, `hypothesis`), verification status, and limitations. See [cases.json](cases.json) and [evidence.schema.json](evidence.schema.json).

Future capabilities: temporal versioning, provenance queries, privacy aware access, visual graph exploration, role based corrections and institutional audit trails. None is represented as currently running.
