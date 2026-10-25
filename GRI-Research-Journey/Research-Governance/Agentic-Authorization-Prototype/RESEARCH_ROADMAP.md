# GRI agentic guardrails and authorization: research roadmap

## Research question
Can independently enforceable tool permissions complement semantic input/output guardrails and reduce unauthorized agent actions without unacceptable rejection of legitimate requests?

## Existing implementation
- `guardrail.py`: deterministic exact-intent and action-scope checks; no LLM classifier.
- `secure_authorization.py`: signed, expiring, one-use authorization grant with demonstration-only process-local replay tracking.
- `evaluation_suite.py`: eight handcrafted regression cases; not a representative security benchmark.
- `source_verification.md`: preliminary source ledger, with explicit unverified entries.

## Layered architecture
1. **Semantic boundary**: optional classifier detects in-scope and out-of-scope inputs and outputs; its decisions are advisory for tool execution.
2. **Deterministic authorization**: validate authenticated principal, agent, policy digest, exact tool/resource, spending cap, and signed approval.
3. **Tool execution boundary**: check grants immediately before side effects; execute with least-privilege credentials; enforce idempotency and atomic replay prevention.
4. **Evidence and evaluation**: record decision codes, policy version, approved action digest, trace IDs, latency, and independent labels without default retention of raw private content.
5. **Governance**: candidate policies evaluated offline, human reviewed, shadow tested, and rolled back on regressions.

## Critical gaps before production
- Replace process-local replay store with atomic durable shared storage and expiration cleanup.
- Bind grants to authenticated identities, trusted issuance, and revocation.
- Add server-side transaction locking, idempotency, time-of-check/time-of-use protections, and secure secret rotation.
- Harden malformed numeric types, NaN/Infinity, serialization, policy schemas, and audit log tampering.
- Implement a separately benchmarked semantic model; do not label deterministic rules as ML.
- Obtain original publications, validate citations and dates, and reproduce baselines with isolated held-out data.
- Add CI on the exact prototype directory and verify actual test run results.
- Obtain security review before connecting this code to production tools or Render.

## Evaluation protocol
Use separately sourced benign, adversarial, out-of-domain, and mixed-intent examples. Split by conversation and attack family to avoid leakage. Define block as the positive class; report confusion matrix, false-approved and false-blocked rates, confidence intervals, latency percentiles, and tool-side-effect escape rate. Never compare the eight-case deterministic suite to Uber PAGE's 95.9% reported accuracy.

## Attribution
Pal et al., *Persona Guardrail: A Production-Grade Defense Framework for Agentic Systems* (researcher-supplied manuscript; publisher status unverified). This project is an independent GRI research implementation, not Uber code or a claim of production-equivalent protection.
