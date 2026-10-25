# GRI Continuous Intelligence — Phase 1

## Implemented
Offline, deterministic intake from **already authorized and collected** JSONL source records; SHA-256 evidence IDs, duplicate suppression, controlled evidence-status vocabulary, invalid-input reporting and mandatory human-review status. No claim is automatically verified or published.

```sh
python -m unittest -v test_evidence_monitor.py
python evidence_monitor.py --input permitted_sources.jsonl --output review_queue.json
```

Required source fields: `source_url,source_platform,source_date,claim_text_paraphrase,verification_status`. This is a research prototype, not an automated crawler or a machine-learning model.

## Target architecture (not deployed)
- Scheduled, rate-limited, terms-compliant source connectors with per-source permission records.
- Immutable raw-source reference + content hash, ingestion timestamp, original author/source attribution, correction/retraction tracking, and independent claim adjudication.
- ML-assisted topic classification, multilingual translation, semantic deduplication and anomaly detection; model version and confidence must be recorded.
- Independent driver-level consent-based data and market-specific institutional sources.
- Separate review queue for high-impact conclusions and publication approval; no autonomous policy escalation.
- GitHub CI for tests; optional Vercel UI and Render background jobs only after owner approval and service inventory review.
- Security: least-privilege tokens, no scraping private groups, redaction of personal data, source-level rate limits, retention policy, audit log and rollback.
- Evaluation: independently labeled holdouts, precision/recall, drift, source coverage, latency, operating cost, inter-rater agreement and false-alert rates.

## Research boundary
Driver anecdotes generate hypotheses, not verified internal platform behavior. Do not use social posts as ground-truth authorization labels. Preserve distinction between company disclosures, empirical driver records, and speculation.
