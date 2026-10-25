# Uber AutoClean: Agentic Code Maintenance and Institutional Governance

Grand Research Institute | Research Journey | 22 October 2026  
Status: comparative industry case, preliminary source verification  
Research framework: Nelson Model institutional analysis as independently applied by GRI

## Research question
How does an organization delegate multistep software maintenance to AI agents while preserving technical correctness, bounded authority, accountability, and human authorization?

## Industry primary source
Uber Engineering, *AutoClean* article, text supplied to GRI on 22 October 2026. Exact original publication URL, date, and authorship remain to be independently verified before formal academic citation. The article reports cumulative cleanup of more than 16,000 feature flags and more than 1,000,000 lines of code over several years. These are company self-reported figures, not independently audited outcomes.

## Described architecture
1. Uber's feature flag system identifies stale production flags.
2. An agent traces call sites, configuration, conditionals, and tests, using PolyglotPiranha through MCP for deterministic Boolean simplification.
3. Continuous integration (CI) tests the diff; scoped deterministic fixers precede agentic fixers, with restricted editing authority (for example, test fixers may edit only tests).
4. Static validation checks for incomplete or mechanically invalid cleanup.
5. CodeCourt independently evaluates focused properties in parallel: no additions, semantic preservation, no intent drift, and no agent artifacts. Failure of any property abandons the diff.
6. Passing diffs proceed to owning engineers for human review and final decision.

The source describes the architecture and workflow; it does not establish independent proof of semantic equivalence in all production contexts, the rate of undetected errors, or downstream organizational effects.

## Institutional interpretation: Nelson Model
This section is GRI's independent application of institutional analysis influenced by Roy C. Nelson's Thunderbird teaching. It does not attribute these AI governance indicators to Nelson as an original published instrument or imply faculty or university endorsement.

| Dimension | Institutional question | Potential observable evidence |
| --- | --- | --- |
| Rules | Which cleanup actions and approval criteria are authorized? | Policy versions, scoped tool permissions, review requirements |
| Actors | Who performs, verifies, approves, and can reverse changes? | Agent identities, owners, reviewer assignments |
| Interests | What tradeoffs exist between speed, cost, reliability, and technical debt? | Engineering effort, incident data, review time |
| Power | Where are execution, veto, and deployment rights located? | Branch protections, permissions, CI gates |
| Accountability | Who owns a regression despite passing automated checks? | Incident records, escalation paths, corrective action |
| Adaptation | How are failures converted into new governance constraints? | Validator revisions, audit trails, postmortems |

## GRI comparative analysis
**Uber MCP Gateway:** controls which tools agents can discover and invoke; AutoClean adds bounded code editing and independent output validation.  
**Microsoft AGT/ACS:** useful comparator for declared permissions and enforceable agent boundaries; architectural similarity does not establish equivalent implementations.  
**GRI PHP remediation prototype:** comparable evidence gates include verified source provenance, version and runtime consistency, CI, and human authorization. The GRI prototype is not a production equivalent of AutoClean.  
**Platform algorithmic management:** connects machine-directed labor coordination to machine-executed engineering workflows without implying that the same algorithms or worker outcomes are involved.

## Falsifiable propositions
- P1: Explicitly scoped agent permissions reduce unauthorized modification attempts relative to broad permissions, controlling for task complexity.
- P2: Independent property-specific validators identify more relevant defects than a single generalist reviewer under matched evaluation conditions.
- P3: Passing CI is insufficient to establish complete cleanup or preservation of intended behavior.
- P4: Clear human approval boundaries improve attribution of deployment decisions but do not alone prove effective accountability.

## Empirical protocol and limitations
Collect task-level diffs, flag state evidence, CI results, validator verdicts, reviewer decisions, reversions, defects, and total compute and labor costs. Compare matched cleanup tasks and record selection effects, false positives, false negatives, and failures abandoned before review. No access to Uber internal logs or evaluation data is claimed. Claims about labor displacement, financial return, or comparative superiority remain untested.

## Research governance
Evidence classification: industry primary-source self-report; GRI analytical interpretation; unvalidated hypotheses. Verify publication metadata and preserve source snapshots and retrieval date in the source register. Do not reproduce proprietary code or claim Uber endorsement. No software or deployment changes are proposed by this case study.

## Research integration update | 24 October 2026

### Governance separation and decision rights
AutoClean is an instructive example of differentiated authority: the cleanup agent proposes code changes, PolyglotPiranha performs deterministic Boolean transformations, scoped fixers address CI failures, CodeCourt evaluates final properties independently, and human owners decide whether to accept the change. The reported validation gate is a design control, not independent evidence of zero regressions.

### Comparative Uber engineering evidence
- **Persona Guardrail:** input and output boundary enforcement for agentic capabilities. Compare authorization at invocation time against AutoClean's verification of a resulting code diff. See [GRI Persona Guardrail analysis](../Algorithmic-Management/Uber-Lyft-Research/uber-persona-guardrail-institutional-authority-2026-10-23.md).
- **Legal Redlining Agent:** lawyer-supervised document changes and a combination of deterministic policy and probabilistic feedback. Compare human legal approval against AutoClean's engineering ownership and review. The reported efficiency and accuracy measures are not interchangeable with AutoClean's cleanup counts.
- **Comparative synthesis:** [Uber Agentic Engineering: From Functional Guardrails to Institutional Accountability](../Algorithmic-Management/Uber-Lyft-Research/2026-10-24-uber-agentic-engineering-reference-synthesis.md).

### GRI governance intelligence platform design implications (proposals, not implemented features)
1. **Execution and verification separation:** assign task-performing and independently evaluating agents distinct permissions, identities and audit events.
2. **Deterministic-first policy:** prefer executable invariants, schema validation, static checks and constrained transformations before model judgment.
3. **Capability-scoped repair:** define allowed file classes, operations, tools and time-limited authorizations; disallow a test repair agent from altering production code.
4. **Evidence-linked approval:** retain the originating task, tool invocations, diff hashes, CI outcomes, property-level verdicts, human reviewer identity and decision.
5. **Fail-closed escalation:** reject or quarantine artifacts when critical validators fail; provide appeal and authorized re-evaluation rather than silently bypassing gates.
6. **Measurement and learning:** track defect escape rate, false rejections, reviewer burden, total cost, elapsed time and reversal frequency before claiming effectiveness.

### Testable comparative design
Evaluate matched maintenance tasks across (A) general-purpose agent plus CI, (B) deterministic tooling plus CI, and (C) scoped agent, deterministic transformations, CI, independent property validators and human approval. Pre-register semantic-regression and scope-violation outcomes, use blinded reviewers where possible, and record rejected as well as accepted changes. This is a proposed study, not a completed experiment.

### Institutional boundary
GRI's independent interpretation is informed by institutional and global-management study at Thunderbird School of Global Management at Arizona State University. Neither Uber nor Thunderbird endorses these hypotheses. The supplied Uber Engineering text is a corporate primary account; original URL, publication metadata, validation dataset and cost figures require independent verification before scholarly citation. This update adds no Uber proprietary source code and does not assert that GRI's deployed platform implements AutoClean or CodeCourt.
