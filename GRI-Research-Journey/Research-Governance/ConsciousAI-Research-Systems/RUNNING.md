# Running the local research systems prototype

**Status:** Working reference implementation for local execution. It is **not** a deployed service and does not fetch live legislation.

Requirements: Python 3.10 or later. No third party packages.

From this folder run:

```bash
python server.py
```

Then open `http://127.0.0.1:8000/graph`, `/cases`, `/policies` or `/health`.

Evidence completeness request:

```bash
curl -X POST http://127.0.0.1:8000/assessments \
  -H 'Content-Type: application/json' \
  -d '{"case_id":"GRI-LYFT-CHI-002"}'
```

Run tests with:

```bash
python -m unittest discover -v
```

## Scope and safeguards

- Read only research endpoints plus a stateless evidence completeness assessment.
- Binds to localhost by default; do **not** expose publicly without authentication, rate limits, deployment hardening, and a security review.
- The graph returns nodes and typed research comparison edges, not a rendered interactive graph.
- Policy endpoint intentionally returns an empty, explicitly unverified registry until official records are reviewed.
- No causal attribution, ethical certification, compliance advice, automated legal updates or production deployment is implied.

## Visual interface and event intelligence

After starting the local server, open `http://127.0.0.1:8000/dashboard` to explore the interactive graph. JSON feeds are available at `/events` and `/policy-sources`. Events and official policy entries must be reviewed and added to their versioned registries before they appear. No background polling is enabled.
