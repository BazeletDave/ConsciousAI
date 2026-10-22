# GRI Governance, Lawful Access and Autonomous Learning Policy (v1)
**Status:** Internal engineering policy proposal. Applies to GRI research ingestion, evaluation, model training and publication. **Not a legal opinion or compliance certification.** GRI operates in Florida; jurisdiction-specific legal review is required before adding new activities.

## Mission and scope
GRI advances independent, evidence-based research into algorithmic management, AI safety, institutional governance and the AI Paradox. The system must preserve source integrity, research independence, human accountability, privacy and lawful access. Publicly available information is not automatically free of contractual, licensing, copyright, privacy or access restrictions.

## Authority boundaries
**Automatic / bounded:** ingest allowlisted official public feeds and explicitly permitted datasets; record original source URLs, publisher, collection timestamp, permitted use and provenance; deduplicate; run read-only integrity checks; produce internal draft summaries and evaluation metrics. No automatic model promotion.

**Human approval required:** publish incident attribution or allegations, share personal information, add new external sources or licenses, change training corpora, deploy or promote models, modify policy, change permissions, send external notices, make consequential decisions or perform security actions. Review must be recorded with reviewer identity, scope, version, rationale and timestamp.

**Disallowed by default:** bypass authentication, access controls, rate limits or robots/terms restrictions; intrusive scanning, exploitation or penetration testing without documented authorization; acquire classified, restricted or unlawfully obtained data; impersonate agencies; claim agency affiliation or endorsement; republish sensitive personal data; conduct surveillance without lawful basis; auto-remediate third-party systems; self-modify safety rules.

## Controls
1. **Source register:** owner/publisher, endpoint, agency, jurisdiction, official/public designation, license/terms, collection method, retention, attribution and review date. New sources fail closed until approved.
2. **Government-source handling:** FBI, CISA, NSA, NIST and other agency publications are treated as attributed statements, not independent confirmation of claims. Record exact advisory/CVE/document identifiers, issue and retrieval dates. Separate government announcements, allegations, verified technical findings and attribution confidence. FOIA and Florida public-records processes do not authorize bypassing agency access controls.
3. **Data minimization:** default to no personal identifiers; restrict and encrypt sensitive data; maintain retention/deletion procedures and incident response. Florida Statutes §501.171 may apply to covered entities holding personal information.
4. **Learning governance:** training datasets require provenance, permitted use, independent labels, train/test isolation, bias/drift and calibration evaluation. Never use model-generated conclusions as self-validating ground truth. Human approval before retraining or promotion.
5. **Change control:** CI checks, versioned policy and model artifacts, rollback, least privilege, secrets outside Git, reviewable logs. A learning agent cannot approve its own permission or policy changes.
6. **Transparency:** clearly mark prototypes, unverified sources, unavailable performance metrics and confidence limits; allow correction and contestation.
7. **Legal change monitoring:** track applicable federal/Florida requirements and agency source terms. Counsel should review specific planned processing and contractual obligations. Policy text does not guarantee legal compliance.

## Primary references (consult current versions)
- U.S. Computer Fraud and Abuse Act, 18 USC §1030: https://uscode.house.gov/us/usc/119-118/t18/s1030/
- Florida Information Protection Act, Fla. Stat. §501.171: https://www.flsenate.gov/Laws/Statutes/2024/501.171
- NIST AI Risk Management Framework, Govern/Map/Measure/Manage: https://airc.nist.gov/airmf-resources/airmf/5-sec-core/
- NIST AI RMF Playbook: https://airc.nist.gov/airmf-resources/playbook/
- CISA Automated Indicator Sharing terms (specific to AIS participation): https://www.cisa.gov/sites/default/files/2022-12/AIS%20Terms%20of%20Use%20v3.0_508_0.pdf

## Enforcement boundary
The companion `governance_gate.py` implements a conservative, **local deterministic preflight** for future autonomous workflows. It is not integrated with external collectors or agents until those workflows explicitly call it. It does not establish legal compliance. No unattended retraining, source additions or policy changes are authorized by this document.
