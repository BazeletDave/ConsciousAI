# Validated offline evidence staging

Run from repository root:

```bash
python -m unittest discover -s research_tools -p 'test_source_pipeline.py' -v
python research_tools/source_pipeline.py --provider reddit --input approved_reddit_export.jsonl --db /secure/staging/evidence.sqlite
```

Input JSONL contains `url`, `title`, `summary`, `observed_at` (timezone aware), `rights_basis` (`licensed` or `public_metadata`) and `contains_personal_data: false`. Human review must substantiate the rights and privacy declarations. Do not place live participant records, access tokens, or the SQLite database in the public repository.

The SQLite ledger stores unverified candidates and intake events, with deduplication by canonical SHA256. It is local persistent storage **only**, not an adapter to the production GRI evidence database. No network calls, live API connections, evidence promotion, or model training occur.

Local validation on 26 October 2026: 5 unittest methods passed, including nine fail closed subcases. This does not establish production readiness. Before live integration, implement credentialed and terms compliant API adapters, restricted storage, deletion handling, source updates, authentication, concurrency and database migration tests, schema mapping to the actual persistent workflow, and staging deployment checks. Preserve Render production unchanged.
