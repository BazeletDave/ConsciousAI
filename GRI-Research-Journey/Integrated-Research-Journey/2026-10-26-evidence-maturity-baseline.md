# Milestone | Reproducible Evidence-Maturity Baseline

**Date:** 26 October 2026. **Status:** Small, explicitly nonrepresentative baseline. Not an AI adoption survey, academic experiment, or employer hiring audit.

This milestone converts the six public GRI GitHub repository README reviews into a machine-readable register and reproducible count figure. It does **not** invent AI screening results, job outcomes, political persuasion effects or cross-country metrics.

- [Source register CSV](2026-10-26-repository-evidence-register.csv)
- [Python standard-library reproducibility script](reproduce_evidence_maturity.py)
- [Generated summary](2026-10-26-evidence-maturity-summary.md)

Run from this directory: `python3 reproduce_evidence_maturity.py`.

**Coding rule:** `documented_deployment=yes` is assigned only where the README expressly links an operational GRI dashboard; this is not independent verification of the live service. `no` means the README does not document an independently deployed AI system for the coded case, not evidence of absence. `documented_human_review=not_assessed` means the README inspection did not systematically establish human review for a specific deployed AI system. These are source-description classifications, not audit findings.

**Sampling limitation:** Six repositories were selected because they belong to the same GitHub owner and were inspected during the research session. They are not a random sample and cannot support population claims about governments, companies, universities, political campaigns, or AI hiring. External institutional cases require a separate protocol with official sources and peer-reviewed evaluation. Any subsequent figures must retain denominators, collection dates, uncertainty where applicable, and source provenance.

**Next study design:** preregister inclusion criteria, collect dated government AI inventories and publicly disclosed organizational AI policies, distinguish adoption claims from deployment evidence, double-code independent reviewer judgments, and report inter-rater agreement. Obtain consent and applicable review approvals before collecting individual applicant or student data.
