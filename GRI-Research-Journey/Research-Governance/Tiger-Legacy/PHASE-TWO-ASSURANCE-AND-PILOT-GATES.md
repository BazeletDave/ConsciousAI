# Tiger Legacy Version One | Phase Two Assurance and Controlled Pilot Gates
**Status:** Phase Two preparation; not an independent audit or production authorization.
**Frozen source baseline:** `03e25f5d07cbf7b740358ad3bc94adee29c05659`
**CI evidence:** [Research workflow](https://github.com/BazeletDave/ConsciousAI/actions/runs/41155845450), [rights workflow](https://github.com/BazeletDave/ConsciousAI/actions/runs/41155845432).
**Verified suite sizes:** 71 synthetic Tiger Legacy tests; 227 dashboard/research regression tests. GitHub signed provenance verification step succeeded.

## Track A: Independent assurance
1. Assign an external reviewer with documented independence and conflicts.
2. Reproduce the frozen commit in a reviewer-controlled environment, recording OS, Python, SQLite, gh CLI, exact commands, exit codes and full logs.
3. Independently verify signed provenance against the pinned artifact and review the signing trust assumptions.
4. Conduct negative challenges: identity spoofing, cross-tenant access, consent expiry and revocation, tampering, replay, truncation, independently retained checkpoint, backup rollback, recovery and denial of service.
5. Publish a controlled-access findings register: finding ID, severity, evidence, reproducibility, owner, remediation, retest result, residual risk and reviewer signature.
**Gate A acceptance:** Independent written reproduction and explicit disposition of all critical/high findings. CI alone is not external review.

## Track B: Synthetic pilot readiness
1. Define a generic pilot profile and a second simulated tenant; use invented identities, resources, consent events and fixtures only.
2. Maintain tenant segregation, trusted synthetic identity, least privilege, fail-closed decisions, revocation and separate evidence custody.
3. Record pilot success/failure criteria before executing tests: unauthorized access rejected, revocation immediate within the modeled workflow, tamper and rollback detected, recovery behavior documented, original Training a Tiger tests unaffected.
4. Build a client-facing requirements and responsibility matrix **without inserting any client audit, private code, credentials, media or personal data in the public repository**.
5. For any real Family Legacy integration, obtain a written scope of work identifying the legal owner, authorized systems, test methods, allowed data, credential handling, deployment authority, incident contacts and stop conditions.
**Gate B acceptance:** Synthetic pilot evidence and documented authorization boundaries. Client approval in principle is not a blanket permission for unrestricted penetration testing or live access.

## Evidence classes and release decisions
- **Historical CI verified:** frozen baseline at the stated SHA.
- **Prepared:** reviewer handoff, synthetic pilot plan, gate definitions.
- **Not yet demonstrated:** external reviewer signoff, production security, real tenant isolation, client remediation, independent recovery exercise.
- **Prohibited without further authorization:** live client scans, production deployment, public disclosure of proprietary implementation or confidential client information.

## Academic and institutional research opportunity
Kiongozi (institutional leadership) asks whether governance is legitimate, contestable and accountable. Training a Tiger supplies controlled experimental evidence. Tiger Assurance tests evidentiary claims; Tiger Legacy evaluates whether controls remain enforceable across authorization, failure and recovery. Preserve attribution, methods, evidence classes and limitations; do not equate engineering tests with academic validation.
