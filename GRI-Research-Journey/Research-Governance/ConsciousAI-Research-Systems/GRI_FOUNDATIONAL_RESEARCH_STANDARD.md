# Grand Research Institute — Foundational Research Controls

**Status:** Institutional research baseline · **Owner:** Grand Research Institute (GRI)  
**Scope:** Public-facing AI governance, algorithmic management, mobility, institutional intelligence, and reproducible research.

## Purpose
GRI develops independently governed research systems that connect empirical evidence, computational analysis, and institutional decision-making. Graduate study and published scholarship inform the methodology; the research, interpretations, and public outputs are GRI's responsibility. No university or faculty endorsement is implied.

## Five foundational controls

1. **Evidence provenance.** Each published research claim must identify a source, publication or observation date when known, evidence type, collection method, reviewer, and limitations. A publisher homepage alone does not verify a specific claim.
2. **Verification state.** Keep `hypothesis`, `reported`, `source_documented`, `independently_validated`, `contested`, and `retracted` distinct. Never silently upgrade existing statuses; legacy records remain as labeled until reviewed.
3. **Reproducibility.** Record the dataset version, transformation, algorithm or rule version, execution date, and evaluation method for each computed finding. Record missing measurements as null or not evaluated, not zero.
4. **Human accountability.** Human approval is required for public conclusions alleging misconduct, compliance findings, material external actions, or changes to verification classifications. Maintain a review and correction trail.
5. **Institutional independence.** Publish GRI research as GRI research. Cite source authors appropriately in supporting references; do not present a faculty roster, licensed course materials, or university affiliation as institutional sponsorship.

## Release gates
- **Integrity:** schema validation, nonbroken case/graph references, and source-link review.
- **Security:** no credentials, personal interview identifiers, restricted course content, or sensitive operational data in public outputs.
- **Research quality:** explicit uncertainty, provenance, and documented limitations.
- **Software quality:** automated regression tests, API health checks, and production endpoint smoke tests.
- **Deployment:** GitHub review → passing checks → controlled merge to `main` → Render automatic deployment → post-deployment verification.

## Research maturity levels
| Level | Required evidence | Permitted public description |
| --- | --- | --- |
| 0 — Concept | Research question and hypothesis | Proposed research |
| 1 — Registry | Source reference and stated limitations | Curated research record |
| 2 — Reproducible analysis | Versioned method and repeatable outputs | Reproducible analytical result |
| 3 — Independently evaluated | Defined test set, measurement protocol and review | Evaluated research result |
| 4 — Operationally monitored | Evaluation plus live monitoring, change control and incident response | Monitored research system |

**Important:** A live web service or successful HTTP response does not establish Level 3 or 4 research maturity.

## Near-term implementation backlog
1. Introduce a machine-readable evidence manifest and schema tests, retaining legacy case data.
2. Add evaluation fixtures and measurable baseline tests before publishing model performance claims.
3. Add timestamped production smoke checks and alerting for failed endpoints.
4. Establish a correction/retraction log and reviewer sign-off for elevated verification states.
5. Extend case coverage only with attributable public evidence and documented limitations.

## Change policy
Preserve the approved dashboard presentation. Changes to research data, methods and APIs should be additive and tested. Do not modify unrelated Render services. Maintain legal and academic integrity requirements, privacy safeguards, and independent institutional positioning.

*This document is a governance and research standard, not a claim that every control is already implemented.*
