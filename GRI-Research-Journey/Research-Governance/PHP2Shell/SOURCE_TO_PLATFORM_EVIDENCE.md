# PHP2Shell | Source to Platform Evidence Mapping

Grand Research Institute | 21 October 2026 | Research working case

## Evidence classification
* **Vendor confirmed:** PHP upstream security advisory and patched release.
* **Operator reported:** A platform operator's own mitigation or service status statement.
* **Reported:** Independent news or national advisory describing operational impact.
* **Hypothesis:** A technical or institutional inference not independently validated.

## How it happened

### CVE-2026-109618: out of memory corruption
**Vendor confirmed:** PHP uses `longjmp()` to abort requests following out of memory failures. Under some initialization sequences, request memory can be reachable before full initialization; subsequent request shutdown can access invalid state. Multipart parsing can contribute to controllable allocation pressure. The upstream advisory states that this can lead to unauthenticated remote code execution. Do not equate this with a proven double free in every execution path.

Primary source: https://github.com/php/php-src/security/advisories/GHSA-w8hw-w9fx-j79w

### CVE-2026-109619: stale global state
**Vendor confirmed:** PHP identifies a stale global state issue that can lead to remote code execution, classified in part as use after free (CWE-416), improper exceptional condition handling and uninitialized pointer access. **Research hypothesis:** Persistent worker reuse can propagate the consequence across requests; the precise call path and triggering conditions must be verified from upstream source commits and regression tests.

Primary source: https://github.com/php/php-src/security/advisories/GHSA-6wmf-4rv5-p3rp

## What happened
PHP published patched upstream versions 8.2.35, 8.3.36, 8.4.27 and 8.5.12 on 21 October 2026. PHP explicitly cautions that no configuration or edge filtering approach is a complete mitigation. Patch installation and active worker verification remain the defensive baseline.

Release record: https://github.com/php/php-src/releases

## What it impacts and where

| Platform or sector | Dependency or response pathway | Evidence status | Do not infer |
| --- | --- | --- | --- |
| PHP core / Zend | Shared runtime vulnerability | Vendor confirmed | All installations exploited |
| WordPress, Drupal, Joomla | Dependent applications running on PHP | Architectural exposure | Vendor compromise or universal exploitability |
| PHP-FPM, Apache mod_php, LiteSpeed, FrankenPHP | Web serving deployment surfaces | Runtime applicability; deployment specific | Identical exploit preconditions |
| Managed WordPress hosting | Centralized operator runtime remediation | Requires individual operator evidence | Every customer installation verified |
| Cloudflare / WAF | Possible partial edge filtering | Defensive control, not full mitigation | Protection equivalent to patching |
| Public sector and self hosting | Patch coordination, service continuity | Institution specific evidence required | Confirmed compromise from shutdown alone |

## Where we go from here
1. Locate exact upstream PHP remediation commits for each maintained branch and document changed functions and associated regression tests.
2. Distinguish source confirmed behavior from inference about exploit prerequisites, request lifecycle and cross tenant effects.
3. Inventory PHP dependencies, image digests, vendor backports and worker versions using the offline `php_case_study.py` utility.
4. Record responsible owner, patch authorization, deployment time, restart or redeployment evidence and active runtime validation.
5. Build a comparative institutional dataset with discovery, disclosure, authorization, remediation and verification timestamps.
6. Analyze institutional response through the Nelson Model: rules, actors, interests, power, options, commitments and adaptation.

## Safe reproducibility
```bash
python3 -m unittest test_php_case_study.py
python3 php_case_study.py sample_inventory.json --report case_study_report.md
```
The tool screens operator supplied JSON only. It does not probe infrastructure, establish exploitability, or validate compromise. Sample assets are synthetic.

## Research limitations
This file is an evidence mapping, **not** a completed line by line upstream patch audit. Do not represent generalized claims about WAF bypass, cross tenant exposure, heap control flow hijacking, or specific platform compromise as confirmed without reproducible evidence. The original user supplied technical narrative is retained as a research hypothesis where source validation is outstanding.
