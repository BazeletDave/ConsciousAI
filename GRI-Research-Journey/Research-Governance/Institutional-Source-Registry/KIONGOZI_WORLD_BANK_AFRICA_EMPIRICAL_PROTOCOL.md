# Kiongozi | World Bank Africa AI foundations: empirical intake and validation
**GRI existing research extension | November 3, 2026**
**Scope:** Kiongozi, Landry Signé source registry, AI Paradox, institutional governance, comparative development and independent assurance. Not a new project.

## Evidence and implementation status
A reproducible, standard-library World Bank WDI collector is stored at [world_bank_africa_baseline.py](../ConsciousAI-Research-Systems/world_bank_africa_baseline.py). It targets Ghana, Kenya, Nigeria, Rwanda and South Africa for the 2020–2024 observation window and the WDI electricity access, internet usage, GDP per capita and population indicators. Country selection is **illustrative and purposive**, not representative of Africa. No unverified indicator values are embedded in this note.

**Execution status:** World Bank's official API documentation and source definitions were verified; a live API response could not be retrieved in the current execution environment, so **no country numerical baseline has been produced, no empirical relationship tested and no live dashboard integration claimed**. The collector is committed for execution in an authorized network-enabled environment. Any successful run must retain the exact CSV, retrieval timestamp, response SHA-256 and Git commit; reruns may differ as the World Bank revises series.

## Official sources and method
* [World Bank Indicators API V2](https://datahelpdesk.worldbank.org/knowledgebase/articles/889392): no API key required; supports country, indicator and date queries.
* [World Bank API query structure](https://datahelpdesk.worldbank.org/knowledgebase/articles/898581): multiple country queries, explicit date windows, JSON output and pagination.
* [World Bank WDI electricity access indicator methodology](https://data360files.worldbank.org/data360-data/metadata/WB_WDI/WB_WDI_EG_ELC_ACCS_ZS.pdf): household survey and census based; national access is not equivalent to reliable, affordable electricity for AI compute.
* [World Bank WGI 2026 methodology](https://www.worldbank.org/en/publication/worldwide-governance-indicators): perception-based six dimensions; historical revisions, uncertainty and measurement limitations must be preserved. WGI must be ingested as a **separate versioned dataset** before governance associations are estimated. Do not mix old percentile ranks with revised absolute scores.
* [Landry Signé public scholarship registry](../Institutional-Source-Registry/LANDRY_SIGNE_PUBLIC_RESEARCH.md): existing academic foundation; GRI's analytical mappings are not claims attributed to Signé or Thunderbird.

## Reproducibility and validation contract
1. Run `python3 world_bank_africa_baseline.py --output africa_wdi_baseline.csv` in a network-enabled, authorized environment.
2. Verify HTTP success, API metadata, expected country and year coverage, null values, original source URL and response digest.
3. Compare WDI figures against the World Bank DataBank or archived downloaded release. Never silently backfill missing values.
4. Separately download and version the **2026 WGI release** and record the exact 0–100 scale or standardized estimate chosen. Retain uncertainty intervals and source revision metadata.
5. Evaluate data completeness by country, year and indicator before any correlation, clustering or comparison. Use years consistently and document data lags.
6. Only after verification, test explicitly labeled hypotheses connecting digital foundations, institutional governance and development outcomes, controlling for confounders. Do not infer causality from cross-country correlations.
7. Run independently reproducible regression and source integrity checks before dashboard publication. Human approval required.

## Research design: bounded comparative tests
**H1 (foundations):** Electricity and internet availability may constrain scalable AI adoption; WDI household access measures are imperfect proxies for data center readiness.
**H2 (institutions):** Governance and public administration capacity may mediate the translation of digital investment into broad benefits. WGI perception indicators do not measure AI governance directly.
**H3 (leapfrogging):** Countries may pursue distinct trajectories based on affordability, skills, local ownership and public infrastructure; investment announcements alone do not establish inclusive growth.
**H4 (agentic governance):** Kiongozi and Tiger assurance requirements for delegated authority, traceability, revocation and remedy remain applicable to AI systems operating in development contexts.

## Data protections
No private student work, confidential GRI IP or proprietary case materials are ingested. No automated political classification, ranking of governments, claims of AI superintelligence, self-modifying models or production ingestion is authorized by this research note.
