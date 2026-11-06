# ConsciousAI | Research Systems Architecture

**Grand Research Institute (GRI)** · Founder and research author: David A. Grand  
**Status:** Public research dashboard deployed on Render; associated assurance, ML evaluation, and policy-intake components remain at differing research and validation stages. Not a certified production audit service or legal monitoring authority.

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

**Implementation status:** Executable research implementation, with its read-only dashboard and API hosted on Render. The graph API returns JSON nodes and edges and the local browser dashboard renders them visually. The verified policy registry is empty; the separate scheduled U.S. Federal Register collector writes unreviewed candidates rather than confirmed laws.

## Global intelligence interface and event research

The [interactive research graph dashboard](dashboard.html) is served locally at `http://127.0.0.1:8000/dashboard` by [server.py](server.py). It visualizes the checked in evidence nodes and relationships, with filters and source status inspection. The [event registry](events.json) is ready for user selected event dossiers. The [official source candidate registry](policy_sources.json) and [policy ingestion and verification protocol](POLICY-INGESTION.md) cover EU, ASEAN and U.S. starting points. **The interface is publicly hosted on Render. It is not a verified real-time global tracker; source ingestion and human verification are separate processes.**

## Scheduled official policy intake
[GitHub Actions policy monitor](../../../.github/workflows/gri-policy-monitor.yml) is configured to request a run every three hours and supports manual dispatch. It runs the Python test suite and collects official U.S. Federal Register search metadata into [policy_candidates.json](policy_candidates.json) as an **unreviewed queue**, preserving first-seen timestamps and review status. The [collector](ingest_federal_register.py) is the first implemented official feed. GitHub Actions schedules can be delayed, disabled, or fail; **successful ongoing execution is not yet confirmed**. EU, ASEAN and other jurisdictions remain source candidates and are not yet automated.

This is near-real-time periodic polling, not instantaneous event streaming. It cannot infer regulatory significance or validate claims without human source review. The dashboard is publicly hosted; the scheduled collector's execution history must be checked separately.

## Global economic and institutional intelligence

The [Nelson model institutional economics framework](ECONOMIC-INTELLIGENCE.md) and [economic data source registry](economic_sources.json) extend the policy and event layers to macroeconomic conditions, labor markets, trade, infrastructure, institutional risk and managerial adaptation. Candidate feeds are not yet ingested or presented as real-time economic measurements.

## Hosted deployment

The dedicated [GRI Global Intelligence dashboard](https://gri-global-intelligence.onrender.com/dashboard) has been configured on Render as the `gri-global-intelligence` service, connected to this repository's `main` branch with automatic deployment enabled. [Render service status](https://dashboard.render.com/web/srv-dbb9i2jncjis7391jedg). Render reported a live deployment on October 25, 2026. Deployment status does not establish the accuracy of research claims, model performance, or external certification. This separate service does not replace existing ConsciousAI deployments. The current dashboard reads checked in research and event data; international and economic feeds are not yet continuously ingested.


## Academic integrity and independent research publication controls

**Institutional alignment reviewed November 6, 2026.** GRI is an independent research organization. David Grand's Thunderbird/ASU educational experience and cited faculty scholarship may inform GRI's analysis, but neither coursework nor academic affiliation establishes university sponsorship, faculty review, validation, coauthorship or endorsement.

For public ConsciousAI research, apply these publication controls:

1. **Source attribution and originality:** Cite original scholarly and primary sources with enough bibliographic detail to verify the proposition. Distinguish a scholar's actual argument from GRI's independent application to AI. Do not reproduce copyrighted or course-licensed readings, lecture slides, recordings, handouts, assignments or assessments without appropriate written authorization.
2. **Evidence classification:** Label observations, illustrative anecdotes, secondary reports, conceptual interpretations, testable hypotheses, synthetic tests, verified results and independently reproduced findings separately. No conceptual analogy or successful deployment check is an empirical validation.
3. **Academic work and AI assistance:** Keep private course submissions, student or classmate information and restricted course materials outside public research archives. For any academic submission, follow the applicable instructor's syllabus and ASU academic integrity rules, including authorization and disclosure requirements for AI tools; repository publication does not substitute for course permission.
4. **Research traceability:** Record dates, original sources, methodology, version history, limitations, rival explanations, review status and correction paths. Verify time-sensitive legal, policy, economic and environmental claims against dated authoritative records before asserting them as facts.
5. **Institutional and technical assurance:** Distinguish code checks, service deployment, independent reproduction, security assurance and scientific validation. Preserve frozen assurance baselines and restricted evidence; never describe a prototype or unreviewed candidate feed as a certified audit or verified live intelligence system.

**Authoritative policy references:** [Thunderbird policies and resources](https://thunderbird.asu.edu/policies-and-resources), [ASU Student Academic Integrity Policy](https://provost.asu.edu/academic-integrity/policy), [ASU Graduate College academic integrity](https://graduate.asu.edu/current-students/policies-forms-and-deadlines/academic-integrity), and [Thunderbird academic catalog policies](https://catalog.asu.edu/policies/global-management). These are institutional policy references, not evidence of institutional endorsement. Individual course syllabi and applicable permissions govern course-specific requirements.

**Review scope:** This is a standing publication control, not a representation that every historical repository file has been individually audited for licensing, factual accuracy, sensitive information, or methodological completeness.
