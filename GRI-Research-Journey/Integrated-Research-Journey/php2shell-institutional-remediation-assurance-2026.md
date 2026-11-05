# November 2026 | PHP2Shell: open patches, institutional remediation, and independent assurance

**Placement:** Bounded extension of existing GRI Integrated Research Journey, AI Paradox, institutional governance and Tiger Assurance. No new research program. **Evidence maturity:** primary advisory verified; GRI vulnerability-specific reproduction pending.

## Research question and answer

Does the availability of an openly distributed security patch ensure timely institutional remediation and independently verified protection? **No.** Open access to source and fixes is necessary but insufficient: administrators must discover affected assets, deploy compatible updates, restart workers, test production configurations, and independently verify closure. This is an institutional capacity question, not evidence of intentional infection or deliberate withholding by PHP maintainers.

## Primary evidence

1. PHP Security Team advisory (21 October 2026): https://www.php.net/archive/2026.php#2026-10-21-5 ; https://www.php.net/
2. PHP 8.4.27 release announcement and source checksums: https://news-web.php.net/php.announce/512
3. CERT EU advisory 2026-018: https://cert.europa.eu/publications/security-advisories/2026-018
4. CISA emergency patch bulletin (21 October 2026): https://content.govdelivery.com/accounts/USDHSCISA/bulletins/42ff5ac
5. NCSC Netherlands affected-product inventory (updated 4 November 2026): https://github.com/NCSC-NL/php2shell
6. Third-party nonweaponized condition verification laboratory (independent claims require GRI reproduction): https://github.com/rdwr-namikb/php2shell-cve-2026-109618-109619-lab

## Technical finding and remedy

* CVE-2026-109618: out-of-memory request initialization and cleanup memory corruption.
* CVE-2026-109619: stale request-owned global state and use-after-free.
* Corrected versions: PHP 8.2.35, 8.3.36, 8.4.27, 8.5.12. Older supported-branch releases are affected; legacy deployments require a supported upgrade or verified vendor backport.
* Only patched runtime software constitutes complete remediation for these CVEs. Emergency settings, including disabling session upload progress and reducing upload exposure, are **partial mitigations**, not proof of closure.
* A third issue, CVE-2026-115560, was disclosed separately on October 23 and must not be conflated with the two October 21 fixes.

## Falsifiable GRI hypotheses

H1: The interval from public patch availability to independently verified closure exceeds the interval from disclosure to public exploit awareness in a meaningful subset of institutions.

H2: Software supply-chain visibility, staffing, service availability constraints, and legacy vendor dependencies explain variance in verified remediation latency better than patch availability alone.

H3: A structured, evidence-linked assurance pipeline reduces false declarations of remediation compared with self-reported patch status.

These hypotheses are **not GRI validated findings**. The NCSC-NL product inventory is a changing observational source and not a representative sample of all PHP installations.

## Bounded engineering protocol and acceptance criteria

1. Pin source advisory versions, dates, CVEs, release tarball hashes, exact PHP SAPI and build options. Preserve checksums and a reproducible execution manifest.
2. Run isolated disposable PHP 8.4.26 and 8.4.27 environments, with no public service exposure or third-party targets. The existing GitHub Actions matrix checks benign runtime behavior only; **it is not a vulnerability reproduction**.
3. Review the third-party nonweaponized condition-verification laboratory for license, scope, safety, exact test behavior and prerequisites. Independently implement or reproduce *nonweaponized* condition checks in the isolated lab; preserve stdout/stderr, exit status, environment, exact commit and toolchain.
4. Acceptance requires vulnerable-condition evidence on the affected build, absence of that condition on the patched build, repeat runs, negative controls, and no evidence of test-harness artifacts explaining the difference. Full RCE is not required and must not be inferred from condition verification.
5. Conduct an independent clean-room replay of the evidence. Distinguish vendor-confirmed fix, GRI-observed behavior, and external reproduction.
6. Expose dashboard states: source_verified, runtime_matrix_passed, vulnerable_condition_reproduced, patched_condition_absent, independent_reproduction_verified. Every state requires linked evidence and an explicit unknown or pending value when not demonstrated.

## Existing system boundaries

The live GRI dashboard deploys from BazeletDave/ConsciousAI via Render auto-deploy. The previously committed PHP assurance bridge is read-only and currently reports synthetic checks and pending CVE reproduction. **Do not promote a case to independently verified based on documentation, version checks, generic smoke tests, or workflow configuration alone.** Preserve Tiger Legacy's existing independent review freeze and do not disclose restricted client relationships.

## Governance interpretation

The observable paradox is not that source code is closed. It is that public disclosure and open patches can move faster than institutional asset discovery, deployment, continuity decisions, and evidence-backed closure. The causal magnitude remains to be measured.
