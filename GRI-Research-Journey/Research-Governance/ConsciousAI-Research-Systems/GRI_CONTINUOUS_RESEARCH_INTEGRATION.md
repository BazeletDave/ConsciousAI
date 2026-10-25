# Grand Research Institute — Continuous Research Integration

**Status:** Controlled research intake design; no automatic access to private ChatGPT conversations.

## Objective
Expand GRI's independently governed research knowledge through reviewed new conversations, academic sessions, public publications, field observations, and experimental results. Keep the public dashboard institution-focused, not a roster of researchers.

## Research intake lifecycle
1. **Capture:** Record an authorized GRI research contribution from ChatGPT or another source. Conversation content is not automatically synchronized with GitHub.
2. **Provenance:** Identify source, date, permission status, evidence type, and limits; do not publish confidential or copyrighted teaching materials.
3. **Classify:** Separate source-reported facts, direct observations, hypotheses, interpretations, and independently evaluated findings.
4. **Connect:** Relate the contribution to GRI programs in AI governance, mobility, algorithmic management, finance, leadership, and institutional accountability.
5. **Review:** Human approval before publishing sensitive claims or promoting verification status.
6. **Integrate:** Use GitHub review and passing checks; preserve source references, correction history, and prior versions.
7. **Evaluate:** Add reproducible tests and outcome measures where feasible. New information in a repository is knowledge-base growth, not evidence of model retraining.

## Example — Thunderbird AI session, October 2026
**Working GRI synthesis, not an official transcript.** A session with Marcos Serrato prompted questions about AI-enabled decision-making, continuous learning, data literacy, human judgment, and leadership adaptation. Explore the research loop **data → prediction → human judgment → action → outcome → feedback**. Test whether explicit feedback and review improve decision quality. These are research hypotheses, not validated results or attributable verbatim quotations.

Cross-reference related GRI research in governance, institutional legitimacy, organizational leadership, algorithmic management, and financial incentives. Verify any faculty-specific research claim against an authorized primary source before public attribution. Do not imply Thunderbird or ASU endorsement.

## Existing automation versus future learning
- `gri-policy-monitor.yml`: configured at `17 */3 * * *` UTC. Produces official metadata candidates and a review queue; keyword triage is not model training.
- `gri-governance-intelligence.yml`: configured at `43 */6 * * *` UTC. Collects public GitHub metadata for review.
- The dashboard's successful deployment does not establish that either scheduled workflow ran successfully at every interval.
- To substantiate learning, version datasets and algorithms, record training/update runs, use held-out evaluations, and document results and human approval.

## Required intake fields
Unique ID, recorded date, topic, GRI program, source and access rights, claim type, verification status, research question, hypothesis, limitations, proposed test, reviewer, and publication authorization.

## Next implementation controls
Validate structured intake records, add source-link integrity checks, maintain reviewer approvals and a correction ledger, and track scheduled workflow execution history separately from the live Render service.

**Scope protection:** No public dashboard redesign, no autonomous ingestion of private conversations, and no publication of restricted university materials.
