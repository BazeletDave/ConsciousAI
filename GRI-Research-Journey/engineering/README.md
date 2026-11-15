# GRI Intelligence Engine 2.0 | Research Prototype

This directory contains the first isolated engineering implementation of the milestone: deterministic evidence intake and a baseline offline evaluation gate.

Run locally using Python 3.11 or later:

```bash
cd GRI-Research-Journey/engineering
python -m unittest discover -p 'test_*.py' -v
```

No third-party dependencies, network calls, automated model training, publication approval, or deployment integration are required. Test data are synthetic.

**Limitations:** SHA-256 digests provide content integrity checks, not authentication or source truth. The drift heuristic only detects mean shifts and must not be represented as comprehensive drift detection. Evaluation metrics do not establish validity, fairness, generalization, or model readiness. Human review and signed provenance have separate evidence and disclosure controls. This public prototype document does not attest to the status of confidential independent assessments.

All changes are additive. The production dashboard, scheduled collectors, and Render services remain unchanged.

## Continuing engineering under controlled disclosure

Development of the existing research prototype can proceed independently of permission to publish confidential review materials. For each code change, retain a reviewable diff, run the existing deterministic tests, record the tested commit and environment, and document reproducible results and limitations. Extend synthetic regression and adversarial coverage only within existing authorized work; do not introduce client data, production connections or new research programs.

The public repository may report results directly reproducible from its code and CI artifacts. Confidential reviewer reports, identities, approval signatures, ethics correspondence and institutional determinations must remain in authorized custody and must not be quoted, summarized as certified outcomes, or committed here without explicit disclosure approval. A report of completed review is not itself a public release authorization. Any human participant activity remains subject to the applicable documented approval scope and conditions, and production deployment requires separate authorization.

Historical milestone statements in other documents refer to their dated evidence snapshots; they are not automatically current or superseded by this workflow. Reconcile them only against records that an authorized custodian can inspect, without publishing restricted contents.
