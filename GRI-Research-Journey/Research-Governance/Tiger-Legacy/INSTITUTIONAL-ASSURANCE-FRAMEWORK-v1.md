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
- **Landry Singh — AI divide / institutional capacity:** Candidate applications: unequal access, capacity constraints, and disparate remediation pathways. **Specific source and attribution pending verification.**
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
| IAF-06 | Singh candidate: equitable access | Alternative review channel and disparate-impact monitoring | Synthetic low-access cohort cannot use default appeal | Appeal completion gap by cohort | Cohort definitions, privacy-preserving aggregate |
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
