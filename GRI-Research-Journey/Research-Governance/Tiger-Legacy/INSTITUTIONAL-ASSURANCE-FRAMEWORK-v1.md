# GRI Institutional Assurance Framework (IAF) v1.0 — Research Design

**Status:** Research protocol / proposed controls; not an implemented certification or externally validated result.  
**Program:** Training a Tiger → Tiger Assurance → Tiger Legacy V1.1.  
**Scope:** Synthetic data only; no client-specific artifacts, credentials, proprietary material, commercial intentions, or production authorization.  
**Institutional independence:** GRI-authored interpretation; faculty and Thunderbird are not sponsors, endorsers, or certifiers.

## Research question

Can technical evidence of AI-system compliance be reconciled with institutional legitimacy, meaningful human oversight, and contestable decisions, including when individually compliant agents interact?

**Hypothesis H1:** A technically valid authorization or evidence record does not by itself establish institutional legitimacy.  
**H2:** Enforced revocation, contestability, independent replay, and escalation reduce unremediated governance failures relative to a technical-only baseline.  
**H3:** Adaptive ML/RL behavior can create new governance failures even when initial permission checks pass.

## Academic provenance and interpretive boundaries

The following are **GRI operationalizations**, not claims that faculty designed or approved Tiger Legacy. Validate precise course readings, quotations, and attributions against primary materials before scholarly publication.

- **Roy C. Nelson — institutional political economy:** Apply liberalism (including embedded vs extreme forms), economic nationalism, and structuralism as *competing explanatory lenses*; examine institutions, incentives, bargaining power, distributional effects, and the state–market relationship. These are analytical lenses, not cybersecurity standards.
- **Robert A. Packenham — comparative political development:** Test the gap between formal reform design and institutional capacity, context, and political implementation. Packenham's 1964 *Approaches to the Study of Political Development* offers a taxonomy of approaches, not a ready-made AI security algorithm. Source: https://www.cambridge.org/core/journals/world-politics/article/abs/approaches-to-the-study-of-political-development/D90AAF6119D3B25F6F9F33AB99D12AC1
- **David Slocum — leadership:** Candidate applications: accountable escalation, adaptation, and organizational learning. **Source-to-concept attribution pending review of exact course materials.**
- **Lena Booth — decision and financial risk:** Candidate applications: sensitivity testing, resource trade-offs, failure costs, and continuity. **Source-to-concept attribution pending review.**
- **Landry Signé — AI divide, institutional capacity, and agent governance:** Signé and Karla Yee Amezaga's [Brookings article on AI agent governance](https://www.brookings.edu/articles/shaping-global-governance-of-ai-agents/) provides a scholarly reference for scoped authorization, runtime oversight, traceability, and institutional capacity. GRI independently maps these themes to proposed IAF-01, IAF-03, IAF-06, IAF-08, IAF-09, and IAF-10 tests. This is not an implemented or validated control. See the [source reviewed GRI crosswalk](../Institutional-Source-Registry/LANDRY_SIGNE_PUBLIC_RESEARCH.md).
- **Doug Guthrie — organizational/institutional governance:** Candidate applications: organizational incentives and governance implementation. **Specific source and attribution pending verification.**
- **Mansour Javidan / GLOBE (optional, scoped):** Apply only when testing cross-cultural organizational expectations, not as a substitute for Nelson's institutional model; distinguish societal practices from values and avoid cultural determinism.

## Traceability matrix — hypotheses and proposed tests

| ID | Lens | Operational control (proposed) | Synthetic test | Metric | Evidence |
|---|---|---|---|---|---|
| IAF-01 | Nelson: institutional authority | Actor/role/mandate and jurisdiction registry; deny absent mandate | Agent has technically valid token but no institutional mandate | Unauthorized approvals / total unauthorized attempts | Decision log, policy version, mandate map |
| IAF-02 | Nelson: distributional incentives | Multi-actor conflict-of-interest escalation | Two legitimate authorities issue contradictory orders | Conflict detection recall, unresolved conflicts | Conflict graph, escalation record |
| IAF-03 | Packenham: implementation capacity | Institutional feasibility checklist and fallback owner | Formally approved policy lacks capable operator | Unowned controls, time to escalation | Capability inventory, handoff log |
| IAF-04 | Slocum candidate: adaptive leadership | Human appeal and override path | Agent output contested by affected person | Appeal availability, resolution time | Appeal ledger, reviewer action |
| IAF-05 | Booth candidate: financial risk | Failure-impact and recovery-cost model | Simulated outage or integrity compromise | Recovery time, estimated impact sensitivity | Assumption register, scenario results |
| IAF-06 | Signé scholarship / GRI interpretation: equitable access | Alternative review channel and disparate-impact monitoring | Synthetic low-access cohort cannot use default appeal | Appeal completion gap by cohort | Cohort definitions, privacy-preserving aggregate |
| IAF-07 | Guthrie candidate: organizational accountability | Named control owner and separation of duties | Same actor requests and approves exception | Separation-of-duties violation rate | Role matrix, signed decision |
| IAF-08 | Tiger Assurance: evidence integrity | Canonical event digest, chained evidence and replay | Tamper with event, reorder chain, replay revoked event | Detection recall and false-positive rate | Canonical input, hash, replay output |
| IAF-09 | Tiger Legacy: consent | Purpose-bound authorization, revocation and expiry | Consent withdrawn during queued execution | Post-revocation action count | Consent event and decision trace |
| IAF-10 | ML/RL governance | Re-evaluate policy on state/action change | Simulated adaptive agent discovers new path to goal | Constraint-violation rate; intervention latency | Policy snapshot, agent trajectory |

## Experiment protocol

1. **Freeze baseline:** record repository commit, test environment, policies, deterministic seeds, synthetic fixtures, and expected results.
2. **Technical-only comparator:** run scenarios with basic token validity and integrity checks but without institutional controls.
3. **Institutional assurance condition:** repeat the same fixtures with authority mapping, escalation, revocation, appeals, and replay verification enabled.
4. **Adversarial cases:** expired/revoked consent, valid credential without mandate, conflicting authority, privileged operator collusion, altered evidence, recovery after partial outage, and adaptive-agent policy circumvention.
5. **Measure:** true/false positives, false approvals, post-revocation executions, replay integrity, detection latency, appeal resolution, coverage, and performance overhead. Report denominators, uncertainty and failure cases.
6. **Reproduce independently:** fresh environment, documented dependencies, fixed inputs, verification script, hashes, and independent reviewer checklist. Do not label independent audit until independently performed.
7. **Release gate:** no client data; no credentials; no operational controls; privacy review; regression tests; human signoff before production integration.

## Planned deliverables and acceptance criteria

- [x] Research protocol and initial concept-to-control traceability matrix (this document).
- [ ] Source register: verified course readings, page references, attribution boundaries, and bibliography for each faculty-related claim.
- [ ] Machine-readable matrix schema with control IDs and evidence fields.
- [ ] Synthetic fixture suite and adversarial evaluation runner with baseline vs intervention.
- [ ] Reproducible results report (sample sizes, confusion matrix, limitations).
- [ ] Independent replay protocol executed by a reviewer separate from the implementer.
- [ ] Read-only dashboard summary, only after results are verified and separately approved for release.
- [ ] All repository quality, rights/security and research-system workflows green.

**Interpretation:** A green CI workflow demonstrates tests passed on a particular revision; it is not proof of overall ML/RL correctness, institutional legitimacy, or external certification.

## November 2026 milestone | Assurance evidence and institutional validation crosswalk

**Milestone classification:** Documentation and evaluation design only. This extends the existing Institutional Assurance Framework, Tiger Assurance and [Integrated Research Journey](../../Integrated-Research-Journey/README.md#november-2026--institutional-assurance-under-accelerating-ai-change). It is not a new research program, implemented control, independent certification, completed validation or production permission.

### Research contribution and falsifiable claims

**Question:** Under which conditions does technical evidence support institutionally legitimate and durable assurance as AI models and delegated authority change? Nelson's institutional political economy is the principal lens for incentives and decision power; Packenham's legal formal, economic, administrative, social system and political culture approaches classify institutional capacity. GLOBE provides carefully bounded cross-cultural leadership questions; Moore's Law is a historical analogy for technological acceleration, not a measured AI performance law. The NIST AI RMF and Generative AI Profile supply recognized risk management terminology. These sources inform GRI's independent operationalization and do not endorse it.

| Institutional claim | Scholarly or governance lens | Required evidence and proposed assessment | Inconclusive or failure signal |
| --- | --- | --- | --- |
| Independent review can challenge a developer's safety claim | Nelson: bargaining power and institutional incentives; NIST Govern | Reviewer appointment and removal terms, conflict disclosures, audit access, publication rights, documented dissent | Sponsor may suppress adverse findings or review access is insufficient |
| Technical validity does not establish legitimate delegated authority | Packenham: legal formal and administrative capacity; existing GRI AI Paradox | Synthetic authority chain, consent scope, revocation and contestable human override, plus named accountable decision owner | Valid technical record with no authorized remedy or appeal |
| Assurance conclusions survive relevant system change only when re-evaluated | NIST Measure and Manage; bounded technological acceleration hypothesis | Version identifiers, configuration and change log, materiality trigger, dated retest and residual risk record | Prior result applied to materially changed system without reassessment |
| Audit evidence can be independently reproduced within its stated scope | NIST Govern and Measure; Tiger Assurance evidence provenance | Reproducible synthetic inputs, method version, expected outputs, reviewer replay and discrepancy log | Independent reviewer cannot reproduce a claimed outcome |
| International standards do not systematically exclude affected institutions | Signé: global AI divide; GLOBE: cross-cultural institutional differences | Participation rules, language and regional coverage, infrastructure assumptions, access costs and appeals | Material coverage gaps unacknowledged; no evidence of meaningful participation |
| Industry and public funding can both create distinct independence risks | Comparative tobacco research governance and vehicle safety institutions | Funding and appointment disclosure, conflict controls, adverse-result publication and corrective authority | Funding source treated as proof of independence or misconduct without evidence |

### Historical and repository traceability

- **Institutional lineage:** [2015 SpaceX/DeepMind governance discussions through 2026 frontier AI standards proposals](../../Integrated-Research-Journey/README.md#november-2026--frontier-ai-external-assurance-and-institutional-accountability). Treat overlapping participants and chronology as contextual evidence, not proof of a continuous organization.
- **Existing synthetic implementation:** [Tiger Legacy research record](README.md) describes authorization, revocation, integrity checks and CI evidence. Verify the current commit and test run before repeating any numeric pass counts; those tests do not establish frontier model safety.
- **Existing institutional foundations:** [Nelson methodological boundaries](../../Integrated-Research-Journey/nelson-model-methodological-boundaries.md) and [institutional AI governance research](../../institutional-ai-governance-assurance/README.md) provide source and interpretive constraints.
- **Established external references:** [NIST AI RMF](https://www.nist.gov/itl/ai-risk-management-framework), [NIST Generative AI Profile](https://www.nist.gov/publications/artificial-intelligence-risk-management-framework-generative-artificial-intelligence), [WHO FCTC Article 5.3 guidelines](https://fctc.who.int/publications/m/item/guidelines-for-implementation-of-article-5.3), and [OpenAI's Governance of Superintelligence essay](https://openai.com/index/governance-of-superintelligence/). The tobacco comparison concerns institutional conflicts, not an assertion of equivalent industry conduct.

### Validation gates and milestone sequence

1. **Evidence register:** For each case, record source date, source type, exact claim, competing interpretation, provenance, model or policy version, and limitations. Status: evaluation design established; complete source-level verification remains to be done.
2. **Case comparison:** Code at least the early DeepMind governance proposal, 2023 Frontier Model Forum and reported 2026 SAFA proposal using common independence, access, authority and participation criteria. Status: proposed analysis, not a completed comparative dataset.
3. **Synthetic assurance protocol:** Map already implemented Tiger Assurance tests to the above criteria and identify missing institutional measurements. Any additional test or code change requires separate review and authorization. Status: proposed mapping, not new test execution.
4. **Independent academic and technical scrutiny:** Seek confidential methodological review, reproduce an exact commit and CI run, document dissent and revisions. Status: future validation gate; no reviewer endorsement claimed.
5. **Public research release:** Publish only source-verifiable findings, clear negative results and aggregate synthetic evidence after authorized review. Never disclose confidential clients, proprietary assurance methods, credentials or restricted audit materials.

**Milestone acceptance:** A traceable crosswalk and validation protocol are documented here. Completion of evidence collection, case coding, additional tests and external review must be separately recorded with dates and verifiable artifacts. Do not promote planned activities to completed results.
