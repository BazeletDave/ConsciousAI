# GRI BZLT Americas FLA Institutional | Institutional intelligence research protocol

**Status:** Research and engineering specification; not an implemented or validated autonomous assurance service. **Scope:** Extend existing GRI research, evidence graph and institutional assurance work. No new repository, deployment, agent service, external integration or disclosure of confidential material is authorized by this protocol.

## Independence and research disclosure

GRI BZLT Americas FLA Institutional is an independent research initiative of Grand Research Institute. Its founder reports historical professional involvement in the development of Florida's medical cannabis industry. This experience may help frame research questions but is not a substitute for independently verifiable documentary evidence. The research is not undertaken for, or on behalf of, any prior employer, license holder, company, executive or related organization. No confidential, proprietary, privileged or nonpublic information from prior professional relationships may be introduced into this research or any AI model, dataset, prompt, repository or dashboard. Any researcher's potentially material prior interests should be recorded privately and assessed for recusal or independent review where warranted.

**Disclosure validation gate:** The founder's former company's precise legal name, corporate lineage, relative market size, historical licensing role and alleged influence are not asserted here. Publish only verified, dated statements, and do not use the GRI BZLT research designation to imply a relationship with any historical corporation. No claim of institutional endorsement.

## Primary research question

Can source constrained agents turn a dated Florida regulatory and agricultural ownership history into reproducible institutional hypotheses, independently testable compliance findings, and governance insights that transfer to existing GRI research on algorithmic management, institutional adaptability, evidence integrity and the AI Paradox?

## Florida historical case expansion

Research targets include Hackney Nursery / Hackney farms and Quincy cultivation; Oglesby farms and Alpha, Florida (resolve exact legal entities and county); Alpha Foliage and Homestead; Knox Nursery / Knox Medical / Fluent and Apopka; 3 Boys Farm and Cresco; Surterra / Parallel and the 2026 SNDL restructuring; Verano / AltMed / MÜV; Pigford eligible applicants and subsequent awardees. Names and geographic leads are **research leads, not verified land title, license transfers, equity interests or historical operating relationships** until supported by deed, corporate, licensing or securities records.

## Evidence graph contract

Every relationship must contain `edge_id`, `source_entity_id`, `target_entity_id`, `relationship_type`, `effective_from`, `effective_to` or unknown, `jurisdiction`, `record_custodian`, `source_url`, `document_date`, `retrieval_date`, `source_snapshot_hash` if retained, `claim_location`, `evidence_class`, `verification_status`, `reviewer`, `confidence_rationale`, `conflicts`, `supersedes` and `privacy_class`. Historical statements without precise dates are not present tense ownership edges. Record source snapshots only where lawful and needed for reproducibility.

**No invented edge rule:** A registered agent is not a beneficial owner; an operator is not a landowner; a brand is not a license; a lender is not automatically an equity holder; a campaign contribution is not proof of regulatory influence; a legal medical authorization is not a clinical outcome; a model score is not an audit conclusion.

## Proposed bounded agent workflow

1. **Source acquisition:** Whitelisted official OMMU, Florida administrative docket, county clerk and appraiser, Sunbiz, SEC, Florida Legislature, election/lobbying disclosures and other state regulator records. Respect source terms, access limits and privacy.
2. **Document classification:** Extract record type, authority, relevant date, parties, entity identifiers, parcel identifiers, monetary terms and version; attach exact text location and provenance.
3. **Entity resolution:** Compare names and identifiers; never automatically merge similar people, farms, brands or corporate entities. Require human review for uncertain matches.
4. **Temporal graph construction:** Add source backed typed edges with as of dates; preserve original records, superseded relationships, failed proposals and unresolved disputes.
5. **Financial reconciliation:** Separate purchase price, announced valuation, stock issuance, debt extinguishment, related party lease, taxes and issuer wide versus Florida revenue. Generate reproducible calculations with source denominators.
6. **Institutional hypothesis testing:** Compare entry barriers, licensing appeal outcomes, financing concentration, land ownership separation, regulatory transition costs and evidence availability across original and subsequent license cohorts. Predefine competing explanations and avoid causal overclaim.
7. **Assurance and escalation:** Deterministic evidence checks, source conflict alerts, independent replay and qualified human review before publication. Withhold claims with insufficient evidence.

## Cross project integration within existing repository

| Existing research | Reusable research output | Hypothesis to test |
| --- | --- | --- |
| Institutional Frameworks and Adaptation | Longitudinal authority, licensing and ownership timeline | Does rule change alter actual accountability or only formal authorization? |
| AI Paradox / Training a Tiger | Bounded agent scenario with conflicting corporate and regulator records | Can a technically correct extraction create an institutionally incorrect conclusion? |
| Tiger Assurance / Institutional Assurance Framework | Source provenance, permission, exception, appeal and independent replay controls | Can evidence verification detect stale ownership, contradictory dates and unsupported causal edges? |
| Algorithmic Management / Driver safety | Medical authorization versus functional impairment distinction | Does a compliance classifier incorrectly substitute authorization for safety evidence? |
| GRI governance dashboard | Read only counts of verified, contested, unresolved and independently reviewed edges | Does evidence coverage improve without increasing false confidence? |

These are **proposed conceptual connections**; no new ML model, data pipeline or dashboard integration is claimed to exist.

## First controlled evaluation

Select 30 dated Florida records across original licensing, farm or property ownership, corporate acquisition, finance, lobbying and Pigford administrative processes. Require at least 10 deliberately ambiguous or conflicting entity/date pairs. Compare automated extraction and linking against independently labeled human adjudications. Report precision, recall, false approval rate, unresolved edge rate, source coverage, replay success, reviewer time, and disagreements. Predefine pass criteria before execution; do not present the proposed 30 record evaluation as a completed study.

## Publication and governance controls

Use only public records or information expressly authorized for the research. Do not disclose confidential former employer details, private contact information, personal addresses or nonpublic security methods. Use public corporate parcel references only when materially relevant. Avoid claims about motives, impropriety or misconduct without adjudicated or independently corroborated evidence. Preserve the distinction between an investigative lead, a source supported claim, a legal finding and an independently assured conclusion.

**Related:** [Dated relationship graph](BZLT-Dated-Relationship-Graph.md), [evidence edge register](BZLT-Dated-Relationships.csv), [financial and governance exhibits](BZLT-Americas-FLA-Institutional-Exhibits.md), [institutional assurance framework](../Research-Governance/Tiger-Legacy/INSTITUTIONAL-ASSURANCE-FRAMEWORK-v1.md).


## Implemented reusable evidence metadata capability

The [offline validator](bzlt_assurance.py) now checks the [dated edge register](BZLT-Dated-Relationships.csv) for required fields, unique IDs, ISO dates, typed relations, HTTPS source URLs and self relations. The [regression tests](test_bzlt_assurance.py) include valid baseline and adverse cases. Both are Python standard library only; neither accesses the network or processes private records.

**Run locally:** `python bzlt_assurance.py --output bzlt_assurance_report.json` then `python -m unittest test_bzlt_assurance.py` from this collection directory. Do not commit generated reports containing sensitive information. The report is metadata validation, **not source document verification, ML model validation, independent human review, regulatory certification or a completed deployment**. As of this commit the scripts have been added, but a clean environment test run has not been independently verified.

**Integration boundary:** Keep the source linked graph as research data, deterministic validation as the evidence control, and the existing GRI governance dashboard as a future read only display after review. Do not activate scraping, new agents, external services or model training without separate authorization and privacy testing.
