# Persisted evidence handoff (read-only)

The existing scheduled workflow writes `ConsciousAI-Research-Systems/assurance_evidence_snapshot.json` using `build_assurance_evidence.py`. This module validates that artifact's exact SHA-256 content hash and record counts, joins its evaluation IDs to the checked-in watchlist, and returns a digest-linked manifest. It **does not** alter the existing producer, Render server, dashboard, scheduler, or `EvidenceLedger` synthetic-only guard.

From this directory:

```sh
python -m unittest discover -v
python -c "from persistent_bridge import build_linked_manifest; from pathlib import Path; p=Path('../ConsciousAI-Research-Systems'); print(build_linked_manifest(p/'ai_intelligence.json',p/'assurance_evidence_snapshot.json')['manifest_sha256'])"
```

**End-to-end boundary:** watchlist -> existing deterministic assurance producer -> persisted JSON snapshot -> integrity and ID checks -> read-only linked manifest -> mandatory human review. The manifest is not a production agent approval and is not served on the dashboard. The producer's record hash is retained without claiming it is a digest of the raw watchlist record. No trusted external audit anchor, immutable storage, or independent source validation exists in this bridge.

**Staleness:** Snapshot and watchlist can diverge between scheduled runs; fail closed on ID mismatch. This implementation does not establish freshness of individual records or the source URLs. Approval, if any, must occur in a separately authenticated and audited workflow.
