# GRI operational baseline | 2026-10-25

## Repository baseline

- Source of truth: `BazeletDave/ConsciousAI`, `main`.
- Observed main commit: `16212f9e832cf1e7429d2541c838c07b3ff53477` (Agentic Governance Engine v2 merge).
- Prior validated research merges: `271172c00a7b4cbda35772dd636dc4f115b05b8c` (Frontier Governance Lab) and `3795d90a34cfa95901705a79b5ed97766d1e6328` (evidence-linked synthetic assurance).
- GitHub Actions for PR #26: GRI Frontier Governance Lab and GRI Research Quality Gate both reported success before merge.
- Latest main commit has no PR-triggered workflow runs returned by the checked GitHub endpoint. This is **not** evidence that all scheduled workflows stopped.
- Latest main Vercel checks reported build-rate-limit failures for `back-door` and `conscious-ai`. These checks do not establish Render service failure.

## Deployment verification status

Public dashboard: https://gri-global-intelligence.onrender.com/dashboard

Public health endpoint: https://gri-global-intelligence.onrender.com/health

Live endpoint verification: **UNVERIFIED in this review** (external access unavailable). No claim is made that Render is down or that its deployed revision equals main.

## Required operational acceptance checks

1. Record an HTTP 200 GET for `/health`, including UTC timestamp and response body.
2. Record an HTTP 200 GET for `/dashboard`; confirm key dashboard data fetches and absence of JavaScript exceptions.
3. Record the deployed Git commit or immutable build identifier from the deployment system; compare to current `main`.
4. Confirm source intake freshness from actual workflow history and checked-in ledger timestamps; separate collected from human-verified evidence.
5. Exercise read-only API routes and validate response schemas, bounded pagination and provenance fields.
6. Run existing research tests and record workflow IDs, outcomes and artifacts for the exact candidate commit.
7. Demonstrate end-to-end evidence handoff from an intake record to a policy evaluation and linked assurance record using synthetic data, without treating the handoff as real authorization.
8. Verify rollback procedure, recovery evidence and service configuration before any production integration.

## Status distinctions

- **Repository integration:** verified for commits listed above.
- **Synthetic research tests:** passed on the PR #26 head before merge.
- **Live Render deployment at exact main revision:** not verified.
- **Cross-module runtime integration:** not established by the offline evidence adapter.
- **Independent audit anchoring and empirical safety validation:** not established.

This baseline is a point-in-time engineering review, not a regulatory certification or an assertion of production failure. Do not alter existing Render services to complete this review.
