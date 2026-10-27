# Country intelligence: political institutions, management and AI

## Implemented scope

This dashboard extension provides a country selector, source dated evidence candidates, five topic lenses, collection health and metadata change detection. South America is the initial research pilot: Argentina, Bolivia, Brazil, Chile, Colombia, Ecuador, Guyana, Paraguay, Peru, Suriname, Uruguay and Venezuela. The World Bank catalog supplies 217 country and economy entries, including territories. A catalog entry does not establish sovereignty or comprehensive monitoring coverage.

The country view is available within `/dashboard`; the read only API is `/intelligence/countries?country=BRA`. The optional `topic` parameter selects political institutions, trade and investment, organizational management, algorithmic management, artificial intelligence, or records requiring topic review. Brazil links to the existing institutional research case. Existing case claims are not used as verified training labels or automatically promoted into country assessments.

The existing Official Policy Monitor workflow collects every three hours. The browser checks the published snapshot every minute while visible. These are collection and display intervals, not a claim of instantaneous worldwide intelligence. Scheduler delays, publisher availability and deployment delays affect freshness. Source failures retain prior evidence and its last successful timestamp. Complete failure records failure metadata and returns a failing collector exit code; the workflow warns while allowing established collectors to continue.

## Sources and attribution

| Source | Role and verified entry point | Boundary |
| --- | --- | --- |
| World Bank | [Country API documentation](https://datahelpdesk.worldbank.org/knowledgebase/articles/898590-country-api-queries), catalog snapshot with retrieval time | Geography and names, not political ideology or current leaders |
| WTO news | [Official RSS gateway](https://www.wto.org/english/res_e/webcas_e/rss_e.htm), `https://www.wto.org/library/rss/latest_news_e.xml` | Trade publisher metadata; preserve WTO attribution; no logo use |
| UN News | [Americas RSS](https://news.un.org/feed/subscribe/en/news/region/americas/feed/rss.xml) | Regional publisher coverage, not exhaustive country reporting |
| Brazil MDIC | [Ministry feed](https://www.gov.br/mdic/pt-br/assuntos/noticias/@@RSS) | Ministry metadata and index entries; some lack publication dates |
| Brazil Chamber of Deputies | [Official API documentation](https://dadosabertos.camara.leg.br/swagger/api.html), proposals queried for inteligência artificial | Legislative proposal records; neither evidence of enactment nor exhaustive regulatory monitoring |

Endpoint responses were exercised during development. Runtime source status, rather than the inclusion of a URL in this table, determines whether a particular collection succeeded. Only title metadata and source links are retained. Publisher content remains attributed; an official publisher can still report an allegation or policy position requiring verification. Direct government and electoral sources for the other pilot countries remain an expansion task.

## Model and evidence boundaries

`country_topics.py` implements multinomial Naive Bayes with Laplace smoothing using only the Python standard library. The five classes correspond to dashboard lenses. Thirty author created examples across English, Spanish and Portuguese train the baseline; fifteen distinct instructional examples test its mechanics. The model version, training content digest, per class precision, recall, F1, macro F1, accuracy and abstention rate are returned with each snapshot. This small holdout shares the training vocabulary and is not independently labeled; its results cannot estimate performance on actual news.

The classifier abstains when fewer than two known terms appear, its leading normalized weight is below 0.55, or the gap to the next class is below 0.15. These thresholds are engineering defaults, not empirically calibrated acceptance criteria. Model weights are uncalibrated topic scores, not probabilities of political change or economic impact. A single topic may miss a document's other themes. Short headlines, unfamiliar vocabulary, multilingual morphology and long proposal titles can cause abstention or misclassification. All outputs remain review candidates.

Country association uses a publisher jurisdiction or a whole word title mention. A mention is not necessarily the subject jurisdiction. Names can be ambiguous; countries without a matching mention may be missed. No individual political profiling, voter targeting or inferred personal beliefs are collected.

No left or right classification is assigned automatically. Each catalog entry begins with a political assessment of `awaiting_reviewed_baseline`, null direction and no supporting evidence. `political_direction` and `causal_impact` in candidate records remain null. Current leaders, election results, coalitions, proposals versus enacted measures, and sector consequences require dated primary evidence and a reviewed coding protocol. New discovery must not be presented as a newly occurring event or a change in political ideology.

## Change tracking and operational controls

Stable record IDs combine source identity and URL. Content digests cover extracted title, link, publisher date, document type and legal status qualifier. The snapshot retains first observation, last observation, revision time, revision count and the preceding content digest. Changes distinguish newly discovered metadata from revisions. A maximum of 1,000 candidates is retained in the current snapshot; Git history preserves committed snapshot versions. Feed truncation or absence does not establish retraction. Current code does not reconstruct complete political event histories.

Fetches use HTTPS, fixed publisher hosts, same host redirects, bounded response sizes, timeouts and four parallel source requests. Dashboard content uses text nodes and validated HTTPS links. No third party scripts, API credentials, new paid resources or database changes are introduced. Publisher text does not become executable instructions or code. API requests read committed snapshots and do not trigger collection.

## Research pathway

1. Establish reviewed country baselines across governing authority, legislative constraints, trade policy, labor governance and AI policy. Avoid collapsing these axes into one ideological label.
2. Add verified electoral, legislative and government sources for each pilot country, with coverage and freshness checks. Extend other countries only as their sources are implemented.
3. Assemble independently adjudicated multilingual metadata labels, with source and time separated evaluation sets, disagreement records and unknown classes. Measure abstention, precision, recall, calibration and performance by language and country before operational reliance.
4. Add event histories, effective dates and sector exposure records. Assess consequences using documented institutional mechanisms and competing explanations.
5. Evaluate predictive models separately against historical baselines and prospective outcomes. Topic classification is not political forecasting. Trade, investment and managerial impact claims require appropriate economic data and causal identification.

The institutional sequence remains worldview, country, rules, actors, interests, power, options, commitment and adaptation. The dashboard supports that analysis; it does not replace managerial judgment or claim institutional endorsement.

## Verification

From this directory:

```bash
python -m unittest discover -v
node --check country-intelligence.js
python country_intelligence.py
python server.py
```

Offline tests cover multilingual country matching, unknown vocabulary abstention, explicit instructional evaluation, metadata revisions, failed source retention, RDF and Atom parsing, unsafe links and redirects, unknown country and topic queries, and proposal status preservation. The collection command makes public source requests and updates only the country snapshot.

Development verification passed 121 service tests and DOM interaction checks against the local HTTP service for country selection, topic filtering, publisher title injection resistance, request failure cleanup and recovery. The collection snapshot contains 69 candidates with all four configured sources successfully fetched. These counts describe the development snapshot, not guaranteed continuing source availability. Chromium could not be installed in the development environment, so rendered desktop and mobile layout verification remains outstanding. Responsive CSS is implemented, but DOM checks do not validate rendered layout.
