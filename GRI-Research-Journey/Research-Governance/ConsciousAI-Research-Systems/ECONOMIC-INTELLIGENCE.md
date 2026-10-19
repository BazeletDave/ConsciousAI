# Global Economic and Institutional Intelligence | Nelson Model

**Research author:** David A. Grand, Grand Research Institute  
**Status:** Research framework and initial data-source registry. The economic feeds below are **not yet running**.

## Nelson model analytical framework
Apply Professor Roy C. Nelson's institutional model, informed by his Thunderbird instruction and institutional case analysis:

**Political and economic conditions → Institutions and rules → Actors and interests → Bargaining power → Managerial decisions → Adaptation.**

The managerial unit of analysis is the institutional environment, not merely the country. Record election and policy continuity risks, opposition and stakeholder interests, enforceability, coalition durability, sunk cost exposure and managerial optionality.

## Indicator families
| Domain | Candidate data series | Institutional question |
| --- | --- | --- |
| Growth | Real GDP, GDP per capita, industrial production | Where is economic activity expanding or contracting? |
| Prices and monetary policy | CPI, inflation expectations, policy rates | How do financing and purchasing conditions change? |
| Labor | Unemployment, participation, earnings, labor productivity | Who gains from automation, and who bears adjustment costs? |
| Capital and currencies | Exchange rates, investment flows, credit, debt | What constrains cross-border strategic decisions? |
| Trade and industry | Exports, imports, tariffs, supply chains | How do rules alter market access and bargaining power? |
| Energy and infrastructure | Electricity cost, reliability, energy mix | What constrains compute and AI infrastructure? |
| Governance | Regulatory predictability, political stability, enforcement capacity | Can commitments and safeguards endure institutional change? |
| AI and digital economy | Compute infrastructure, digital adoption, labor displacement studies | What is the difference between technical capability and institutional authority? |

## Candidate official and licensed sources
- [IMF Data](https://www.imf.org/en/Data) and [IMF SDMX APIs](https://data.imf.org/): international macroeconomic datasets; dataset and licensing verification required.
- [World Bank Indicators API](https://api.worldbank.org/v2/): development indicators and historical series.
- [OECD SDMX API](https://sdmx.oecd.org/): member and partner economies; confirm current dataflow identifiers.
- [ILO ILOSTAT](https://ilostat.ilo.org/data/): labor market statistics.
- [BIS statistics](https://www.bis.org/statistics/): credit, banking and monetary data.
- [FRED API](https://fred.stlouisfed.org/docs/api/fred/): U.S. and international economic time series; API key required.
- [UNCTADstat](https://unctadstat.unctad.org/): trade and investment.
- [Eurostat API](https://ec.europa.eu/eurostat/web/main/data/database): EU statistical series.
- [ASEANstats](https://www.aseanstats.org/): regional indicators.
- Economist Intelligence Unit country risk forecasts: **licensed source**, not assumed freely accessible.

These are source candidates, not proof of operational integration or of any specific recent data value.

## Data contracts
Every observation should preserve `indicator_id`, `geography`, `unit`, `value`, `observation_period`, `published_at`, `retrieved_at`, `source_url`, `dataset_id`, `frequency`, `vintage`, `revision_status` and `verification_status`.

Distinguish (a) official observation, (b) forecast, (c) GRI calculation, (d) inferred relationship, and (e) scenario. Do not present stale observations as live measurements. Retain revised values as historical vintages where available.

## Cross-layer research queries
- Does increased enterprise agent adoption coincide with labor productivity, wages, or employment changes? Do not infer causality from co-movement.
- How do changes in interest rates, electricity prices and currency conditions affect AI infrastructure investment decisions?
- How do political coalitions and institutional durability alter implementation of AI regulation?
- How do platform earnings observations compare with official wage and cost-of-living benchmarks, with gross versus net and observed versus hypothetical amounts distinguished?
- How do IMF, ASEAN, EU, U.S. and Indian policy events relate to contemporaneous economic indicators and institutional risk?

## Roadmap
1. Confirm access and stable API contracts for individual official series.
2. Build scheduled collectors with per-source freshness and failure monitoring.
3. Normalize series and preserve vintages and metadata.
4. Join economic observations to policy and event nodes through jurisdiction and time windows.
5. Add comparative visualizations and a documented institutional risk assessment model; require explicit weighting and validation.

No global economic dataset has been ingested by this document alone.
