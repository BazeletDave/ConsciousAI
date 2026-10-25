# Independent research review operating procedure

**Current status: NO INDEPENDENT REVIEWS COMPLETED OR CLAIMED.** This protocol does not appoint reviewers or authorize release.

## Rights-clearing gate
A human data steward must inspect each source's terms and copyright, institutional teaching-case restrictions, interview consent, and publication permissions. Candidate metadata is **not** marked rights-cleared merely because a link is public. Do not ingest restricted Thunderbird course packets, student work, private interviews, screenshots, or personally identifiable driver data into the public dataset.

## Independent reviewer assignment
Assign two human reviewers with no authorship or material conflict for each case. A third independent adjudicator resolves disagreements. Record authenticated reviewer IDs, affiliations, conflicts, timestamped assessments, source documents inspected, rationales and immutable record digests in an access-controlled review system. Public releases should contain redacted audit metadata, not reviewer personal details or confidential source material.

## Annotation task
For each case, distinguish: (1) publisher authenticity, (2) whether the cited source actually supports the bounded claim, (3) factual corroboration beyond the original publisher, (4) methodological reproducibility, and (5) unresolved limitations. Label **supported / unsupported / indeterminate** with rationale; do not force indeterminate claims into binary ML ground truth.

## Benchmark design
The current metadata-only seed has too few distinct case families for a defensible holdout. Expand to multiple independent cases per institution and case family, de-duplicate near-identical sources, and group by shared source/case/participant before splitting. Freeze the test set before model development. Report dataset size, class balance, confidence intervals, confusion matrix, majority and rule-based baselines, error analysis, and subgroup results only where sample size and ethics permit.

## Promotion criteria
No benchmark report or model deployment is authorized until the steward signs off on rights, two human reviews and adjudication are completed, an independent holdout is locked, and a reproducible evaluation has actually run. Unmeasured values remain null.
