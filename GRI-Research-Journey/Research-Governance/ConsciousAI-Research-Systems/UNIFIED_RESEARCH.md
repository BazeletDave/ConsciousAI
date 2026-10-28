# Unified GRI research and question answering

The /dashboard#gri-research-library panel connects public research in GRI-Research-Journey, Research-Journey, research, autonomous-mobility-research and root research documents. It covers Uber and Lyft, autonomous vehicles, mobility, the Fourth Industrial Revolution, AI, the AI Paradox and institutional governance. Other public GRI research within these roots remains discoverable.

The index rebuilds from repository files each time the Python service starts. New research commits follow the existing Render deployment path. It performs no external source collection and does not change existing feed schedules. The generated index is a runtime cache; the builder is the versioned source of truth.

GET /research/catalog reports documents, searchable passages, linked PDF and Office artifacts, topic coverage, exclusions and a corpus digest. Text documents are searched in full through paragraph passages; binary artifacts are linked but their contents are not searched. Exact duplicate text is consolidated with alternate links. Private or restricted paths, coursework identifiers, raw participant interviews, mirrored source snapshots, and the separate novel project are outside the index. Files outside this repository are not automatically connected.

GET /research/ask?q=...&topic=... uses BM25 statistical passage retrieval and returns up to five distinct source titles, excerpts and line links. It provides an extractive research answer, not a generative model synthesis or independent fact check. Unsupported vocabulary and insufficient support are exposed; it must not invent an answer. Repository passages can contain hypotheses, historical statements, preliminary findings and attributed reports. Each retains an explicit evidence status and requires primary source checking before scholarly submission.

Existing country evidence connections now scan the broader GRI research roots as well. Their analytical links remain proposed associations, not causal findings. This integration does not train a predictive model or promote unreviewed claims.

Validation: run python -m unittest discover -v. Rebuild locally with python unified_research.py. Inspect source links, topic coverage, irrelevant questions, restricted paths, long questions, source line provenance and the dashboard search flow before release.
