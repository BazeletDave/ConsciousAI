# Out-of-distribution (OOD) research probes

This synthetic extension tests six manually authored state/action combinations **not present in the four-state, two-action Q-learning training vocabulary**. The Q-table cannot score unseen pairs; a separate institutional permission guard denies them without extrapolating Q values.

Reproduce in this directory:

```sh
python3 -m unittest discover -s . -p 'test_*.py' -v
python3 qlearning_governance.py
python3 ood_governance.py
```

**Interpretation:** These are vocabulary-shift and unknown-authority probes, not a statistical OOD generalization study. They are hand-selected by the researchers; they do not constitute an independently designed benchmark. The deliberately permissive baseline is illustrative only. A fail-closed rule is a property of the explicitly coded guard, not evidence that a deployed AI model is safe.

**Independent reproduction protocol:** Use a fresh checkout pinned to the PR commit; record Python version, command output, test counts, SHA-256 digests, and independently review all fixture labels and the authority policy. Recompute the report without trusting the author-produced output. Test a tampered ledger and wrong HMAC key. External custody, scientific replication, and academic attribution remain unverified.
