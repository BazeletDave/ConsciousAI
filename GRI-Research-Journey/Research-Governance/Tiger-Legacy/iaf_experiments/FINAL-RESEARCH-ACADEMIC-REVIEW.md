# GRI IAF V1.1 — Final Internal Research and Academic Review

**Review classification:** Internal research assessment, not independent scholarly peer review or faculty endorsement.

## Reproduction
From this directory run:

```sh
python3 validation_bundle.py > validation-bundle.json
python3 -m json.tool validation-bundle.json > /dev/null
```

The command discovers all `test_*.py` tests and exits nonzero on test failures. The JSON consolidates eight synthetic policy fixtures, stateful trace replay, tabular Q-learning with 1,200 training episodes and 400 held-out decisions, six author-designed OOD probes, and temporary SQLite evidence-ledger checkpoint verification. The output includes input file hashes, Python version, test count, outcomes, and explicit review limitations. The temporary SQLite file is deleted after the run; no persistent or external checkpoint is created.

## Findings and evidence boundaries

| Hypothesis | Assessment | Evidence boundary |
|---|---|---|
| H1: technical validity does not guarantee legitimacy | Supported as an **illustrative counterexample** by author-designed missing-mandate and revoked-consent fixtures | No real institutional legitimacy measurement |
| H2: revocation, replay, escalation reduce governance failures | **Partially demonstrated** for rule-based synthetic denials and tamper detection | Appeal/contestability, escalation latency, fairness, recovery costs and real remediation not implemented |
| H3: adaptive ML/RL can create governance failures | **Exploratory demonstration:** tabular Q-learning optimizes incentives and can propose actions that a separate rule gate rejects | No proof of real-world RL failure rate; held-out seed is not an independent distribution |
| OOD | Six novel vocabulary/state-action probes are rejected by a hard-coded fail-closed guard | Not a statistical OOD robustness benchmark |
| Evidence ledger | SQLite HMAC and hash-chain replay, checkpoint comparison | No external custody; privileged operator with key can rewrite evidence and checkpoint |

## Academic attribution review

- **Roy C. Nelson:** His three political-economy perspectives are used as *interpretive lenses* for authority, incentives, and institutional legitimacy. They are not asserted to be a cybersecurity algorithm. Verify precise citations against the assigned Nelson materials before publication.
- **Robert A. Packenham:** The framework identifies his 1964 *Approaches to the Study of Political Development* as a conceptual political-development source. Application to operational AI control feasibility is a GRI inference, not a claim made by Packenham.
- **David Slocum, Lena Booth, Landry Singh, Doug Guthrie:** Their proposed mappings remain **candidate interpretations**. No precise course-page or primary-publication citations have been supplied or verified in this review. Do not present them as authenticated scholarly derivations.
- **Mansour Javidan / GLOBE:** Relevant only to intercultural organizational expectations; not used as the default AI-governance framework. No faculty endorsement implied.
- **GRI provenance:** All ten IAF controls, synthetic benchmarks and mappings are GRI operationalizations. They do not carry university, faculty, or external certification.

## Review disposition

**Conditional internal research acceptance:** coherent and reproducible in design, with synthetic evidence and explicit limitations. This is **not** independent reproduction, external peer review, security certification, or production approval. Required before research release: run the bundle in a fresh environment; inspect actual CI test logs; obtain independent reviewer signoff; validate exact academic source citations; independently anchor checkpoints if evidence integrity is claimed beyond a single trusted operator. Keep PR #94 unmerged until human approval.
