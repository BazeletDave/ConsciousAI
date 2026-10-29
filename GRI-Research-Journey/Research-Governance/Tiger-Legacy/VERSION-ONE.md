# GRI Tiger Legacy | Version One

**Grand Research Institute | Independent cybersecurity and AI assurance research**  
**Status:** Engineering baseline and synthetic prototype authorized; no production integration or client testing authorized.  
**Initiated:** 29 October 2026

## Mission

Develop a reusable, client independent security and assurance research prototype that evaluates authorization, consent, evidence integrity, recovery, and accountable human control. Family Legacy is not a component of the product or its identity. No client specific information, audit contents, or customer data belong in this public prototype.

## Verified baseline

The existing Tiger Legacy research charter lists candidate reusable components: Training a Tiger assurance experiments, Agentic Authorization Prototype, Agentic Governance Engine, PHP2Shell research, and ConsciousAI assurance/dashboard. These are **candidates**, not proven interoperable modules. Training a Tiger's documented synthetic results demonstrate why local validation is not equivalent to task success. Source inspection, dependency review, and tests are required before any reuse claim.

## Version One architecture and contracts

1. **Tenant boundary:** Every request, evidence record, consent grant, and audit query must carry a validated tenant context; deny absent, inconsistent, or cross tenant identifiers.
2. **Identity and authorization:** Default deny. Evaluate authenticated principal, resource ownership, scoped permission, expiry, and explicit human approval for consequential actions.
3. **Consent:** Record purpose, subject, resource, grantor authority, time, expiry, and revocation. Revocation must affect subsequent access checks; preserve non sensitive audit evidence.
4. **Evidence integrity:** Canonical event representation, digest and signed provenance with independently verifiable keys; verify chain continuity and detect alteration or replay.
5. **Sensitive data minimization:** Use generated synthetic records and media only. No live credentials, private recordings, audit details, or raw sensitive customer information in source control or the public dashboard.
6. **Assurance reporting:** Show tests, failures, scope, evidence provenance, and explicit unmeasured states. Never represent simulated results as operational security.
7. **Recovery:** Test restoration, integrity, and authorization after recovery; document limitations. No autonomous production remediation.

## Acceptance tests before a prototype demonstration

- Tenant A cannot read, mutate, or enumerate Tenant B records, media, grants, or audit entries.
- Unauthenticated access and unowned media access are rejected.
- Expired or revoked consent is denied and an auditable decision is produced.
- Tampering, missing events, and replayed evidence are detected.
- Authorized access succeeds under declared scope; negative tests do not depend on knowing secret test fixtures.
- Recovery from a controlled synthetic failure preserves expected data and evidence integrity.
- Tests run reproducibly in CI; dashboard reports come from actual test artifacts rather than invented scores.

## Development sequence

**Gate A — Inventory:** Inspect candidate code, interfaces, dependencies, tests, threat boundaries, and dashboard endpoints.  
**Gate B — Core:** Implement isolated synthetic tenant fixtures, deny by default authorization, and consent ledger.  
**Gate C — Assurance:** Implement cryptographic provenance and tamper/replay verification.  
**Gate D — Reporting:** Publish aggregate, synthetic only evidence through a read only research dashboard interface.  
**Gate E — Review:** Run regression and adversarial test cases; obtain independent review before claiming production readiness.

Target a substantial prototype by 31 December 2026; this is a planning target, not a guaranteed delivery or certification.

## Integration boundary

A future client implementation requires written authorization, architecture review, data processing terms, source remediation ownership, security testing, and separate production credentials and infrastructure. A security layer cannot by itself remediate unsafe application endpoints, leaked credentials, unsupported dependencies, or defective access checks. Client data must remain under client control and outside GRI's public research datasets.

## Change management

This file establishes Version One development scope. Existing historical research experiments remain unchanged. No live scanning, client access, production deployment, or security certification is implied.
