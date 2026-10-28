# CISA 2030 | Synthetic assurance measurement v0.1

This module introduces an offline, standard library only assurance evaluator for six GRI research constructs. It does not implement CISA certification or measure operational infrastructure. Each measure is explicitly **pass**, **fail**, or **unmeasured**. Missing evidence cannot be counted as success. Boolean input represents an experimenter's synthetic observation, not independent proof.

Run locally from this directory:

```bash
python -m unittest -v test_assurance.py
```

The SHA256 digest binds a canonical JSON representation of the case, but it is not a signature, timestamp authority, or independently anchored audit trail. This module neither reads secrets nor performs network requests. No endpoint or dashboard changes are made here.

**Integration plan:** validate this offline module through CI, then expose only clearly labeled synthetic research results through a separately reviewed read only endpoint. Confirm dashboard compatibility and deployed source freshness before adding a visual panel. The existing unified research index may retrieve these Markdown research documents on rebuild, but this is not confirmation of deployment.

**Methodology:** define experimental criteria before testing; capture authorized inputs and independent outcomes; do not interpret the synthetic boolean measures as real world security effectiveness.
