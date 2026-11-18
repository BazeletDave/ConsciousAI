# GRI Research Case | Microsoft Agent Framework PyPI Supply Chain Incident

**Observation date:** 2026-11-18  
**Status:** Documented external incident; GRI exposure assessment incomplete  
**Placement:** Existing AI Paradox, Black Box Paradox, and Tiger Assurance research. This is a bounded extension, not a new program.

## Scope and evidence discipline

This case examines the reported malicious publication of Microsoft Agent Framework Python package versions `1.26.1` and `1.26.2`, with an emphasis on dependency integrity, startup execution, CI identity privileges, and independent assurance. The technical details below are attributed to published security advisories and investigations, not independently reproduced malware analysis. Do not equate potential exposure with confirmed compromise.

### Confirmed and reported external facts

* GitHub Security Advisory **GHSA-764m-3ppc-5m73** and Wiz's investigation identify malicious `agent-framework` releases `1.26.1` and `1.26.2`. The releases were removed from PyPI.
* Researchers report use of Python startup mechanisms, with credential harvesting as the malicious objective. This creates exposure beyond application imports, potentially including automated Python execution in CI.
* Reported targeting of CI credentials and OIDC authority is a distinct concern from the correctness of the agent framework's application logic.
* The cause of unauthorized publication, total downstream victim count, and actual compromise of any particular consumer require separate evidence.
* A GitHub 404 screenshot is not evidence of the cause of a repository's unavailability.

**Primary sources:** [GitHub Security Advisory](https://github.com/advisories/GHSA-764m-3ppc-5m73); [Wiz technical investigation](https://www.wiz.io/blog/malicious-version-of-microsofts-agent-framework-published-to-pypi).

### Institutional context, not incident attribution

A U.S. House Homeland Security Committee hearing announced for 2026-11-18 addressed worldwide homeland threats, including AI-enabled cyber risks. The hearing's existence does **not** establish that witnesses discussed this specific PyPI incident, that the State Department testified, or that unreported closed-door international consultations occurred.

**Source:** [House Homeland Security Committee announcement](https://homeland.house.gov/2026/11/14/media-advisory-chairman-garbarino-announces-annual-worldwide-threats-hearing-2/).

## GRI-specific inspection | limited scope

Connected GitHub inspection of `BazeletDave/ConsciousAI` on 2026-11-18 returned no default-branch search matches for `agent-framework`, `1.26.1`, or `1.26.2`. Direct inspection of the Agentic Governance Engine manifest showed `fastapi>=0.115,<1`, `pydantic>=2,<3`, and `uvicorn>=0.30,<1`; Motion Classification declared `numpy>=1.24,<3` and `scikit-learn>=1.3,<2`. Neither manifest directly lists the affected package.

The `.github/workflows/gri-research-quality.yml` workflow grants `contents: read`, `id-token: write`, and `attestations: write`; it installs Motion Classification dependencies and performs research and Tiger Legacy tests and provenance attestation. OIDC capability is a review consideration, **not evidence of credential theft**.

**Limits:** Default-branch searches and two manifests do not verify transitive dependency resolution, historical CI runs, runners, caches, container images, Render, Vercel, or cloud token exposure. No assertion of full GRI safety or independent clearance is warranted. No secret rotation, runtime isolation, or deployment audit has been executed as part of this case.

## Research conclusions

1. **Publisher trust is not artifact integrity.** Trusted project identity alone cannot prove every distributed version is safe.
2. **Agent assurance extends into the build environment.** Python startup execution can bypass application-level testing assumptions.
3. **Delegated authority creates asymmetric consequences.** CI identities and cloud tokens can have broader privileges than an application agent.
4. **Provenance and security are separate predicates.** A signed artifact may establish origin and integrity without establishing that all inputs were benign.
5. **Disclosure counts are not victim counts.** Publication duration, package downloads, and exfiltration limits do not establish the number of compromised organizations.
6. **Institutional evidence is distributed.** Registries, maintainers, cloud providers, researchers, agencies, and affected operators each hold partial evidence.
7. **Functional tests are necessary but insufficient.** A passing regression suite is not proof of continuous dependency or credential integrity.

These findings extend the existing Black Box Paradox: an organization can observe successful system behavior while lacking sufficient evidence to verify the trustworthiness of the software supply chain and delegated execution authority.

## Bounded assurance follow-up

* Inventory direct and transitive dependencies across actual builds and retained CI artifacts, including historical resolution during the malicious publication window.
* Review OIDC permission scope, especially whether `id-token: write` is needed for the entire job rather than a narrower attestation context.
* Evaluate trusted dependency lock and hash verification, including approved resolution and artifact digests.
* If installation evidence appears, preserve logs and artifacts, isolate affected execution environments, assess possible credential access, and rotate exposed secrets through authorized operations.
* Reconcile evidence with existing Tiger Assurance provenance and immutable ledger controls; do not create a parallel research project.

## Publication boundary

**Approved research-level statement:** The inspected GRI default-branch source and two direct dependency manifests showed no direct reference to the affected Microsoft package; complete historical and runtime exposure verification remains open.

**Not supported:** “GRI is completely safe,” “all deployments are independently cleared,” “the whole world was compromised,” or claims about undisclosed government deliberations.

**Case classification:** External incident verified by cited researchers; GRI exposure preliminarily unobserved in inspected sources; broader deployment clearance pending.
