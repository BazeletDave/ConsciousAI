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

## November 2026 | Populated historical evidence register and comparative evaluation

**Assessment date:** 2 November 2026. **Method:** Desk review of publicly accessible original institutional statements, an author-published historical book excerpt, and contemporaneous reporting. **Unit of analysis:** Governance arrangement, not an individual founder or a model's technical safety. **Evidence states:** P = primary organizational disclosure; H = retrospective historical account; R = attributed news reporting; S = independent secondary research; U = unavailable or not independently verified. No confidential charter, auditor contract, internal minutes or model evidence was examined.

### Evidence register

| ID | Arrangement and date | Verifiable evidence and source class | Material limitation | State |
| --- | --- | --- | --- | --- |
| E01 | DeepMind post-acquisition ethics board; reported meeting in August 2015 at SpaceX | [New York Times historical reporting](https://www.nytimes.com/2023/12/03/technology/ai-elon-musk-larry-page.html); [Sebastian Mallaby, *Project Mario* (March 2026)](https://colossus.com/article/project-mario-demis-hassabis-deepmind-mallaby/) | Retrospective reporting and excerpt; original board charter, decision rights, funding and meeting records not examined | H |
| E02 | DeepMind/Google Project Mario negotiations, approximately 2015–2017 | [Mallaby's author-published book excerpt](https://colossus.com/article/project-mario-demis-hassabis-deepmind-mallaby/) documents proposed independent governance and unsuccessful negotiations | No executed charter or effective independent veto verified; excerpt is not a complete archival record | H |
| E03 | Frontier Model Forum launch, 26 July 2023 | [Joint founding announcement](https://openai.com/index/frontier-model-forum/) names Anthropic, Google, Microsoft and OpenAI, proposed advisory board, charter, governance and funding work | Founding aspirations do not establish independent auditor powers or enforcement | P |
| E04 | Frontier Model Forum later institutional status | [Forum's own governance and funding disclosure](https://www.frontiermodelforum.org/about-us/) states 501(c)(6), member-company operating board and membership-fee funding | Organizational disclosure does not demonstrate access to confidential model evidence, enforcement or reviewer independence | P |
| E05 | Forum's 2023 AI Safety Fund | [October 2023 joint update](https://openai.com/index/frontier-model-forum-updates/) announced a fund exceeding $10 million with philanthropic participation | A funding announcement does not establish independent governance of individual studies or audited disbursements | P |
| E06 | Proposed Standards Authority for Frontier AI, September 2026 | [The Information, 24 September 2026](https://www.theinformation.com/articles/google-openai-anthropic-ai-safety-group-takes-shape/) reports Google, OpenAI and Anthropic discussing a body for voluntary commitments, auditor qualifications and third-party evaluations | Reporting based on unnamed sources; no verified operative charter, board, auditor accreditation or binding authority | R |
| E07 | External assurance reference standard, January 2023 | [NIST AI RMF 1.0](https://www.nist.gov/publications/artificial-intelligence-risk-management-framework-ai-rmf-10) and [NIST AI RMF Core](https://airc.nist.gov/airmf-resources/airmf/5-sec-core/) identify Govern, Map, Measure and Manage, including independent review and ongoing risk management | Voluntary guidance, not evidence that any case organization implements all outcomes | P |
| E08 | Comparative public frontier safety policy review, March 2025 | [METR, *Common Elements of Frontier AI Safety Policies*](https://metr.org/assets/common-elements-mar-2025.pdf) compares developer-published safety policies | Public commitments and document coding are not independently verified effectiveness or legal enforcement | S |

### Consistent case evaluation

**Interpretation convention:** *Documented* means the cited public record directly describes the institutional feature; *proposed* means an intention without verified implementation; *not established* means the reviewed evidence does not establish it, **not** that it never existed. This is an evidence sufficiency matrix, not a numerical safety ranking.

| Criterion | 2015 DeepMind ethics board | Project Mario | Frontier Model Forum | Proposed SAFA |
| --- | --- | --- | --- | --- |
| Formal institutional structure | Historical accounts document a board meeting; operative charter **not established** (E01) | Alternative independent governance **proposed**, not adopted in reviewed account (E02) | Established 501(c)(6), member-company operating board **documented** (E03–E04) | Entity formation and charter **not established** (E06) |
| Independent appointment and removal | Independence and removal rights **not established** | Independent directors and decision rights **proposed**; not operationally verified | Operating board is composed of member representatives; separate evaluator independence **not established** (E04) | Auditor qualification role **reported as proposed**; appointment safeguards **not established** (E06) |
| Funding and conflicts | Funding and conflict policy **not established** | Corporate control was a subject of negotiation; executed safeguards **not established** | Member fees **documented**; separate AI Safety Fund announcement **documented** (E04–E05) | Funding model and conflicts safeguards **not established** (E06) |
| Independent evidence access and reproducibility | Model access and reproducible testing **not established** | Proposed authority does not demonstrate audit access | Forum aims to support evaluations; compulsory evidence access **not established** (E03–E04) | Support for third-party testing **reported as proposed**; access rights **not established** (E06) |
| Corrective authority and enforcement | Binding veto or remedies **not established** | Independent control **negotiated but not adopted** in cited history | No public regulatory enforcement mandate established by reviewed documents | No binding authority **established**; reported plan is voluntary (E06) |
| Participation and global legitimacy | Affected-party representation **not established** | External participation **proposed**, scope unverified | Public consultation and participation goals **documented**; equitable influence not demonstrated (E03) | Membership and developing-economy representation **not established** (E06) |
| Durability under system updates | Retesting and review cadence **not established** | No operational reassessment protocol established | General safety coordination documented; mandatory model-version reassessment **not established** | Reassessment requirements **not established** (E06) |

### Preliminary findings and rival explanations

**Finding F1 (supported, limited):** The reviewed arrangements differ substantially in institutional form: a historically reported ethics board, a negotiated but unadopted governance proposal, an established industry coordination nonprofit, and a reported prospective standards body. Their existence alone cannot demonstrate independent model assurance (E01–E06).

**Finding F2 (supported):** The Frontier Model Forum discloses both member-company board oversight and member-fee funding. Those facts establish structural dependence for governance and finance, but **do not prove biased decisions, compromised research or wrongdoing** (E04–E05).

**Finding F3 (evidence gap):** Across the reviewed public records, enforceable access rights, adverse-finding publication protections, independent auditor removal rules and model-version reassessment duties cannot be verified consistently. This is a finding about the **available documentation**, not proof that such mechanisms are absent.

**Finding F4 (prospective):** SAFA could add evaluator qualification and incident reporting coordination if implemented, but its eventual independence and enforcement capacity cannot be assessed as operational in November 2026 (E06).

**Rival hypotheses:** H-A, accelerating system changes outpace assurance review; H-B, weak access rights and conflicts constrain review even without rapid model change; H-C, fragmented jurisdiction and uneven public capacity limit oversight; H-D, voluntary industry coordination can nonetheless improve shared evaluation practice. None is causally resolved by this document comparison.

### GRI assurance application and next validation gates

1. **Evidence closure:** Obtain actual charters, conflict policies, evaluator contracts and version-triggered retesting rules where publicly available; preserve source dates and negative searches. No confidential access assumed.
2. **Coding reliability:** Have an independent reviewer recode E01–E08 and every matrix cell against an explicit rubric; preserve disagreements and corrections. Not yet completed.
3. **Technical bridge:** Map the existing Tiger Assurance synthetic authorization, revocation and provenance tests to decision rights, evidence access and change management; do not equate those tests with frontier-model evaluation. No new code or tests executed for this milestone.
4. **Institutional comparison:** Apply Nelson's institutional political economy as principal explanatory framework, with Packenham's political development approaches, GLOBE leadership distinctions and Signé's global AI divide as complementary lenses; test against contrary evidence and jurisdictional differences.
5. **Publication boundary:** Treat the register as a dated, public-source desk evaluation. Do not claim external validation, accreditation, government endorsement, SAFA participation or any confidential client findings.

**Milestone status:** Eight evidence entries and a four-case, seven-criterion comparative matrix **completed at the public-document desk-review level**. Independent source replication, primary-charter collection, technical crosswalk verification and external methodological review remain open.

## 2 November 2026 | Independent-method source recoding and synthetic control traceability

**Scope and independence declaration:** A separate second-pass desk recoding was performed using original public organizational disclosures, the author-published Mallaby historical excerpt and NIST AI RMF, without treating the preceding GRI matrix as dispositive. The reviewer was an AI-assisted research process acting within the same GRI workflow, **not an unaffiliated human reviewer**. GitHub test files and prior CI documentation were inspected; tests were **not executed anew**, no GitHub attestation was independently reverified in this pass, and no external review signoff is claimed.

### Second-pass coding rubric

For each case and criterion: **D = directly documented** by a cited primary institutional disclosure or exact repository test assertion; **H = supported by attributed historical reporting or author-published historical account**; **P = publicly proposed, without demonstrated implementation**; **N = not established in the reviewed evidence**. A source may support a structure or aspiration without supporting effective independent assurance. Record the narrower conclusion if a criterion combines several requirements.

| Case | Existence / formal structure | Reviewer independence | Funding and conflicts | Audit evidence access | Binding remedy | Global representation | Version-change retesting |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 2015 DeepMind ethics board | H: meeting and intended board | N | N | N | N | N | N |
| Project Mario | H: governance negotiations; P: independent arrangement | P | N | N | P | N | N |
| Frontier Model Forum | D: incorporated industry nonprofit and member board | P: evaluation ambitions; independence N | D: member fees; conflict controls N | P: support for evaluations; compulsory access N | N | P: collaboration ambitions; equitable influence N | N |
| Reported 2026 SAFA | P: proposed organization, formation N | P: auditor qualification; independence N | N | P: third-party testing; access rights N | N | N | N |

**Replicated conclusions:** The publicly documented Forum governance and member-fee funding classifications are confirmed by its [current organizational disclosure](https://www.frontiermodelforum.org/about-us/). Its [2023 founding announcement](https://www.frontiermodelforum.org/updates/announcing-the-frontier-model-forum/) supports an evaluation objective but does not itself prove an independent evaluator's authority. The [author-published Mallaby excerpt](https://colossus.com/article/project-mario-demis-hassabis-deepmind-mallaby/) supports a historical governance negotiation, not an implemented independent charter. The SAFA classification remains attributed to [September 2026 reporting](https://www.theinformation.com/articles/google-openai-anthropic-ai-safety-group-takes-shape/), without a verified operative charter. This is a reproducible *document classification*, not causal proof of industry capture, bias or safety outcomes.

**Correction and source discipline:** The earlier E08 classification as P was corrected in this register to S, denoting independent secondary research rather than a *primary organizational disclosure*. The correction is retained here for auditability; the original classification remains visible in Git history. E01 and E02 remain retrospective historical evidence; E06 remains press reporting. Coding should distinguish provenance class from whether a governance feature is documented. No underlying primary charters, signed auditor contracts or meeting minutes were newly obtained.

### Exact repository control-to-requirement mapping

Source paths below are relative to the [Tiger Legacy Version One implementation](version_one/). **Inspected assertions** means present in source, not newly executed or independently reproduced in this pass.

| Assurance requirement | Exact inspected test and behavior | Evidentiary boundary | NIST AI RMF relationship |
| --- | --- | --- | --- |
| Tenant isolation and default denial | [test_security.py](version_one/tests/test_security.py): `test_isolation_and_default_deny` rejects cross-tenant principals, missing resources and unauthorized reads | Synthetic in-memory principals; no real identity authentication or enterprise tenancy certification | Govern 2.1; Map 4.2; Measure 2.7 |
| Purpose-bounded authority and expiry | `test_grant_expiry_revocation`, `test_paired_authority_cases`: authorized view permitted before expiry; edit, expired and cross-tenant requests denied | No independent determination that a grantor is institutionally legitimate | Map 3.5; Measure 2.8 |
| Revocation and forged grant rejection | `test_grant_expiry_revocation`, `test_forged_grant`, `test_cross_tenant_grant`: revoke denies later access; wrong owner and tenant rejected | Does not establish human appeal, contractual revocation enforcement or external decision rights | Govern 2.1; Map 3.5 |
| In-memory event integrity and replay | `test_tampering`, `test_missing_event`, `test_replay`: mutation, missing event and duplicate identifier rejected/detected | HMAC chain is not independently anchored or an external audit | Measure 2.7; Measure 2.8 |
| Durable ledger tamper and truncation detection | [test_evidence_ledger.py](version_one/tests/test_evidence_ledger.py): `test_update_delete_fail_closed`, `test_mutated_payload_detected`, `test_truncation_detected_by_external_checkpoint`, `test_wrong_key_fails` | Crucial negative control: locally truncated ledger can self-verify unless compared with separately retained checkpoint | Govern 1.4; Measure 2.7 |
| Recovery, concurrency and reproducibility | `test_backup_restore`, `test_concurrent_unique_sequence`, `test_durable_reopen`: backup checkpoint match, concurrent append uniqueness and reopen verification | Tests of synthetic fixture behavior; not an independent disaster recovery audit | Measure 2.5; Measure 2.7 |
| Read-only reporting and fail-closed integrity | [test_reporting.py](version_one/tests/test_reporting.py): `test_offline_snapshot_read_does_not_modify_file`, `test_tamper_fails_closed`, `test_rehashed_unsafe_claim_fails_closed`, `test_deterministic_report` | Report hash and policy checks do not prove truth of inputs or security of real deployments | Govern 1.4; Measure 2.8 |
| Bridge integrity and retained original endpoint | [test_tiger_legacy_bridge.py](../ConsciousAI-Research-Systems/test_tiger_legacy_bridge.py): `test_swapped_report_and_rehashed_internal_digest_fails_pinned_manifest`, `test_original_tiger_assurance_route_retains_contract`, `test_http_success_and_fail_closed`; simulated integrity errors return HTTP 503 | Simulated local HTTP regression, not public service security or external accreditation | Govern 6.2; Measure 2.7 |
| Institutional legitimacy beyond valid cryptography | `test_local_evidence_check_is_not_task_completion`, `test_biased_observation_remains_a_failure_boundary`: verified chain coexists with uncompleted task or biased observation | These are synthetic counterexamples, not measured population effects or external adjudication | Map 2.3; Measure 2.8 |
| Reviewer appointment, funding conflicts, adverse publication, global representation and material model-update retesting | **No direct test assertion identified in the inspected suites** | Institutional governance gaps require charter, contractual and human-process evidence, not merely more cryptographic tests | Govern 1.5; Govern 5.1; Measure 1.3; Measure 3.1 |

NIST subcategory references are **analytical alignments**, not claims of compliance or certification. [NIST AI RMF Core](https://airc.nist.gov/airmf-resources/airmf/5-sec-core/) explicitly addresses independent assessors in Measure 1.3, ongoing review in Govern 1.5 and emergent risk tracking in Measure 3.1.

### Reproduction record and next gate

- **Completed in this pass:** Public-source second-pass coding; documented disagreement on E08 provenance classification; inspection of `test_security.py`, `test_reporting.py`, `test_evidence_ledger.py`, `test_tiger_legacy_bridge.py`, and existing [reproducible evidence documentation](REPRODUCIBLE-EVIDENCE-PACKAGE.md).
- **Not completed:** Fresh exact-commit test execution, independently held checkpoint challenge, attestation verification, independent reviewer identity/conflict declaration, independent human recoding and signed adjudication. Earlier CI evidence remains historical and commit-scoped; do not extend it to this documentation update.
- **Next independent gate:** Supply an unaffiliated reviewer the [independent reproduction protocol](INDEPENDENT-REPRODUCTION-PROTOCOL.md), a pinned source commit and E01–E08 source set. Require blind recoding, recorded disagreements, exact test output and signature/attestation verification before declaring independent reproduction.
- **Confidentiality:** Synthetic only; no real clients, credentials, restricted model evidence or production integration. No tests or services were modified by this documentary crosswalk.


### Pre-review internal quality assurance clarification (2 November 2026)

This section records documentary corrections, not independent validation. The source register uses P for primary organizational disclosure, H for historical accounts, R for reporting and S for independent secondary research. E08 is S; E01 is historical evidence and the day of the reported August 2015 meeting is not asserted without a sufficiently verified source. The AI-assisted second pass was conducted inside GRI, not by an unaffiliated reviewer. NIST AI RMF mappings are interpretive alignments, not compliance determinations. Earlier passing CI and attestation results apply only to their recorded commits; the submitted review commit `e34b1b89c627a6a35f6e50adb3f98043aeeed96d` requires fresh, exact-commit reproduction. Neither this documentary amendment nor any internal quality assurance constitutes an independent audit, a production security assessment or evidence that hypotheses H1–H3 have been empirically confirmed.
