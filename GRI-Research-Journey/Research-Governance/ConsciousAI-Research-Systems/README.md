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
The local research service does not audit corporate systems. A separate GitHub Actions workflow is configured to collect Federal Register metadata on a schedule, but successful executions and ongoing operation have not been independently confirmed. Production deployment would require authentication, authorization, privacy controls, monitoring and maintenance ownership.

## Local executable reference service
The [Python research service](server.py) provides read only `GET /cases`, `GET /cases/{caseId}`, `GET /graph`, `GET /policies`, and a stateless `POST /assessments` evidence completeness endpoint. See [running instructions](RUNNING.md), [automated tests](test_server.py), [graph edges](graph.json) and [policy seed registry](policies.json).

**Implementation status:** Local executable reference implementation, not hosted or deployed. The graph API returns JSON nodes and edges and the local browser dashboard renders them visually. The verified policy registry is empty; the separate scheduled U.S. Federal Register collector writes unreviewed candidates rather than confirmed laws.

## Global intelligence interface and event research

The [interactive research graph dashboard](dashboard.html) is served locally at `http://127.0.0.1:8000/dashboard` by [server.py](server.py). It visualizes the checked in evidence nodes and relationships, with filters and source status inspection. The [event registry](events.json) is ready for user selected event dossiers. The [official source candidate registry](policy_sources.json) and [policy ingestion and verification protocol](POLICY-INGESTION.md) cover EU, ASEAN and U.S. starting points. **This is a local interface, not a hosted live feed or a verified automated global tracker.**

## Scheduled official policy intake
[GitHub Actions policy monitor](../../../.github/workflows/gri-policy-monitor.yml) is configured to request a run every three hours and supports manual dispatch. It runs the Python test suite and collects official U.S. Federal Register search metadata into [policy_candidates.json](policy_candidates.json) as an **unreviewed queue**, preserving first-seen timestamps and review status. The [collector](ingest_federal_register.py) is the first implemented official feed. GitHub Actions schedules can be delayed, disabled, or fail; **successful ongoing execution is not yet confirmed**. EU, ASEAN and other jurisdictions remain source candidates and are not yet automated.

This is near-real-time periodic polling, not instantaneous event streaming. It cannot infer regulatory significance or validate claims without human source review. The interactive dashboard remains local and is not publicly hosted.

## Global economic and institutional intelligence

The [Nelson model institutional economics framework](ECONOMIC-INTELLIGENCE.md) and [economic data source registry](economic_sources.json) extend the policy and event layers to macroeconomic conditions, labor markets, trade, infrastructure, institutional risk and managerial adaptation. Candidate feeds are not yet ingested or presented as real-time economic measurements.

## Hosted deployment

The dedicated [GRI Global Intelligence dashboard](https://gri-global-intelligence.onrender.com/dashboard) has been configured on Render as the `gri-global-intelligence` service, connected to this repository's `main` branch with automatic deployment enabled. [Render service status](https://dashboard.render.com/web/srv-dbb9i2jncjis7391jedg). The initial build was in progress at creation on October 19, 2026; the public URL is not proof of successful runtime operation. This separate service does not replace existing ConsciousAI deployments. The current dashboard reads checked in research and event data; international and economic feeds are not yet continuously ingested.
