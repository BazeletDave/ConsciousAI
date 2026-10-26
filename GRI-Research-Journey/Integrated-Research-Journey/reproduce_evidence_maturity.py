#!/usr/bin/env python3
"""Reproduce evidence-maturity counts from GRI's reviewed repository README register.
No external packages or private data. Not a population estimate of institutional AI adoption.
"""
import csv
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve().parent
INPUT = HERE / "2026-10-26-repository-evidence-register.csv"
OUTPUT = HERE / "2026-10-26-evidence-maturity-summary.md"
rows = list(csv.DictReader(INPUT.open(encoding="utf-8", newline="")))
assert len(rows) == len({r["case_id"] for r in rows}), "Duplicate IDs"
assert all(r["source_url"].startswith("https://github.com/BazeletDave/") for r in rows)
assert all(r["documented_deployment"] in {"yes", "no", "not_assessed"} for r in rows)
counts = Counter(r["documented_deployment"] for r in rows)
lines = [
    "# Repository Evidence-Maturity Snapshot",
    "",
    "Reviewed public README records only; N=%d. **Not** a representative sample of employers, platforms or AI adoption." % len(rows),
    "",
    "| Deployment evidence recorded in reviewed README | Repository count |",
    "| --- | ---: |",
]
for label in ("yes", "no", "not_assessed"):
    lines.append(f"| {label} | {counts[label]} |")
lines += [
    "",
    "The 'yes' category records the ConsciousAI README's link to the deployed GRI dashboard; it does not establish independent validation or deployment of every research module.",
    "The 'no' category means the reviewed README does not document an independently deployed AI system for the coded case, not that none exists.",
    "Human-review status is not assessed for all six cases; no governance effectiveness score is inferred.",
    "",
    "## Figure: observed documentation status (each block = one repository)",
    "",
]
for label in ("yes", "no", "not_assessed"):
    lines.append(f"- {label}: {'█' * counts[label]} ({counts[label]})")
lines.append("")
OUTPUT.write_text("\n".join(lines), encoding="utf-8")
print(OUTPUT.read_text(encoding="utf-8"))
