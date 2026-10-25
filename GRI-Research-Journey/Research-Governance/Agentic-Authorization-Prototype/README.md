# GRI Agentic Authorization Prototype
**Status: independently implemented, local unit tests passed; research only. Not deployed.**

This zero-dependency Python prototype enforces deterministic **tool-time** restrictions separately from intent screening. It does **not** implement Qwen, natural-language semantic classification, real identity verification, signed approvals, persistence, or an agent runtime. An untrusted caller could forge the `approved` boolean: production authorization requires independently verified approval credentials and a trusted principal. Never connect this prototype to real financial, customer or operational systems.

## Run
```bash
python -m unittest discover -v
```

## Features
- Exact normalized intent labels (not semantic interpretation)
- Fail-closed checks for agent, intent, tool, resource, nonnegative transaction amount and approval flag
- SHA-256 policy content fingerprint
- Confusion matrix with BLOCK positive; FAR = FN/(FN+TP), FBR = FP/(FP+TN)
- Synthetic tests covering approved and rejected actions

## Research context and sources
Independent GRI extension inspired by Pal et al., *Persona Guardrail: A Production-Grade Defense Framework for Agentic Systems* (full manuscript supplied to GRI), and Uber Engineering:
- [Scaling AI in Legal: Building Uber's Redlining Agent](https://www.uber.com/us/en/blog/building-ubers-redlining-agent/) (8 October 2026)
- [Designing MCP Gateway Uber's MCP Management Platform](https://www.uber.com/us/en/blog/designing-mcp-gateway/) (1 October 2026)
- [Running a Software Factory Efficiently at Uber Scale](https://www.uber.com/us/en/blog/efficient-software-factory/) (27 August 2026)

The first version tests deterministic authorization only. It cannot reproduce PAGE benchmark results or the paper's reported latency and false-approval rates. Next experiments should introduce a separately evaluated semantic classifier, real identity and cryptographically verifiable approvals, immutable policy versions, adversarial holdouts, multi-turn evaluation and action interception.
