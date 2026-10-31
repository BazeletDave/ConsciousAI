# GRI BZLT | Independent documentary review register

**Status:** Awaiting qualified human reviewer. No documentary claim is independently certified by this register.

## Review standard

The reviewer must inspect the underlying source, not merely the CSV or graph. For each edge E01–E19, record document title, issuer/custodian, exact passage or page, date of event, legal parties, financial units, relationship classification, and any conflicting records. Verify original documents or official archives and retain a permitted snapshot and SHA256 where practical. Reviewer must attest that they have no material conflict of interest with the reviewed party or disclose the conflict.

## Review checklist

| Group | Edges | Verification question | Human decision |
| --- | --- | --- | --- |
| 2015 Florida DOH review panel | E01–E03 | Does the actual adjudicative record identify the scorer on the claimed date, and how does it reconcile with the initial panel announcement? | Pending |
| Cresco / Bluma transaction and subsidiaries | E04–E09 | Is the acquisition date correct? Does the subsidiary schedule indicate consolidated ownership rather than direct parentage? Are share counts accurate? | Pending |
| Parallel asset foreclosure and SNDL financing | E10–E13, E17–E19 | Do each asset perimeter, indirect interest, reporting date, secured loan and extinguished debt figure match filed records? | Pending |
| Parallel operating brands | E14–E16 | Are the brands, locations, legal entities and state licenses accurately characterized at the event date? | Pending |

## Human review form

For each edge create a review row containing:
`edge_id, source_document, source_locator, reviewer_identifier, reviewer_role, review_date, evidence_snapshot_sha256, claim_verified_yes_no_partial, legal_entity_match, temporal_match, financial_unit_match, conflicts_found, corrective_action, decision, signoff`.

A reviewer may select **verified**, **rejected**, **qualified** or **unresolved**. Blank decisions remain unresolved. Reviewer identity should be stored in an access controlled review record if privacy or independence requires it; do not publish personal contact details. No AI generated signoff is permitted.

## Release gates

1. GitHub Actions workflow completes successfully against the exact checked out CSV, validator and tests, with downloadable retained artifact and SHA256 inputs.
2. All 19 relationships receive documentary review, with explicit resolution or quarantine of unsupported edges.
3. At least one qualified human reviewer signs the evidence decision register, and a separate person independently reproduces or spot checks material financial and legal claims.
4. The governance dashboard receives only an aggregate, read only, approved summary; **no connection or production integration before all gates pass**.

**Current disposition:** Gate 1 configured, execution not independently confirmed; Gates 2–4 pending. This document does not confer compliance certification, legal opinion or an external endorsement.


## Source inspection update: 31 October 2026

[Document inspection ledger](BZLT-Source-Inspection-Ledger.csv) records each of E01–E19 in grouped rows, original document titles, issuer/custodian, document section or passage locator, event date, parties/relationship, financial units, evidence limitations and pending reviewer fields. Grouped rows cover all 19 IDs but **do not substitute for individual signed reviews**.

**Source review classifications:** E04–E12 and E14–E19 source content inspected; E01–E03 and E13 blocked or unresolved. Even source confirmed items require human independent verification. No human reviewer has signed. No conflict of interest declaration has been supplied. No original document snapshot SHA256 has been retained; these fields are blank by design and must not be fabricated.

**Priority exceptions:** (1) The Florida DOH 2015 announced panel and later reported scoring panel differ, requiring original DOAH order and contemporaneous scoring sheets; (2) Cresco subsidiary schedules establish consolidated relationships, not all immediate legal parents; (3) SNDL July and September indirect exposure percentages must be kept at their separate as of dates; (4) issuer location counts do not independently verify regulatory licenses; (5) lender spelling and individual creditor allocation require original agreement reconciliation.

**Release status:** HOLD. An AI source inspection is not a qualified human attestation. A reviewer must supply actual name or controlled reviewer identifier, role, review date, exact passage or page, source snapshot checksum where permissible, conflicts disclosure and signed decision for each edge. Until then do not label the research independently certified or integrate an approved summary into the governance dashboard.


## Founder review and authorization record: 31 October 2026

**Recorded from direct user instruction:** The user, identifying the reviewer as **David Grand**, states that they personally reviewed the material, accept the ledger, confirm that documentary source inspection was completed, and authorize GRI to proceed. This is a **founder-reported human review and management authorization**, not a cryptographically authenticated signature or independent external attestation. Reviewer name spelling corrected to David Grand; formal signed certification and conflict disclosure remain separate requirements.

**Review disposition:** Founder acceptance recorded for the inspected ledger, subject to the explicitly preserved source exceptions and release gates below. This authorization does not resolve inaccessible source E01–E03 or E13, establish document SHA256 snapshots, attest to absence of material conflicts, or prove CI success.

**Conflict disclosure:** Not supplied in the authorization. A formal statement of no material conflict or a specific disclosure is required before this review is represented as independently conflict assessed. Given the founder's disclosed historical professional involvement, the review must be labeled **founder review**, not independent review.

**Operational authority:** Proceed with controlled research, source remediation, exact commit CI verification, and preparation of a read only dashboard summary. Do not publish the unresolved edges as independently verified, claim external assurance, or activate the dashboard release until the acceptance gates are satisfied. No previous employer affiliation is implied.
