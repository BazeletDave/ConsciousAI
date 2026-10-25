# GRI Intelligence Engine 2.0 | Research Prototype

This directory contains the first isolated engineering implementation of the milestone: deterministic evidence intake and a baseline offline evaluation gate.

Run locally using Python 3.11 or later:

```bash
cd GRI-Research-Journey/engineering
python -m unittest discover -p 'test_*.py' -v
```

No third-party dependencies, network calls, automated model training, publication approval, or deployment integration are required. Test data are synthetic.

**Limitations:** SHA-256 digests provide content integrity checks, not authentication or source truth. The drift heuristic only detects mean shifts and must not be represented as comprehensive drift detection. Evaluation metrics do not establish validity, fairness, generalization, or model readiness. The human-review process and signed provenance are separate future milestones.

All changes are additive. The production dashboard, scheduled collectors, and Render services remain unchanged.
