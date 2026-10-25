# Measurable Agentic Security Evaluation (research prototype)

This suite measures **authorization decisions**, not generative-AI security efficacy. It is an independent GRI extension and is not affiliated with Uber.

## Reproduce
From this directory:

```sh
python -m unittest -v test_measurable_eval.py
python measurable_eval.py --out evaluation_results.json
python measurable_eval.py --dataset adjudicated_cases.jsonl --out external_results.json
```

Each JSONL row must have `id`, `split`, `family`, `expected_allow` (boolean), and an `action` object with `agent_id`, `intent`, `tool`, `resource`, `amount`, `approved`. Optionally supply independently observed `tool_executed` boolean **on every row** to measure actual unauthorized side effects. Labels must be independent of the tested policy.

## Report
The JSON report contains dataset SHA-256, policy SHA-256, individual decisions and reasons, confusion matrix, per-family results, false-approved and false-blocked rates, and Wilson 95% binomial intervals. A zero-error nine-case fixture does **not** establish zero deployment risk; the upper confidence bound is nonzero. No latency, semantic classifier accuracy, or tool-side-effect outcome is invented.

## Experimental next steps
Build adjudicated benign/OOD/adversarial/mixed sets, separate discovery and held-out validation by attack family and conversation, add a simulated tool executor with tamper-proof audit records, measure P50/P90/P99 under concurrent load, and validate real tool-level enforcement. No real credentials, payments, or external tools should be enabled in this prototype. Apply policy updates through review, shadow mode, limited rollout, and rollback. Compare with the user-supplied Pal et al. Persona Guardrail paper only as an **external published claim**, not a reproduced benchmark.
