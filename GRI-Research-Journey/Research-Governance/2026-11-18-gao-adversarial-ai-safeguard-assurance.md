# GRI Research Evidence | GAO Covert AI Safeguard Testing (2026)

**Source publication:** October 16, 2026; **public release:** November 18, 2026  
**Classification:** Independent federal performance audit; externally verified findings, not GRI-reproduced tests  
**Placement:** Existing Accelerating AI Governance Paradox, Black Box Paradox, and Tiger Assurance research; bounded evidence extension, not a new project.

## Primary evidence

The U.S. Government Accountability Office (GAO), *Artificial Intelligence: Covert Testing Used Common Platforms to Create Viable Attack Plans*, GAO-27-108814, evaluated four widely used generative AI platforms (ChatGPT, Claude, Gemini, and Grok) in spring 2026. Two were assigned a mass-casualty explosives scenario and two an electrical-grid disruption scenario. The report anonymizes platform-to-scenario mappings as A–D.

In all four tests, safeguards activated, including refusals or subsequent content/account restrictions. Investigators nevertheless obtained information assessed as viable for facilitating the assigned malicious scenario, within fewer than 12 hours per platform. GAO used documentary checks, safe field verification and subject-matter experts; it did **not** conduct real attacks. The report notes that the underlying information was generally not novel, but AI compressed synthesis into hours rather than weeks or months.

**Primary source:** https://www.gao.gov/products/gao-27-108814  
**Full report and methodology:** https://files.gao.gov/reports/GAO-27-108814/index.html

## Evidence boundaries and countervailing detail

* This was a bounded test of four platforms, assigned different scenarios; it is **not** a controlled comparative ranking of their overall safety.
* The platforms initially rejected GAO's prepared prompts; successful bypasses followed iterative interactions. Initial safeguard activation is not evidence of sustained resistance.
* GAO reports some inaccurate or hallucinated outputs, including a proposed event date that did not correspond to an event. The report's viability judgment does not mean every detail was correct.
* The findings do not establish that any real-world attack occurred, that every version or subscription tier remains vulnerable, or that the same prompts would work today.
* The report withheld operational details and platform identities within scenarios to limit misuse. This research note intentionally excludes attack procedures, target details and bypass recipes.
* Provider responses and subsequent mitigations should be assessed by version and date, not inferred from the 2026 test.

## Integration with existing GRI thesis

**Capability clock (C):** AI can accelerate synthesis of dispersed dual-use information; this audit supplies observed task-completion evidence for the tested versions and scenarios.

**Deployment clock (D):** The audit examined accessible commercial interfaces, not prevalence of malicious use or downstream deployment. No population-wide exposure rate can be inferred.

**Institutional assurance clock (G):** Controls activated but did not consistently withstand extended adversarial interactions. The distinction between nominal control presence and independently demonstrated resistance is measurable; the audit alone does not establish a temporal governance lag.

**Black Box Paradox:** Users and institutions may observe refusals while lacking visibility into the model's behavior across prolonged, adaptive interactions, version changes, and account tiers.

**Tiger Assurance:** Evaluate sustained adversarial robustness, escalation and monitoring, time-to-detection, post-incident correction, and independent reproduction using safe synthetic scenarios. A passing functional test or initial refusal must not be described as comprehensive security clearance.

## Bounded institutional follow-up

1. Register GAO-27-108814 as primary, dated evidence with its scenario and model-version limitations.
2. Map findings to existing assurance controls and explicitly record which controls were tested versus merely declared.
3. Define a **safe** evaluation indicator: fraction of synthetic, non-operational adversarial sessions in which controls maintain the intended refusal or escalation behavior over a fixed interaction budget.
4. Record remediation dates and independently retest when evidence is available; distinguish vendor statements from verified improvements.
5. Reconcile this case with existing supply-chain and critical-infrastructure cases as distinct failure modes, **not** as causally connected incidents.

**GRI research inference:** Control activation is not equivalent to effective, persistent control. Independent, version-specific evidence is needed to assess whether institutional assurance keeps pace with AI capability and accessibility. This remains a testable proposition, not a universal conclusion.

**Publication boundary:** Cite the GAO directly. Do not imply GRI conducted the tests, that a specific named provider was Platform A/B/C/D, or that a real attack resulted.
