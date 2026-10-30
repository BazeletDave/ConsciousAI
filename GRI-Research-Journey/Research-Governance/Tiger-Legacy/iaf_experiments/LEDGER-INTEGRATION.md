# IAF Synthetic Evidence Ledger Integration

**Status:** Research adapter proposed in PR #94. This bridge imports the existing `version_one/evidence_ledger.py` and appends synthetic action-decision traces to a separate SQLite file. It does **not** change the original ledger implementation, production routes, or legacy research artifacts.

Run from this directory:
```sh
python3 -m unittest discover -s . -p 'test_*.py' -v
python3 verify_research.py > evidence-report.json
```

Five bridge tests exercise append/checkpoint, incorrect key, privileged tampering after trigger removal, checkpoint mismatch, and rejection of non-synthetic inputs.

**Security boundary:** The research HMAC key is hard-coded **only in test code** and is not a production secret. SQLite immutability triggers and HMACs are not sufficient against an operator with key and database control. The exported checkpoint is marked as lacking an independent custodian. No claim of external attestation or independent review is made.

**Further gates:** CI must explicitly execute all new tests; the evidence report must be independently reproduced. Genuine ML/RL training and held-out evaluation remain outside this adapter.
