# GRI Global Mobility Evidence Program — protocol v0.1
Date: 2026-10-24 | Research only | Public-source and consent-based evidence

## Objective
Connect (1) platform engineering and pricing disclosures, (2) legal and institutional rules, and (3) first-person driver experiences to test falsifiable hypotheses about algorithmic management, agentic automation, income, autonomy and accountability. The unit of evidence is a source-specific observation, not a presumed fact about internal algorithms.

## Seeded source register (retrieved October 24, 2026)
| Source | URL | Evidence class | Research use |
|---|---|---|---|
| Uber 2026 US Algorithmic Transparency Report | https://tb-static.uber.com/prod/uber-static/uber-sites/_pdf/ai-on-uber/US-Algorithmic-Transparency-2026.pdf | Corporate institutional disclosure | Stated pricing, matching and AI practices; self-reported |
| Uber marketplace pricing | https://www.uber.com/us/en/marketplace/pricing/ | Corporate product documentation | Distinguish rider price from driver fare |
| Uber upfront fares help | https://help.uber.com/driving-and-delivering/article/upfront-fares?nodeId=bc83ed7e-6725-41de-afcb-72d263e5589f | Corporate product documentation | Disclosed fare factors and exceptions |
| Uber estimated earnings per active hour | https://www.uber.com/us/en/blog/piloting-estimated-earnings-per-active-hour-on-trip-requests/ | Corporate pilot disclosure | Distinguish active time from online time |
| Uber 2025 European Algorithmic Transparency Report | https://tb-static.uber.com/prod/uber-static/uber-sites/_pdf/ai-on-uber/Algorithmic_Transparency_7.pdf | Corporate institutional disclosure | Cross-market transparency comparison |
| Reddit r/uberdrivers May 2025 upfront-fare discussion | https://www.reddit.com/r/uberdrivers/comments/1kuegv2 | Public anecdotal discussion | Hypotheses on fare changes and acceptance behavior |
| Reddit r/uberdrivers Jan 2026 acceptance-rate discussion | https://www.reddit.com/r/uberdrivers/comments/1q9t602/it_has_been_beyond_liberating_to_say_f_my/ | Public anecdotal discussion | Perceived acceptance-rate incentives; not causal proof |
| Reddit r/uberdrivers Oct 2026 pricing allegation | https://www.reddit.com/r/uberdrivers/comments/1x2vf79/notice_how_ridiculous_pay_has_been_recently/ | Public anecdote with AI-generated assertions | Code separately: firsthand account vs unsupported AI explanation |
| Reddit r/uberdrivers Oct 2026 algorithm speculation | https://www.reddit.com/r/uberdrivers/comments/1wytvp3/dear_drivers_read_this_breakdown_algorithms_and/ | Unverified public speculation | Hypothesis-generation only; not evidence of internal implementation |

## Evidence ledger schema
`observation_id,source_url,source_platform,source_date,accessed_date,geography,platform_company,actor_type,claim_text_paraphrase,claim_type,firsthand_flag,documentation_flag,independent_corrob_flag,verification_status,measurement_unit,observation_window,consent_basis,license_review,redaction_status,coder_id,adjudication_status,notes`.

Permitted verification statuses: `CORPORATE_CLAIM`, `FIRSTHAND_UNVERIFIED`, `INDEPENDENTLY_CORROBORATED`, `UNVERIFIED_SPECULATION`, `REJECTED`. These do not imply equal evidence strength. Store minimum necessary quotations and source links, not bulk scraped personal profiles.

## Research design
- **Platform layer:** algorithmic fare-setting, offer cards, incentives, dispatch, support, fraud controls, autonomous vehicle integration and agentic tools.
- **Institutional layer:** company policies, public disclosures, labor and transportation rules, disputes, appeals, and changes over time and across jurisdictions.
- **Driver layer:** gross and net earnings, online vs active hours, unpaid pickup miles, operating costs, rejection decisions, deactivation experiences, trust and safety.
- **Comparisons:** same market/time/vehicle type; platform-specific contrasts; pre/post policy changes with comparison markets where feasible; clearly separate descriptive from causal findings.
- **Primary measures:** net earnings per online hour, net earnings per engaged hour, gross offer per total mile (including pickup), deadhead share, estimated-vs-actual trip time, offer acceptance and cancellations, self-reported autonomy and trust. Track denominator, currency, fuel/maintenance assumptions and uncertainty.
- **Qualitative coding:** two independent coders, disagreement adjudication, inter-rater reliability where appropriate, negative-case sampling, and documented sampling bias.
- **Hypothesis H1:** Differences between platform-disclosed earnings metrics and drivers' net earnings per online hour are material and market-dependent.
- **Hypothesis H2:** Offer information and incentive design are associated with acceptance strategy, but observational correlations cannot identify hidden personalization.
- **Hypothesis H3:** Tool-time authorization and human appeals influence whether agentic platform actions are contestable and auditable.

## Public social media and consent
Reddit, public YouTube channels, public Facebook/Instagram posts, and consenting interviews are candidate evidence streams, **not** unrestricted harvesting targets. Observe platform terms, privacy law, copyright, ethical research standards and consent requirements. Do not collect private groups, personal identifiers, faces, plates, precise routes or location histories without a defensible legal and ethical basis. Do not claim representativeness from self-selected posters. A video creator's narrative is not an independently validated trip record.

## Next reproducible deliverables
1. Collect a small purposive, documented, diverse source sample with provenance and inclusion/exclusion rules.
2. Obtain consent-based deidentified trip records and interviews, if available, to corroborate public accounts.
3. Create an independently adjudicated coding dataset with split-by-driver/market/time to prevent leakage.
4. Test preregistered metrics and report confidence intervals, sensitivity to cost assumptions, and contrary findings.
5. Connect claims about agent autonomy to the separately maintained authorization simulator, without pretending social-media posts are agent-security benchmark labels.

## Limitations
The listed sources are initial discovery examples. No systematic collection, human coding, independent replication, causal analysis or access to Uber/Lyft internal algorithms has yet occurred. Corporate statements and public allegations must remain clearly attributed.
