# Event provenance and governance decision contract | Version One

**Scope:** Public, synthetic-only research interface extending the existing Executable Governance package. This is a schema specification, not a deployed service, independent audit, cryptographic signature, or assurance certification. No client data or confidential implementation details.

## Contracts

- [Existing event input schema](event.schema.json): event_id, moving, handling_detected, driver_attribution_verified, confidence and synthetic source_type. Retained unchanged for compatibility.
- [Versioned decision record JSON Schema](governance-decision.schema.json): links a source event to a policy version, authorization basis, decision outcome, evidence classification and provenance.
- Record time uses RFC 3339 date-time; all hashes are lowercase SHA-256 hexadecimal.
- artifact_sha256 identifies the exact source artifact bytes, not necessarily the JSON decision record. The producer must specify the source artifact and encoding in its operational documentation.
- canonicalization=RFC8785 is a declaration only; consumers must actually implement and test RFC 8785 before claiming canonical verification. SHA-256 alone does not authenticate the author or make records immutable.
- parent_record_sha256 may link to an earlier record, but a hash chain alone does not guarantee append-only storage, trusted timestamps, or independent verification.
- Verification status must not be marked independently_reproduced without documented external reproduction evidence.
- Any substantive schema or policy revision must update the version and preserve earlier records. Breaking contract changes require a new major schema version.

## Example decision (illustrative; hashes and identifiers are placeholders)

```json
{
  "schema_version": "1.0.0",
  "decision_id": "demo-decision-a",
  "event_id": "demo-event-a",
  "recorded_at": "2026-10-31T12:00:00Z",
  "source": {"source_type": "synthetic", "system_id": "offline-reference"},
  "provenance": {
    "generator": "illustrative-example",
    "artifact_sha256": "0000000000000000000000000000000000000000000000000000000000000000",
    "canonicalization": "none",
    "verification_status": "unverified"
  },
  "policy": {"policy_id": "reference-warning-policy", "policy_version": "1.0.0", "authorization_basis": "synthetic_research_only"},
  "decision": {"outcome": "REVIEW_EVIDENCE", "reason": "Human review required before consequential action", "human_review_required": true},
  "evidence_classification": "simulation",
  "limitations": ["Illustrative record; digest is a placeholder and must not be interpreted as verified."]
}
```

## Governance rules

1. Validate the input event and decision record against their declared schemas.
2. Separate observation from attribution and authorization. Classification is not permission to intervene.
3. Record policy version and reason at decision time; never silently rewrite historical decisions.
4. Capture provenance of each source artifact and evidence limitations; redact or avoid sensitive data.
5. Require human review for uncertain or consequential actions; the reference contract permits no punitive or physical intervention.
6. Preserve correction history as additional linked records rather than overwriting prior evidence.

**Next engineering work, not claimed complete:** executable validation tests for the new schema, real canonicalization checks, signature and trust anchor design, immutable storage and independent replay verification.

**Research basis:** NIST AI RMF 1.0 (https://doi.org/10.6028/NIST.AI.100-1); JSON Schema Draft 2020-12 (https://json-schema.org/draft/2020-12/schema); RFC 8785 (https://www.rfc-editor.org/rfc/rfc8785).
