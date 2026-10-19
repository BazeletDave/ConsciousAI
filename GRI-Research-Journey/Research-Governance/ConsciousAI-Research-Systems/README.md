# ConsciousAI | Research Systems Architecture

**Grand Research Institute (GRI)** · Founder and research author: David A. Grand  
**Status:** Development specifications and reproducible reference prototype; **not deployed**, not a production audit service, and not a live legal monitoring service.

This project advances three previously proposed concepts into one integrated research architecture:

1. [Ethical Intelligence API](Ethical-Intelligence-API.md): machine readable decision accountability and review criteria.
2. [Transparency Graph](Transparency-Graph.md): provenance and relationships across organizations, technical systems, decisions, observations and governance.
3. [AI Policy Tracker](AI-Policy-Tracker.md): jurisdictional policy register with primary source verification and effective date tracking.

## Shared research foundations
- [GRI institutional leadership monograph](../../Algorithmic-Management-Institutional-Leadership/Research-Monograph-Full-Text.md)
- [Uber engineering and the AI paradox](../../Algorithmic-Management-Institutional-Leadership/Uber-Engineering-AI-Paradox-Operational-Management-2026.md)
- [Uber and Lyft longitudinal research](../../Algorithmic-Management/Uber-Lyft-Research/README.md)
- [Chicago paired Lyft transaction case](../../Algorithmic-Management/Uber-Lyft-Research/case-study-002-chicago-consecutive-lyft-rides.md)
- [Integrated Research Journey](../../Integrated-Research-Journey/README.md)

## Working reference assets
- [Machine readable case registry](cases.json)
- [JSON Schema for evidence records](evidence.schema.json)
- [API interface draft](openapi.yaml)

The initial case registry contains source described records only; it does not assert a causal link between Uber engineering and Lyft pricing. It deliberately separates observations, company reported claims, and GRI hypotheses. Records are examples for reproducible research and interface design, not independently verified audit determinations.

## Research integrity
No external systems are accessed, no corporate systems audited, and no automatic policy updates are performed by this repository. A real deployment would require authentication, authorization, privacy controls, source ingestion, review processes, and maintenance ownership.

## Local executable reference service
The [Python research service](server.py) provides read only `GET /cases`, `GET /cases/{caseId}`, `GET /graph`, `GET /policies`, and a stateless `POST /assessments` evidence completeness endpoint. See [running instructions](RUNNING.md), [automated tests](test_server.py), [graph edges](graph.json) and [policy seed registry](policies.json).

**Implementation status:** Local executable reference implementation, not hosted or deployed. The graph endpoint returns JSON nodes and edges rather than a visual UI. The policy registry is empty pending primary source verification; no real time ingestion is active.

## Global intelligence interface and event research

The [interactive research graph dashboard](dashboard.html) is served locally at `http://127.0.0.1:8000/dashboard` by [server.py](server.py). It visualizes the checked in evidence nodes and relationships, with filters and source status inspection. The [event registry](events.json) is ready for user selected event dossiers. The [official source candidate registry](policy_sources.json) and [policy ingestion and verification protocol](POLICY-INGESTION.md) cover EU, ASEAN and U.S. starting points. **This is a local interface, not a hosted live feed or a verified automated global tracker.**
