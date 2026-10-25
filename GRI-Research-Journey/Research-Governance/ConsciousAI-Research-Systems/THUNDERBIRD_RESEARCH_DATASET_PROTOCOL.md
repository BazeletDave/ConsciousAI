# Thunderbird-informed institutional research dataset protocol

**Status:** Research protocol, not an independently labeled dataset. **Institution:** Thunderbird School of Global Management at Arizona State University. Educational frameworks are attributed to faculty; GRI extensions are separate hypotheses.

## Candidate case families
- **Roy C. Nelson — institutional and political-economy analysis:** Intel site selection; Brazil versus Argentina investment decisions; WTO cotton and wind disputes; IFC environmental and social safeguards; Brazil's devaluation. Apply liberalism, economic nationalism and structuralism as *alternative analytical lenses*, not ground-truth labels.
- **Global leadership and intercultural communication:** cross-cultural leadership and negotiation, with GLOBE dimensions only when the specific question warrants them. No country-level stereotype is an individual label.
- **Algorithmic management:** Uber/Lyft operational claims, driver-reported offers, and platform engineering disclosures. Keep contributor testimony, company disclosures and verified measurements separate.
- **Agentic governance:** delegation, capability boundaries, approvals, traceability, exception handling, and institutional accountability.

## Source and copyright controls
Teaching materials, proprietary case packets, graded submissions and identifiable interview data are **not** copied into public training sets. Public records are limited to bibliographic metadata, original GRI analytical annotations and links to lawful source material. Faculty-developed frameworks must be credited. Institutional affiliation is not an endorsement.

## Labeling and review protocol
1. Record claim, provenance URL or authorized internal citation, source type, jurisdiction, time and limitations.
2. Attach a SHA-256 digest to the frozen record and version the dataset manifest.
3. Two distinct authorized reviewers independently assess *source authenticity*, *claim support*, *context* and *uncertainty*. Preserve disagreement and adjudication.
4. A separate steward validates reviewer identity, independence, rights/consent and evidence links. Never infer these from self-reported fields.
5. Create a documented holdout split **by case family and source**, not random snippets from the same case. Prevent near-duplicate leakage.
6. Evaluate against a fixed baseline, report per-class performance, confidence intervals and subgroup coverage where justified; publish failure cases and limitations.
7. Require security, privacy, licensing, ethics and human release approval before any model promotion.

## Research-ready label schema (proposal)
`record_id, source_family, institution, claim_type, evidence_tier, source_uri, observed_at, rights_status, reviewer_1, reviewer_2, adjudicator, disagreement, label, label_rationale, record_digest, split, limitations`.

No claim is independently reviewed merely because it appears in an existing case registry. No ML performance is represented until a rights-cleared, independently labeled holdout exists.
