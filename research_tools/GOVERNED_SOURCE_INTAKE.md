# Governed Multisource Research Intake

**Status:** Research prototype, isolated from production. This tool does not connect to Reddit, YouTube, social networks, Render, or any external API. It processes lawfully obtained metadata supplied as JSON Lines. No scraping, automated polling, model training, or dashboard changes are included.

## Operation
```bash
python research_tools/governed_source_intake.py input.jsonl reviewed_candidates.jsonl
```

Example input line:
```json
{"source_type":"youtube","url":"https://www.youtube.com/watch?v=example","title":"Public discussion","observed_at":"2026-10-26T12:00:00Z","rights_basis":"public_metadata","summary":"Research lead requiring verification.","contains_personal_data":false}
```

Allowed source types: reddit, youtube, government, academic, journalism, participant, other. The public intake rejects participant records because consent must be verified separately in a restricted workflow. It rejects pending permissions, non HTTPS URLs, missing provenance fields, and any record not explicitly declared free of personal data. Source domain matching is a basic consistency check, not proof of authenticity. URLs must never be fetched automatically by this script.

Outputs carry a deterministic content digest and candidate ID, with **UNVERIFIED_SOURCE_CANDIDATE**, **HUMAN_REVIEW_REQUIRED**, **training_eligible=false**, and **publication_approved=false**. These labels must not be interpreted as independent verification. The script does not validate licensing or consent; human reviewers must do so.

## Before enabling any live connectors
1. Confirm source specific API permissions, rate limits, terms, retention and redistribution rights; do not assume publicly accessible means permitted for AI training.
2. Design a private participant consent and withdrawal workflow; store identifiers and raw interviews outside the public repository.
3. Establish secure ingestion, secret management, deduplication, failure handling, provenance retention, source correction and deletion workflows.
4. Implement tests for schema, URL boundaries, privacy leakage, idempotency, rights controls and adversarial source text.
5. Use human authorization for all evidence promotion and publication. Retrieval augmented analysis and model training require separate approval and data rights review.
6. Integrate with existing persistent evidence ledger only after reviewing its actual schema and running a staging end to end test. Do not change existing Render services or three hour refresh schedules.

**Research use:** The France Uber Eats claim remains unverified. Social posts are hypothesis generators; official records and independently collected observations can provide distinct corroborating evidence.
