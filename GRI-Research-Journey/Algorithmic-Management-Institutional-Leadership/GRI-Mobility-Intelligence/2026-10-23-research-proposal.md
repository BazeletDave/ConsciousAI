# GRI Mobility Intelligence: A Human-Centered, Constraint-Aware Decision System for Ridehail Drivers and Working Students

**Grand Research Institute | Research proposal v0.1 | 23 October 2026**
**Status:** Proposed research and software prototype; not a validated or deployed service.
**Research independence:** Independent GRI research, not sponsored, endorsed, or operated by Uber, Lyft, or Thunderbird.

## Abstract
This project proposes a driver-controlled decision-support platform combining operations research, predictive modeling, and institutional governance to help ridehail drivers—including working students—allocate limited driving hours while protecting sleep, coursework, class attendance, safety, and personal commitments. Rather than maximizing gross fares or trip volume, the system seeks to maximize risk-adjusted net economic contribution subject to hard time and fatigue constraints. A Boca Raton–Miami Beach Friday evening scenario illustrates an itinerary with a potential southbound paid trip, a bounded South Beach service interval, and a return north before a driver-selected cutoff. The prototype will initially use manually entered offers, consented historical records, and explicitly simulated scenarios; it will not assume access to platform dispatch, ride requests, or passenger data.

## 1. Research question
Can personalized, explainable, constraint-aware decision support improve realized net earnings per available hour and schedule adherence compared with drivers' ordinary planning, without increasing fatigue or undermining educational obligations?

Secondary questions: Which forecasts are reliable enough to improve decisions? How do platform rules, asymmetric information, and driver autonomy shape the value of recommendations? Can a model fairly serve drivers with different resources, needs, and risk tolerance?

## 2. Institutional and scholarly foundation
Apply Roy C. Nelson's institutional political-economy teaching as a methodological lens: rules, actors, incentives, authority, implementation, contestability, and adaptation. This is GRI's independent application, not a faculty-endorsed or native Nelson AI model. Connect David Slocum's leadership and human-centered organizational adaptation, Lena Booth's financial value creation and opportunity costs, and Mansour Javidan's communication, trust, and negotiation research only where analytically warranted. Maintain course-specific academic integrity requirements. Place algorithmic management, platform labor, mobility policy, and the move toward agentic management in comparative context.

## 3. Decision problem and mathematical formulation
For candidate action sequence x over time horizon T, maximize:
**E[net revenue(x)] - λ·downside_risk(x) - μ·unpaid_repositioning(x) - ν·schedule_disruption(x)**

Subject to hard constraints:
- Driver-approved start and end times, return-home location, class/study blocks, and maximum duty duration.
- Minimum sleep opportunity before the next commitment, defined by the driver and informed by safety guidance, with no recommendation to drive when fatigued.
- Legal and platform compliance, no prohibited dispatch manipulation or unauthorized automation.
- Geographic feasibility and realistic uncertainty in travel times, wait times, return-trip availability, tolls, and expenses.
- Explicit ability to choose **do not drive** when feasible earnings do not justify the costs or risks.

Do not interpret a route recommendation as a guaranteed ride or fare. Distinguish contribution margin from take-home pay and taxes.

## 4. Illustrative Friday-night scenario
**Starting area:** Boca Raton, Florida.
**Candidate market:** Miami Beach / South Beach.
**Possible pattern:** Evaluate a southbound paid offer; optionally service local demand for a driver-selected window; compare return north at approximately 12:01 a.m. versus 2:00 a.m.; preserve sufficient time for the next day's class and sleep. The user's mention of five evening rides is a scenario target, not a predicted or guaranteed number of bookings.

Candidate strategies: A) remain local; B) travel south only with an acceptable paid offer; C) travel south including an unpaid repositioning leg; D) terminate early and return; E) do not drive. Evaluate with a travel-time range and probability distribution for offers rather than fabricated real-time demand. Late-night travel and fatigue risks must be treated as decision constraints, not simply costs to trade away.

## 5. Proposed system architecture
1. **Driver profile and consent:** hourly/weekly goals, vehicle expense model, tolls, schedule, study commitments, return deadline, sleep buffer, accessibility and personal preferences; encrypted, minimal data collection.
2. **Offer and trip ledger:** user-entered or expressly authorized records with timestamps, gross fare, tips, incentives, pickup/deadhead distance, active and idle time, expenses, location at appropriate privacy granularity, provenance.
3. **Forecasting layer:** calibrated probabilistic predictions for hourly demand proxies, idle time, travel time, and net contribution, with missing-data fallbacks and out-of-distribution warnings. Do not claim the model predicts Uber's proprietary dispatch decisions.
4. **Constraint optimizer:** start with deterministic rules and scenario enumeration; later time-dependent shortest path, mixed-integer programming, or stochastic optimization where justified.
5. **Explanation engine:** compare alternatives, show uncertainty intervals, identify binding constraints, explain the no-drive option.
6. **Audit and governance:** model/data versions, driver overrides, recommendation outcomes, errors, consent withdrawal, safety review, and reproducibility.

## 6. Development stages
**M0 — Governance and specification:** define data dictionary, prohibited integrations, consent, security, privacy, safety thresholds, acceptance criteria.
**M1 — Working rules-based MVP:** offline web dashboard/CLI, user-input scenarios, trip economics calculator, calendar blocks, return deadline, no-drive recommendation, CSV import/export, unit tests.
**M2 — Research dataset:** collect voluntary driver records with explicit provenance and consent; clean, de-identify, document selection bias.
**M3 — Machine-learning baseline:** compare simple historical averages with gradient-boosted or regression forecasts; temporal splits, calibration, MAE and uncertainty coverage.
**M4 — Route/shift optimizer:** scenario planning under time, fatigue and earnings constraints; test against rules-based baseline.
**M5 — Pilot and paper:** consented within-driver evaluation, predeclared outcomes, safety monitoring, error analysis, limitations and reproducibility appendix.
**M6 — Optional authorized integrations:** calendar or mapping interfaces and ridehail platform APIs only where available, permitted, and properly authorized. No credential scraping, automated acceptance, dispatch interference, or bypassing terms.

## 7. Evaluation plan
Primary endpoints: net contribution per total committed hour, missed return deadlines, and compliance with sleep/class blocks. Secondary: unpaid mileage, variance of realized earnings, prediction calibration, recommendation acceptance, driver satisfaction, and subgroup performance. Compare against driver-selected baseline and simple heuristics; use matched conditions or prospective crossover where feasible. Report confidence intervals and negative results. Protect against confounding from weather, events, incentives, and platform policy changes. No causal improvement claim before prospective testing.

## 8. Safety, privacy, and ethical boundaries
Fatigue and legal restrictions are hard exclusions. Avoid encouraging dangerous overnight shifts, distracted interaction while driving, or financial pressure to override sleep. Do not collect passenger identity or precise passenger destinations without lawful necessity and consent. No unauthorized Uber/Lyft access; user-provided screenshots and manually recorded offers remain attributed and permission-scoped. Do not imply employment, sponsorship, platform approval, or academic endorsement. Driver controls all recommendations and can reject them. A student-focused variant must not require disclosure of sensitive educational records.

## 9. Research deliverables
- A versioned technical specification and architecture diagram.
- An open, reproducible rules-based prototype with test fixtures clearly labeled synthetic.
- An opt-in trip-data schema and provenance ledger.
- Baseline and ML forecasting notebooks/scripts, model cards, fairness and safety tests.
- A research paper with methodology, empirical results only when measured, limitations, and comparative institutional analysis.
- A demonstration linking the project's driver economics to GRI's broader algorithmic and agentic management research.

## 10. Initial acceptance criteria
- The MVP rejects itineraries that violate a return deadline, study/class block, duty-time limit, or required sleep opportunity.
- The MVP offers a no-drive alternative and displays net rather than only gross economics.
- All predicted demand and trip outcomes are clearly labeled estimates with uncertainty.
- No production platform credentials or passenger-identifying data are required.
- Tests cover impossible itineraries, zero rides, unexpected tolls, long deadhead miles, delayed return, and forecast failure.
- Every empirical assertion in subsequent papers links to auditable evidence.

## 11. Limitations and next research questions
Platform offer allocation is proprietary and partially observable. A small volunteer sample cannot represent all drivers or cities. Self-selection, demand seasonality, and unmeasured expenses may bias estimates. This proposal specifies a research program and engineering roadmap; it does not demonstrate economic or safety benefit yet.

## 12. Immediate GitHub work packages
See linked repository issues for (1) MVP specification and safeguards, (2) data model and validation, and (3) forecasting/optimization evaluation. Sequence implementation behind M0 governance gates.

---
**Research positioning:** This project complements the GRI integrative manuscript *From Algorithmic Management to Agentic Enterprise* and the existing Uber/Lyft research instruments. The Boca Raton–Miami Beach route is a hypothetical planning case, not a claim of actual Friday-night demand or live ride availability.
