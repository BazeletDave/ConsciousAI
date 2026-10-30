# Tiger Legacy V1.1 — GRI Research Advancement Plan

**Authority:** GRI conditional internal research approval, recorded 2026-10-29.  
**Research scope:** Institutional Assurance Framework (IAF), Training a Tiger, Tiger Assurance, Tiger Legacy.  
**Status:** Internal research continuation; no client implementation, external certification or commercialization.

## Verified starting point
The GitHub workflow runs for approval commit `21bc1af1f3ba385650a131081efedd6dfd0597e8` all concluded successfully: IAF Reproduction Gate, GRI Research Quality Gate, and Research rights and security checks. Earlier clean-run evidence was archived in artifact `iaf-reproduction` (run 40979376606, artifact 12943383364).

## Research work packages
### A. Adversarial institutional-control tests
- Introduce separately labeled synthetic cases for stale consent, conflicting delegation, incomplete provenance, unavailable reviewer, privilege escalation and attempted replay.
- Record explicit expected decisions and the source of each expected label.
- Separate test authorship from review of expected labels where practicable; document disagreements rather than suppress them.

### B. Evidence and reproducibility
- Pin test runtime and record commit SHA, inputs, fixture digests, execution log and artifact checksum.
- Test incorrect keys, altered records, rollback and missing external checkpoint custody.
- Preserve distinctions between local tamper evidence and independently witnessed evidence.

### C. Methodology and academic provenance
- Distinguish deterministic rule enforcement from empirical model robustness.
- Test alternate Q-learning rewards and training seeds; retain both positive and negative outcomes.
- Maintain an attribution register with exact publication/course references and page locations; do not claim faculty endorsement.

### D. Institutional evaluation
- Map controls to source integrity, authorization, consent and revocation, contestability, operator accountability, independent validation and remediation.
- Analyze authority and incentives using GRI's institutional political-economy framework.
- Publish limitations with every experimental result.

## Governance gates
**Allowed now:** synthetic engineering, adversarial tests, reproducibility checks, internal GRI scientific-panel review and draft research manuscripts.

**Requires a new decision:** PR merge, public publication, live deployment, third-party data access, any client-specific work, IP licensing, or financial arrangement.

## Review record
GRI's principal reports completing a full review and previously reported three other reviews. Signed individual reviewer reports, identities, and independent panel determinations have not been provided to this repository. This plan does not imply external scientific certification.

**Immediate next research deliverable:** adversarial fixture expansion with documented acceptance criteria and a reproducible CI evidence bundle.
