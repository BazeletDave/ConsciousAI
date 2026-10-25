# Read-only intelligence-to-governance adapter

The adapter consumes the existing checked-in `ConsciousAI-Research-Systems/ai_intelligence.json` watchlist and emits a digest-linked, deterministic **simulation** assessment using `governance.py`. It makes no network requests, executes no tools, and cannot authorize real-world actions. The watchlist's URLs and verification-status fields are carried as unverified metadata, not reclassified as verified evidence.

Example from this directory:

```python
from pathlib import Path
from governance import Metrics
from intelligence_adapter import load_watchlist, evaluate_intake
watchlist = Path("../ConsciousAI-Research-Systems/ai_intelligence.json")
record = load_watchlist(watchlist)[0]
print(evaluate_intake(record, metrics=Metrics(.10, .02, .10, 2)))
```

**Security boundary:** This adapter deliberately sets `Request.authorized=False`. Its reviewer approval flag is merely a synthetic publication-review annotation, not identity verification. Thus even benign policy metrics yield DENY for operational authorization. The existing `EvidenceLedger` accepts SYNTHETIC evidence only and is **not** used to relabel real public-source records. An independent, provenance-validated public evidence ledger, trusted identity and reviewer authorization, persistence and external audit anchoring are future work.

**Acceptance:** run `python -m unittest discover -v` from this directory; verify the adapter's source snapshot SHA changes with file edits; confirm no existing service or dashboard code is modified. CI runs these tests on pull requests. No claim is made that the live Render dashboard consumes this adapter.
