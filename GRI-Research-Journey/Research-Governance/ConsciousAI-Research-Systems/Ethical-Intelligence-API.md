# Ethical Intelligence API | Research specification

**Status:** API contract and research prototype only; not deployed.

## Objective
Evaluate whether an algorithmically mediated decision has identifiable authority, sufficient provenance, meaningful review, and documented correction pathways. The output is an evidence completeness assessment, **not** a certification that a company or decision is ethical, fair, lawful, or compliant.

## Proposed workflow
1. Register an organization, system, decision or event with source provenance.
2. Record decision owner, technical operator, authorized scope, affected stakeholders and time.
3. Attach observations and supporting or contradictory evidence with classification and verification status.
4. Check whether explanation, audit trail, human override, appeal and correction mechanisms are documented.
5. Return evidence gaps and required review actions; require human adjudication for consequential findings.

## Assessment dimensions
| Dimension | Research question | Example field |
| --- | --- | --- |
| Authority | Who authorized the action? | `decision_owner` |
| Traceability | Can an independent reviewer reconstruct it? | `evidence_ids` |
| Explanation | Can affected people understand the result? | `explanation_status` |
| Contestability | Can the result be challenged? | `appeal_status` |
| Correction | Can errors be reversed and recorded? | `correction_status` |
| Economic impact | Who receives value or bears cost? | `affected_parties` |

## Interface
See [OpenAPI contract](openapi.yaml) for proposed `GET /cases`, `GET /cases/{caseId}`, and `POST /assessments` routes. The contract is descriptive and is **not** an active HTTP endpoint.

## Case application
The Chicago Lyft paired transaction case would be marked **unresolved** pending final payout data, fee definitions, transaction IDs, demand context and a documented explanation. Uber's MCP Gateway is a separate engineering case about delegated tool access and audit controls, not a source for Lyft pricing decisions.
