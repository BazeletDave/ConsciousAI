# Tiger Legacy Version One | Synthetic Security Lab

Research-only Python standard library reference engine. No production integrations or external network calls.

Run from this directory: `python -m unittest discover -s tests -v`.

Synthetic tenants alpha and beta are used to test deny by default authorization, resource ownership, scoped consent, expiration, revocation, cross tenant denial, and HMAC SHA256 hash chain integrity. The HMAC secret is an explicitly synthetic local test key. Evidence is in memory and not independently anchored or durable. Authentication is assumed, not implemented. This is not a production identity service, cryptographic certification, or deployable cybersecurity replacement.

The existing Agentic Governance Engine provides a useful canonicalization and hash chain pattern, but its financial capability policy is not reused directly. The CISA evidence ledger intentionally rejects synthetic records and is not reused for this synthetic lab. The Agentic Authorization Prototype's README states its approval boolean is forgeable without external verification. These are important compatibility boundaries.

Further gates: persistent isolation, authenticated principals, independent key management, concurrent updates, durable signed evidence, backup restoration, negative test expansion, CI execution, dashboard integration, and independent review. No real client systems or data.
