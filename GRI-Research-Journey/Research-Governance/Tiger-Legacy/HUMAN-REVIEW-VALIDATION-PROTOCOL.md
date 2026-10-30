# GRI AI Paradox | Prospective Human Review Validation Protocol

**Status:** Prospective research design only. No human participants recruited, enrolled, tested, or independently validated.  
**Institution:** Grand Research Institute. Independent research; no Thunderbird or ASU endorsement or ethics approval is implied.  
**Scope:** Existing Training a Tiger, Tiger Assurance, and Tiger Legacy research. Synthetic scenarios only.

## Research question

When a governed AI workflow encounters missing, contradictory, or misleading observations, can actual human reviewers improve the correctness and accountability of final decisions without disproportionate delays, unnecessary holds, or unreviewable discretion?

## Hypotheses

H1: Reviewers given explicit authority and evidence provenance instructions have fewer unsafe approvals than reviewers given only a task outcome summary.  
H2: Reviewers receiving conflicting evidence are more likely to hold or escalate than those receiving apparently consistent evidence, but may increase false holds.  
H3: Review quality declines under workload or time pressure, subject to ethical and prospective controls.  
Null: No difference, or worse performance, under additional governance procedures.

## Study design requiring ethics clearance before enrollment

A preregistered, randomized, blinded, controlled study with consenting adult participants. Use a factorial or balanced crossover design with order counterbalancing and case level randomization. Predeclare sample size through power analysis based on pilot variance; do not infer adequate sample size from the current Monte Carlo assignments. No real users, clients, private documents, accounts, security incidents, or production access.

Compare two reviewer interfaces:
1. Standard synthetic task decision package with the information normally available in the fixture.
2. Governance enriched package with scoped authority, consent status, provenance, observation disagreements, escalation rules and a clear review record.

Use independent synthetic scenario construction and adjudication before assigning cases to participants. Include safe tasks, concealed hazards, common cause sensor failure, forged authority claims, expired or revoked consent, false positive alarms, and ambiguous cases with an explicitly documented adjudication policy. Randomize condition order and record reviewer familiarity, training, and task difficulty without collecting unnecessary personal information.

## Reviewer procedure

1. Provide plain language study information, voluntary consent, withdrawal and data handling terms before participation.
2. Train participants on the synthetic setting, allowed actions, escalation, and the meaning of evidence uncertainty. Require a comprehension check.
3. Present randomized cases without disclosing synthetic ground truth.
4. Require a decision: approve, deny, request more evidence, or escalate; record rationale, evidence relied on, authority checked and confidence.
5. Record task duration and any requested evidence. Do not impose unsafe stress or deceptive real world consequences.
6. Debrief participants and offer a withdrawal mechanism consistent with the approved protocol.

## Primary outcomes

Unsafe approval rate: approval of a case adjudicated as unauthorized or hazardous, divided by all such assigned cases.  
Unnecessary denial rate: denial of adjudicated legitimate cases divided by legitimate assigned cases.  
Escalation appropriateness: escalation of ambiguous or conflicting cases using preregistered adjudication criteria.  
Decision quality: agreement with independently adjudicated case labels, with ambiguous cases analyzed separately.  
Review latency and effort: observed time, additional evidence requests, and reviewer burden.  
Interrater agreement: report a suitable agreement statistic and uncertainty interval where sample size permits.

Use participant clustered inference for repeated decisions, and report intention to analyze, exclusions, attrition, subgroup exploratory limits, and missing data. Do not conflate an algorithmic simulation with a human reviewer.

## Institutional cost accounting

Predeclare valuation ranges rather than treating hypothetical shadow prices as measured facts. Capture reviewer labor time, escalation burden, false hold delay, unnecessary intervention cost, and consequences of missed hazards. Analyze cost effectiveness as incremental net value and report break even thresholds under low, central and high valuations. Include stakeholder distribution: who bears false holds, who bears hazards, and who benefits from intervention. Treat rare severe harm as a scenario sensitivity rather than a reliably estimated frequency from small experiments.

## Ethics and authorization gate

Before recruiting, obtain a documented determination from the appropriate qualified ethics review authority as to whether the project requires IRB review or exemption; secure any required approvals, consent materials, retention schedule, access controls and withdrawal procedure. Independent GRI research does not automatically inherit university IRB oversight. Recruitment or data collection must not begin until the applicable determination and approvals are documented. No automatic recruitment, outreach or participant contact is authorized by this protocol.

## Data management and reproducibility

Use participant pseudonyms, separate consent records from study responses, encrypt access restricted records, and specify retention and deletion schedules before collection. Publish only approved aggregate or synthetic data. Freeze scenarios, labels, randomization seed, statistical analysis plan and code hashes before first enrollment. Preserve unfavorable findings and reviewer disagreements. Make a redacted reproduction package available for controlled external review under GRI confidentiality rules.

## Execution status and next gates

**Protocol drafted, no human study executed.** Next gates: independent case adjudication and pilot materials; ethics determination and power analysis; recruitment authorization; actual study execution; blinded analysis; independent methodological review. The original Monte Carlo findings remain synthetic and unaltered.
