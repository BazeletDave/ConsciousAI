# IAF V1.1 — Genuine Learning Experiment (Synthetic Tabular Q-Learning)

This increment introduces **actual tabular Q-learning** using Python's standard library. The agent learns action values from rewards and explores actions with epsilon-greedy selection. The intentionally risky reward favors `export`; an independent institutional permission gate evaluates every proposed action at execution time.

## Reproduce
```sh
cd GRI-Research-Journey/Research-Governance/Tiger-Legacy/iaf_experiments
python3 -m unittest discover -s . -p 'test_*.py' -v
python3 qlearning_governance.py
```

Training uses a fixed seed, 1,200 episodes, and four synthetic states. Held-out evaluation uses a **different seed** and 400 action decisions. Results include false approvals for an intentionally permissive baseline versus the institutional gate and a digest of held-out decisions.

## Critical limits
- The agent **does learn** a Q-table, but this is not deep RL, production ML, or a deployed autonomous system.
- The holdout is independent in RNG seed, **not** in task distribution or researcher design. It is not a robust out-of-distribution (OOD) benchmark.
- The baseline is intentionally permissive and is not a fair comparison to a mature authorization product.
- A zero false-approval count on synthetic cases is a test observation, not evidence of production efficacy.
- Academic attribution and independent reproduction remain separate gates.
- The synthetic states, action names, and rewards contain no client information.
