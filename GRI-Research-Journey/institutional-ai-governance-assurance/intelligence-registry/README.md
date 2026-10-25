# GRI Governance Intelligence Registry | Offline Reference Prototype

**Status:** Research prototype; no live feeds, production monitoring, or dashboard deployment. Standard-library Python 3.9+.

This registry turns public-source research leads into machine-readable, reviewable records without equating an allegation, an AI-generated inference, or a synthetic demonstration with a verified fact.

## Run

```bash
python GRI-Research-Journey/institutional-ai-governance-assurance/intelligence-registry/registry.py
python -m unittest discover -s GRI-Research-Journey/institutional-ai-governance-assurance/intelligence-registry -p 'test_*.py' -v
```

The script reads adjacent `signals.json`, validates records, and prints a summary. No network calls, automated enforcement, external system access, or writes occur.

## Integration contract

Future dashboard ingestion can consume validated JSON records containing `id`, `title`, `domain`, `source_url`, `source_type`, `verification`, `governance_risk`, `safeguard`, `opportunity`, `review_status`, and `last_reviewed`. The dashboard must display verification and review states, not merely a risk score. Publication, notification, automated actions, and model updates require separate authorization and security review.

## Source boundaries

Uber's Persona Guardrail and ADR are external engineering references, not GRI-controlled services. Waymax is an externally maintained research simulator and is **not** a real-world autonomous-vehicle safety certification; its license is non-commercial and must be reviewed before any use or redistribution. The enrollment-fraud discussion is an unverified classroom lead, not an allegation against identified students.

Related research: [comparative architecture](../research-program-architecture.md) and [methods protocol](../evidence-and-methods-protocol.md).
