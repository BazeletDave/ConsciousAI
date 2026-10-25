# Frontier Hierarchical Governance: Integration Research Candidate v0.2.0

**Status:** GRI research prototype; not production-certified or accepted upstream.

This research track investigates deterministic three-layer governance: seven fail-closed absolute constraints, four ordered research priorities, and five instruction authority levels. An OPA/Rego v1 implementation, Python reference evaluator, tests, sample audit evidence, and fail-closed mandatory policy combiner have been assembled and tested locally in a portable research package.

## Architecture
- Trusted classification facts are mandatory; no raw-text keyword policy or hidden LLM calls.
- Absolute violations deny, unknown findings block pending review, and high risk escalates.
- Instructions are ranked root > system > developer > user > untrusted, with deny > escalate > allow on ties.
- Other regulatory policies must be independently evaluated. A host combines all mandatory verdicts by conjunction, not by allowing one policy to override another.
- Decision evidence includes a deterministic result and SHA-256 input digest. Signing and append-only audit storage remain integration requirements.

## Open-source connections
1. [GOPAL](https://github.com/Principled-Evolution/gopal) (Apache-2.0): primary upstream Rego integration target. Repository convention uses versioned policy areas, paired Rego tests and policy metadata; upstream is read-only for the connected account.
2. [Microsoft Agent Governance Toolkit](https://github.com/microsoft/agent-governance-toolkit) (MIT): candidate runtime enforcement host, not yet adapted.
3. AICertify and other OPA control planes: potential independent assessment and policy composition targets, not yet tested.

## Verification
Local Python test suite: **14 tests passed** (including seven individual absolute-constraint subtests). OPA binary was not available in the execution environment; Rego compilation, Rego test execution, cross-language parity, and real runtime enforcement are **not verified**. CI workflow has been drafted in the distributable package but has not run on GitHub.

## Research conclusions
This is an original GRI integration proposal based on public policy architectures, **not** an assertion of official Anthropic, OpenAI, or Microsoft internal rules. The 'reasoning obstruction' constraint concerns authorized auditability and does not require disclosure of private chain-of-thought. The module currently assumes that instruction applicability and classification provenance are established by a trusted host. Those assumptions are blockers to production-grade use.

## Production and upstream gates
Rego CI, applicability and priority-conflict semantics, authenticated classifier facts, runtime interception, kill-switch testing, append-only signed audit records, adversarial evaluation, version compatibility, licensing review and upstream maintainer acceptance.

No production service has been modified, and no upstream PR has been submitted.
