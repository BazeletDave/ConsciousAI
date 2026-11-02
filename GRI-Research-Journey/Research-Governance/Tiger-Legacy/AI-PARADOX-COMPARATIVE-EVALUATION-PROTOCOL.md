# GRI AI Paradox | Controlled Comparative Evaluation Protocol

**Research owner:** Grand Research Institute | Independent research led by David A. Grand  
**Authorization:** GRI authorized a limited research extension on 30 October 2026. This document is a prospective protocol, not experimental findings or authorization for deployment.  
**Scope:** Existing Training a Tiger, Tiger Assurance and Tiger Legacy research only. Synthetic data and offline evaluation. No changes to frozen experiments, operational dashboard, production systems, clients, or confidential review records.

## Institutional question

Can explicit authority boundaries, revocation, independent observation and human review reduce unauthorized or harmful outcomes in a controlled algorithmic task while retaining useful task performance? The AI Paradox is tested as the divergence between locally compliant automated behavior and institutionally legitimate outcomes, not presumed as an empirical fact.

## Existing evidence and separation

1. [Training a Tiger independent assurance experiment](../../Algorithmic-Management/Training-a-Tiger-AI-Paradox/Implementation/Assurance-Experiment/README.md) documents strong hidden-friction detection **when probes are trustworthy**, failure under biased probes, and the gap between local recovery validation and task completion. These are historical synthetic findings and must not be rewritten or generalized to cybersecurity.
2. [Tiger Legacy research methods and results](RESEARCH-METHODS-AND-RESULTS.md) documents synthetic authorization, consent, ledger integrity and adversarial fixture tests. These are not production security certifications.
3. [Nelson institutional methodological boundaries](../../Integrated-Research-Journey/nelson-model-methodological-boundaries.md) guide interpretation of actors, interests, power, rules, legitimacy and institutional capacity. The political economy lens is not a model performance score.

## Prospective paired design

Compare the same seeded synthetic task cases and identical model or rule outputs under two governance conditions:

* **Baseline:** existing task execution policy and locally available validation, without the additional independent authorization and observation gate being evaluated.
* **Governed:** same task outputs and task budget, with explicit scoped authorization, expiry and revocation checks, independently measured observation where available, and human review required before consequential exceptions.

Record additional probes, latency proxies, reviewer effort and rejected work as governance costs. If the governed condition receives extra information or intervention opportunities, report this explicitly and do **not** attribute improvements solely to better intelligence or identical resource budgets. No live human review is presumed: a synthetic review oracle must be labeled as such.

## Outcomes and falsifiable hypotheses

* **Primary:** unauthorized action allowance rate, denominator all attempted actions without valid authorization; separately report false denials of valid actions.
* **Primary:** severe hidden-change allowance rate, denominator all assigned severe hidden-change cases; stratify by trustworthy, missing and biased observations.
* **Secondary:** completed legitimate task rate, intervention and unnecessary hold rates, revocation enforcement, event-chain integrity, recovery completion on assigned cases, and resource or latency overhead.
* **H1:** governed authorization reduces unauthorized allowances relative to baseline on the declared fixtures.
* **H2:** independent observation reduces severe hidden-change allowances only when measurement assumptions hold.
* **H3:** locally passing recovery or evidence checks do not necessarily establish successful end-to-end task outcomes.
* **Null:** differences may be zero, negative, or limited to synthetic assumptions. A failed hypothesis is a publishable research result.

## Method and evaluation controls

Use versioned deterministic fixtures, paired seeds, a frozen pre-execution protocol, positive and negative controls, deliberately biased or absent observations, expired and revoked grants, cross-tenant attempts, tampering and truncation. Retain fixture hashes, code revision, environment, test outputs and exact denominators. Report uncertainty intervals when repeated seeds permit them; otherwise report descriptive counts only. Distinguish case assignments from independent units. Separate author-run checks from independently reproduced results. Document failures and unmeasured dimensions rather than adjusting success criteria after observation.

## Institutional interpretation

Map each failure to (a) human intent and competing interests, (b) institutional authority and permission, (c) algorithmic execution, (d) observed consequence, and (e) contestability, correction and accountability. Explicitly distinguish malicious misuse, mistaken authorization, sensor or specification failure, and institutional incentive misalignment. These categories may overlap and are not assumed causal without evidence.

## Stop conditions and publication gates

Stop the comparative run if fixtures unexpectedly contain real client data, secrets, personally identifying material or operational credentials; if execution would touch live services; or if a proposed change modifies frozen historical evidence. Never grant autonomous operational control. Before publication, confirm reproducibility, review limitations and approve only public metadata and nonconfidential results. GRI's internal decisions, reviewer identities and proprietary evidence remain confidential. External academic researchers may request controlled private verification under the [existing policy](../ConsciousAI-Research-Systems/CONFIDENTIAL-REVIEW-RECONCILIATION.md).

## Next controlled evaluation: Training a Tiger and Tiger Legacy

This authorized extension retains the frozen Training a Tiger findings unchanged. Its independent observation gate detected severe hidden friction under trustworthy measurements, but failed when probes were biased. Its local recovery validation passed approximately 99.7 percent of recovery attempts while counterfactual task success was approximately 21.4 percent of assigned hidden shift cases. These findings motivate new evaluation criteria; they are not cybersecurity performance estimates.

The next comparison will use the same deterministic synthetic inputs for baseline and governed conditions. It will measure unauthorized action allowance, false denial of valid actions, detection of modified evidence, recovery completeness, legitimate task completion, and additional intervention costs. Negative controls must include valid authorization, absent or biased observations, and locally valid recovery that fails the full task objective.

Before execution, freeze the source revision, fixtures, expected outcomes, metrics and decision thresholds. Retain exact denominators, environment, logs, deviations and a reproducible result digest. Distinguish developer-run checks from independent external reproduction. Do not modify original experiment archives, expose private information, access live systems or claim operational effectiveness.

**Status:** Experimental design specified; execution and independent validation not yet demonstrated.

## First executed paired synthetic fixture | 1 November 2026

**Exact evaluated revision:** `9894cfc7e13aee290475e14f7907339460d07742`, draft PR #97. **Evidence:** GitHub Actions GRI Research Quality Gate run [41369930495](https://github.com/BazeletDave/ConsciousAI/actions/runs/41369930495), successful; Research Rights and Security Checks run [41369930578](https://github.com/BazeletDave/ConsciousAI/actions/runs/41369930578), successful. The quality gate log reports **75 Tiger Legacy tests passed**, including `test_paired_synthetic_authorization_outcomes`, and successful release evidence reproduction and signed provenance verification.

**Paired fixture design:** Five fixed authorization attempts were evaluated in two conditions: (A) an intentionally permissive `allow all` synthetic baseline, and (B) the existing Tiger Legacy scoped authorization engine. Two attempts were authorized by fixture ground truth and three were unauthorized. The test asserts the following fixture outcomes:

| Condition | Unauthorized allowed / unauthorized attempts | False denials / authorized attempts |
| --- | --- | --- |
| Permissive synthetic baseline | 3 / 3 | 0 / 2 |
| Scoped Tiger Legacy policy | 0 / 3 | 0 / 2 |

**Interpretation:** These are deterministic, developer-defined fixtures and test assertions, **not** estimated real-world rates, model training effects, or an independent scientific replication. The deliberately weak baseline demonstrates that scoped authorization distinguishes these enumerated cases; it is not a representative comparison with the historical Training a Tiger learner. Evidence integrity, biased sensor reliability, full-task recovery and statistical generalization are not established by this paired test. The original Training a Tiger data and results were not modified.

**Remaining gate:** Independent reproduction by a separate reviewer, broader preregistered fixtures and complete outcome measurements before strengthening external efficacy claims. This documentation entry does not replace a fresh quality gate on subsequent commits.

## Status and next gate

**Protocol drafted; experiment not yet executed under this protocol.** Next gate: inspect existing synthetic fixtures and identify the smallest reusable paired comparison without changing deployed interfaces. Obtain separate authorization before any operational integration, material architectural change, new spending or release of restricted material.


## GRI Tiger Legacy | Reproducible Assurance Milestone | 1 November 2026

**Milestone designation:** Reproducible Assurance Milestone. This dated entry supersedes earlier prospective status statements above only with respect to the completed synthetic fixture and automated verification gates. The research remains bounded to Tiger Legacy Version One.

**Executed evidence:** The paired synthetic authorization fixture was verified in GitHub CI at the exact revision and run recorded above. A subsequent research branch revision, `57a8a0c6f81e573d1dde45b5aa1bbd0856b9d960`, introduced the reusable `.github/workflows/tiger-legacy-isolated-reproduction.yml` workflow. [Isolated reproduction run 41370731900](https://github.com/BazeletDave/ConsciousAI/actions/runs/41370731900) completed successfully in a Python 3.11 container, including the test execution, environment capture, SHA256 manifest generation and artifact upload. The [Research Rights and Security Checks run 41370731779](https://github.com/BazeletDave/ConsciousAI/actions/runs/41370731779) also succeeded. The GRI Research Quality Gate run 41370731718 was still in progress when last inspected; do not infer its final result from this entry.

**Preserved evidence:** GitHub Actions artifact `tiger-legacy-reproduction-d4249cb5ccfc7843a57b82582fc0e4457fecd17e`, artifact ID `13108213946`, was reported uploaded with SHA256 digest `9496971c92392583e76844c60678c2e458f74524de5264917c4f39cd07f52de4`. The run metadata reports head SHA `57a8a0c6f81e573d1dde45b5aa1bbd0856b9d960`. The exact per-test count for this container run must be confirmed from its archived test log before making a count-specific claim.

**Independent assessment:** An independent reviewer (iR) supplied a methodological assessment classifying the earlier `906554f1e7200e72ed17bd3b8d53fc8420227c57` evidence as **Provisionally Verified (CI-Level) | Pending Clean-Room Execution**. The review was based on CI and documentation, not a documented third-party execution. The new successful isolated CI run is a separate engineering achievement and must not be described as independently executed by iR or as a clean-room execution of the exact older commit. Confidential reviewer identity and records remain outside the public repository.

**Assurance boundary:** Passing synthetic authorization and regression checks does not establish real-world cybersecurity efficacy, unbiased observations, end-to-end recovery, statistical generalizability, or production readiness. PR #97 remains subject to ordinary review and merge controls. Future sign-off requires independent reviewer reconciliation of the exact revision, container evidence and baseline CI logs, followed by separately designed outcome evaluations.

**Institutional significance:** GRI now has a reusable isolated test and evidence capture mechanism supporting transparent, bounded verification without exposing confidential client data or proprietary assessment records. This milestone records reproducibility infrastructure, not independent scientific certification.
