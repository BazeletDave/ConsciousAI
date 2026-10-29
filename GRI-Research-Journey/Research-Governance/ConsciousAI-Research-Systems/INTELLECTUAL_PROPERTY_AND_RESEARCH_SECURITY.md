# Intellectual Property, Attribution and Research Security Guardrails

**Owner:** Grand Research Institute (GRI). **Scope:** ConsciousAI research repository, public source registry, AI governance dashboard and future machine learning pipelines. **Status:** Governance policy; not proof of technical enforcement or legal ownership.

## Rights and attribution
1. Public accessibility does not imply public domain status, a license to reproduce, or authorization to train models. Store bibliographic metadata, lawful links and original GRI analysis by default.
2. Dr. **Landry Signé** retains attribution and all rights belonging to him or his publishers and institutions. No faculty affiliation, classroom access or personal relationship implies assignment of intellectual property or endorsement of GRI.
3. GRI records its independently authored analyses, original code, research instruments, system designs and derivative insights separately, subject to third-party rights, employment or academic agreements, and applicable law. GRI does not claim ownership of source materials merely because they were read, taught, discussed or submitted to a research system.
4. For course materials, teaching cases, slides, transcripts, notes, recordings and private communications, default to **restricted** until permission, license and applicable academic policy are established. Original recollections may inform research questions but must not expose protected material.
5. For quotations, figures and excerpts, require a source locator, rights basis, excerpt limits and human review before publication. Preserve citations and distinguish direct quotation, paraphrase, inference and GRI hypothesis.
6. Do not upload credentials, personally identifying research records, unpublished faculty material, proprietary classroom packets or unlicensed copyrighted full text to public GitHub.

## Machine learning and dashboard gates
Each intake record must include `source_id`, `author`, `publisher`, `url`, `rights_basis`, `license`, `visibility`, `ingestion_permission`, `training_permission`, `citation_locator`, `content_hash`, `reviewer`, and `review_status`.
- Default `visibility=restricted`, `ingestion_permission=false`, `training_permission=false` until independently checked.
- Publicly linked metadata may be indexed once verified; indexing is not model training.
- Block training on materials without affirmative documented authorization or another documented legally valid rights basis.
- Label model outputs as **GRI analysis**; never impersonate Dr. Signé or suggest his endorsement.
- Require human approval and test evidence for promotion to the production collector, dashboard or ML training pipeline.
- Preserve audit logs, version history, correction and takedown procedures, and a provenance trail from source to derived claim.
- Treat source documents as untrusted input: isolate parsing, reject prompt injection instructions, avoid secrets in logs, and limit agent tool permissions.
- Do not silently bypass a failed license, attribution, privacy, or security gate.

## Security implementation checklist (not yet attested)
Repository access controls and branch protection; secret scanning; dependency and code scanning; role-based permissions; separate public/private data storage; least-privilege service credentials; encryption; retention schedules; independent review; CI policy checks; deployment rollback; incident reporting.

## Landry Signé source register
See [public scholarship registry](../Institutional-Source-Registry/LANDRY_SIGNE_PUBLIC_RESEARCH.md). Any future Thunderbird learning-lab contributions must be classified by rights and access before publication or ingestion.

**Limit:** This policy is a written control specification. Actual enforcement requires code, CI tests, deployment configuration, and an evidence-backed audit. Legal ownership or license disputes require qualified legal review.
