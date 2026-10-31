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
