# Uber Agentic Engineering: From Functional Guardrails to Institutional Accountability
Grand Research Institute (GRI) | Independent research working paper | 24 October 2026

**Evidence status:** This is GRI's original synthesis of engineering sources and a user-supplied copy of Pal et al.'s *Persona Guardrail*. It does not represent Uber collaboration, independently replicated performance, or a production deployment.

## Central research question
As enterprise AI evolves from advising humans to executing tasks, how should institutions specify delegated authority, enforce executable permissions, measure outcomes, and preserve human accountability?

## Uber engineering case map
1. **Persona Guardrail (Pal et al.).** Agent-specific semantic functional boundaries; synchronous input and output checks; versioned policies; evaluation, shadow mode, human review, limited rollout and rollback. The authors report on PAGE: baseline 85.7% versus iterated-allowlist 95.9% accuracy; OOD detection 57.3% versus 93.5%; false-approved rate 25.0% versus 4.7%. The evaluated hybrid allowlist+blocklist is *not* the highest-accuracy configuration: 94.9% accuracy with 8.2% false-blocked versus 95.9% and 3.6% for iterated allowlist. This is a direct malicious-user, turn-level threat model: no demonstrated prevention of compromised tools, indirect injection, unauthorized intermediate actions or multi-turn escalation.
2. **Legal Redlining Agent (Uber Engineering, October 8, 2026).** Word-integrated, lawyer-supervised contract review combines deterministic legal policy with probabilistic feedback retrieval and agentic clause proposals. Uber-reported figures of >20% review-time reduction and 91% decision accuracy require independent replication and explicit denominators. GRI question: how are suggestions, legal policy and professional sign-off separated?
3. **Stale feature flag/code cleanup (Uber Engineering, October 2026).** Agent-assisted removal of production technical debt. GRI question: what tests, change review, authorization and rollback evidence are required before a machine-generated deletion?
4. **MCP Gateway (Uber Engineering, October 2026).** Enterprise tool discovery and mediation. GRI question: does tool-time authorization enforce principal, scope, destination, resource and transaction limits independently of conversational classifiers?
5. **Software factory and enterprise AI adoption (Uber, October 2026).** Scaling agent-assisted engineering and knowledge work. GRI question: do throughput gains persist after accounting for defects, human review time, security, externalities and incident costs?

These case descriptions derive from previously supplied research notes and the provided manuscript; canonical blog links, exact titles and publication metadata should be verified before journal submission.

## Persona Guardrail: methodological reading
PAGE contains 2,180 labeled messages, comprising 2,076 persona-centric and 104 AgentHarm-derived messages. Four AgentDojo-derived domains are Workspace, Slack, Banking and Travel; the AgentDojo indirect-injection environment itself was not run. Mixed intents are an important boundary case: 92.2% were blocked, and scoring them as should-block versus should-approve changes apparent performance. The authors report P90 model-call latency below 100 ms over tested loads, but application/network overhead is excluded. Reported production false-block below 1% and false-allow below 2% are author claims, not independently audited statistics.

Production decision rates are not error rates without adjudicated ground truth. Discovery examples must be separated from held-out evaluation. Candidate policies should be cloned and reviewed rather than silently modifying active policy.

## Referenced literature: research map
**Attack and evaluation:** AgentDojo (Debenedetti et al., 2024); AgentHarm (Andriushchenko et al., 2025); InjecAgent (Zhan et al., 2024); Agent Security Bench (Zhang et al., 2025); agentic-security SoK (Kim, Guo & Song, 2026); indirect prompt injection (Greshake et al., 2023); CLINC150 out-of-scope detection (Larson et al., 2019).

**Trust architecture and execution:** CaMeL / *Defeating Prompt Injections by Design* (Debenedetti et al., 2025); Progent (Shi et al., 2025); IsolateGPT (Wu et al., 2025); Instruction Hierarchy (Wallace et al., 2024); StruQ and SecAlign (Chen et al., 2025); Task Shield (Jia et al., 2025); MELON (Zhu et al., 2025).

**Runtime guardrails:** LlamaFirewall (Chennabasappa et al., 2025); Llama Guard (Inan et al., 2023); WildGuard (Han et al., 2024); ShieldGemma (Zeng et al., 2024); Constitutional Classifiers (Sharma et al., 2025); NeMo Guardrails (Rebedea et al., 2023); Microsoft Prompt Shields (2025); OWASP Top 10 for LLM Applications (2025).

**Agent foundations and model serving:** Toolformer (Schick et al., 2023); ReAct (Yao et al., 2022); AutoGen (Wu et al., 2023); Qwen3-VL technical report (Bai et al., 2025). These works are mapped from the Pal et al. bibliography, not asserted to have been independently read or validated by GRI.

## Original GRI institutional governance framework (hypothesis)
**Mandate → Semantic Boundary → Executable Capability → Evidence → Contestability.**

- **Mandate:** accountable human principal, authorized purpose, applicable institutional rules and affected stakeholders.
- **Semantic boundary:** versioned agent allowlist, explicit prohibited intents and ambiguity escalation.
- **Executable capability:** independent tool-level enforcement of identity, resource, recipient, transaction ceiling, expiry and human approval before consequential side effects. An LLM's ALLOW token is not an authorization grant.
- **Evidence:** policy digest, action logs, independently labeled test sets, outcome quality, false-approved and false-blocked rates, latency percentiles and rollback proof.
- **Contestability:** appeals, incident review, correction mechanisms and human-approved policy revision.

This model extends, but is not attributed to, Uber's engineering. The **AI Compliance Paradox** hypothesis is that delegated machine capability can grow faster than institutions' ability to define authority, detect harm and provide remedies.

## Testable research propositions
H1: A versioned, iterated functional allowlist improves detection of competent-but-out-of-domain requests against a generic classifier on independently held-out data.
H2: Deterministic tool-time permissions prevent unauthorized intermediate actions that input/output guardrails alone cannot reliably stop.
H3: Agentic productivity gains diminish when reviewer effort, defect remediation and incident costs enter the denominator.
H4: Human-approved candidate policies with shadow testing and rollback produce more auditable change histories than automatic active-policy self-modification.

## Reproducible experiment plan — not yet executed
Create synthetic mobility, workspace, finance and code-maintenance agents without real credentials or customer data. Compare generic classifier, static allowlist, iterated allowlist, hybrid list and tool-time authorization. Evaluate benign, adversarial, OOD, cross-persona, mixed and multi-turn cases. Partition correlated examples and attack campaigns together; keep discovery separate from held-out golden, adversarial and production-analogue validation. Report accuracy, OOD recall, FAR=FN/(FN+TP), FBR=FP/(FP+TN), unauthorized tool execution, P50/P90/P99 latency, review burden, confidence intervals and sample sizes. Require human approval and rollback tests before any policy activation.

## Institutional interpretation
Roy C. Nelson's Three Worldviews framework, taught at Thunderbird School of Global Management at Arizona State University, offers a separate teaching lens: liberalism (market coordination and efficiency), economic nationalism (strategic capacity and security), and structuralism (power distribution and labor). GRI's independent extension examines how enterprise AI redistributes authority among companies, workers, users, infrastructure providers and regulators. No university endorsement is implied.

## Source and verification register
- Pal, B., Maddireddy, S. R., Munir, M. B., Puha, Z., Zhurovich, M., Raghavendra, A. & Tout, S. *Persona Guardrail: A Production-Grade Defense Framework for Agentic Systems*. Full manuscript text supplied by researcher; venue and DOI unverified.
- Uber Engineering, *Scaling AI in Legal: Building Uber's Redlining Agent* (October 8, 2026): canonical URL and quantitative claims pending source verification.
- Uber Engineering, stale feature flag cleanup / AutoClean, MCP Gateway and software-factory articles (October 2026): canonical titles, URLs and performance figures pending source verification.
- Pal et al. bibliography [1]–[28]: reference inventory derived from the supplied paper; primary-source review pending.

**Publication safeguard:** Do not equate a GitHub commit with an independently validated result, or a semantic guardrail with authenticated executable authority.
