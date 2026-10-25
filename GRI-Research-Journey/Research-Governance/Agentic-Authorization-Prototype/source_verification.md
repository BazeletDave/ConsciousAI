# Source verification ledger (24 October 2026)
Research-only. A verified publication is not a replication of its results.

| Work | Primary source | Status | Relevance |
|---|---|---|---|
| Pal et al., Persona Guardrail | Full manuscript supplied by researcher; independent publisher landing page not yet confirmed | MANUSCRIPT PROVIDED, PUBLICATION UNVERIFIED | Input/output persona enforcement; PAGE; excludes intermediate actions |
| Debenedetti et al., AgentDojo (2024) | https://proceedings.nips.cc/paper_files/paper/2024/hash/97091a5177d8dc64b1da8bf3e1f6fb54-Abstract-Datasets_and_Benchmarks_Track.html | VERIFIED PRIMARY | Indirect prompt injection; different threat model from PAGE |
| Andriushchenko et al., AgentHarm (ICLR 2025) | https://proceedings.iclr.cc/paper_files/paper/2025/hash/c493d23af93118975cdbc32cbe7323f5-Abstract-Conference.html | VERIFIED PRIMARY | Harmful agent requests; not a persona benchmark |
| OWASP Top 10 for LLM Applications 2025 | https://genai.owasp.org/resource/owasp-top-10-for-llm-applications-2025/ | VERIFIED HISTORICAL EDITION | Excessive agency, prompt injection |
| OWASP GenAI LLM Top 10 2026 | https://github.com/GenAI-Security-Project/GenAI-LLM-Top10 | CURRENT PROJECT INDICATED BY OWASP ARCHIVE; NOT FULLY REVIEWED | Current security taxonomy |
| Uber Legal Redlining Agent | https://www.uber.com/us/en/blog/building-ubers-redlining-agent/ | ORIGINAL ENGINEERING PUBLICATION | Human-supervised legal workflow |
| Uber Designing MCP Gateway | https://www.uber.com/us/en/blog/designing-mcp-gateway/ | ORIGINAL ENGINEERING PUBLICATION | Tool governance |
| Uber Efficient Software Factory | https://www.uber.com/us/en/blog/efficient-software-factory/ | ORIGINAL ENGINEERING PUBLICATION | Operational productivity |

## Evidence boundaries
- The supplied Pal et al. manuscript reports 95.9% accuracy and 4.7% false-approved rate on its PAGE benchmark; these are **author-reported**, not independently reproduced.
- PAGE explicitly does not establish prevention of indirect prompt injection or intermediate unauthorized tool actions.
- Our independent prototype provides deterministic tool authorization; it is **not** a reproduction of Persona Guardrail, PAGE, or Uber's production system.
- Remaining citations in the 28-item bibliography are **not yet individually verified**. Do not mark them verified without checking the original work.
- The supplied manuscript has an internal inconsistency: its abstract describes a hybrid allowlist/blocklist framework, whereas its empirical section concludes the iterated allowlist outperforms the combined configuration on overall accuracy and benign false-block rate. Report both accurately.
