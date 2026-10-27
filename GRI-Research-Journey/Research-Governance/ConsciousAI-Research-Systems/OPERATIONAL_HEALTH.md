# Operational health and collection diagnostics

`GET /health` checks the six required local datasets for presence and JSON parsing. It returns HTTP 503 if any are missing or invalid. `HEAD /health` uses the same check and status with an empty response body. Readiness does not establish schema validity, data freshness, or independent research validation.

`GET /health/collections` reports collection age separately. HTTP 200 means the diagnostic was returned; inspect its `status` field for `current` or `attention_required`. Collection delays do not remove the dashboard from service. `HEAD /health/collections` checks route availability only.

| Dataset | Timestamp inspected |
| --- | --- |
| Federal Register candidates | `last_collection_at` |
| Governance intelligence feed | `source_last_collection_at` |
| International and mobility discovery | `generated_at`, plus publisher fetch outcomes |

The threshold is six hours, allowing two configured three hour policy collection windows. Ages greater than six hours are `stale`. Timestamps more than five minutes ahead are `future_timestamp`. Missing files, unreadable JSON, invalid types, absent timestamps and timestamps without a timezone cannot produce `current`. International discovery also requires a nonempty publisher collection list with every outcome `fetched`; otherwise a recent file reports `collection_incomplete`.

The intelligence feed uses the upstream collection timestamp so regenerating a derived feed cannot conceal old source data. International discovery reports the latest collector run and publisher outcomes, not the publication date or factual currency of individual articles. Empty collections can be legitimate. Timestamp checks do not authenticate a publisher, verify claims, authorize publication, establish full source coverage, or prove that Render is running the latest GitHub commit.

Inspect manually after deployment:

```bash
curl --fail https://gri-global-intelligence.onrender.com/health
curl --fail https://gri-global-intelligence.onrender.com/health/collections
```

For `attention_required`, inspect each feed status and timestamp, then the GRI Official Policy Monitor workflow and deployment history. Check publisher collection outcomes before retrying. Preserve the existing review gates; never replace an old timestamp with the current time to clear an alert.

Run regression checks from this directory:

```bash
python -m unittest discover -v
```

Tests use synthetic files and a controlled clock, including delayed collection, derived feed regeneration, future and timezone errors, partial publisher failures, corrupted files, and GET/HEAD readiness consistency. No external requests or production data mutation are required by the diagnostic.
