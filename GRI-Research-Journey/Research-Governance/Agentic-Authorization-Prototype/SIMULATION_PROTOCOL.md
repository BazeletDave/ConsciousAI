# GRI simulated tool execution experiment

Research-only, offline, zero-network, zero-real-tool side effects. The simulator models a controlled resource store and records **authorization decision** separately from **actual execution**. It compares enforcing and monitor-only modes on identical fixtures. Each event is linked to the previous event with SHA-256, enabling detection of edits to a retained chain (not protection against an attacker rewriting the entire chain without an independently trusted anchor).

## Reproduction

Run from this repository directory:

```sh
python -m unittest -v test_simulated_runtime.py
python simulated_runtime.py --out simulation_results.json
```

## Interpretation

The nine synthetic fixtures contain one authorized booking and eight unauthorized requests. Enforcing mode should execute only the authorized booking; monitor-only mode deliberately executes all nine simulated actions. This demonstrates **what enforcement changes in this test harness**, not a measured real-world attack success rate. The simulated action store contains no user data and makes no API calls. Do not describe hash chains as immutable audit records or infer external validity from this fixture set.

## Local validation

Five simulator tests passed in a local test environment against the repository's authorization logic and fixture definitions reproduced locally. The committed GitHub revision has not yet been independently run through CI.

## Next research gate

Replace handwritten cases with independently adjudicated held-out scenarios, record actual side effects from a sandbox tool runner, test authorization under concurrency, authenticate grant issuers, and separately benchmark an LLM semantic classifier and latency. Require review before deploying any tool integration.
