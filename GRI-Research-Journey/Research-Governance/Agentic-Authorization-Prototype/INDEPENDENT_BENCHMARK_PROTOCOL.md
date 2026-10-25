# Independent-label multi-turn benchmark protocol
Status: **evaluation infrastructure implemented; external dataset ingestion not yet performed**.

Run from this directory:
```bash
python -m unittest -v test_independent_benchmark.py
python independent_benchmark.py --dataset adjudicated_turns.jsonl --out results.json
```
Each JSONL record: `conversation_id`, `turn_index` (zero-based), `family`, `split`, `expected_allow` (boolean), `label_source` (`independent_human` or `external_dataset`), `adjudicator_id`, and `action` containing exactly `agent_id,intent,tool,resource,amount,approved`. Metadata is an assertion, not verification: independently audit labels and provenance. Entire conversations must remain in one split and one family. Pair experiments on identical conversation IDs and ground truth.

Metrics: turn-level false approval/block rates, Wilson 95% intervals, per-family confusion matrices, and conversation-level rate of at least one prohibited turn allowed. Paired comparison uses seeded conversation-cluster bootstrap. Bootstrap interval is descriptive, not proof of statistical independence, causation, or generalizability. Pre-register hypotheses, sample sizes, exclusion rules and stopping criteria before using external data.

**Dataset mapping caution:** AgentDojo, AgentHarm and PAGE contain tasks and/or labels that do not directly provide this prototype's structured action fields. Do not invent tool calls or treat malicious intent as an observed executed action. A source-specific adapter requires provenance, licensing review, independently labeled action mappings, and held-out validation. No external dataset has yet been imported or benchmarked; no model-generated multi-turn behavior or real side effects are measured.

**Security:** Offline, research only. Do not connect to real accounts, financial transfers, customer data, or live agent tools.
