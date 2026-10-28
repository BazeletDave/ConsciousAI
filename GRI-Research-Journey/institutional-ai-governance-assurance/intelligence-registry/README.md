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

## Scheduled collection and dashboard integration

[GitHub Actions workflow](https://github.com/BazeletDave/ConsciousAI/blob/main/.github/workflows/gri-governance-intelligence.yml) is configured for six-hour polling plus manual dispatch. It runs unit tests, requests public metadata for three allowlisted GitHub repositories, and commits the [persistent evidence ledger](evidence_ledger.json) with unreviewed status. The [collector](collect.py) and [tests](test_collect.py) are version controlled. GitHub scheduling and successful execution have **not** yet been verified.

The existing GRI research server now defines a read-only `GET /intelligence/governance-registry` route that returns the checked-in ledger's public metadata. This is an interface integration, **not** a claim that Render has deployed or validated it. The ledger begins empty until a successful collection run. The [dashboard adapter](dashboard_adapter.py) is a separate local reference implementation.

**Operational limitation:** GitHub Actions writes may trigger automatic deployment if the linked Render service deploys from `main`. No direct Render deployment or configuration change was initiated. Verify CI permissions, runtime tests, deployment status, and endpoint response before describing the feed as operational.

## Global enrollment and identity fraud research stream

The [Synthetic Student Paradox](../../../research/case-studies/synthetic-student-paradox-2026.md) now links to a [global comparative research protocol](../../../research/case-studies/global-enrollment-identity-fraud-research-stream.md). It defines an incident and claim evidence model, mapping to this registry, proposed dashboard views, and evaluated document intelligence tasks. The classroom account remains attributed and independently unverified; no individual student data or fraud labels are introduced. This documentation link does not add a collector, dashboard display, or trained model.
