"""Offline model candidate registry with fail-closed promotion eligibility."""
import hashlib
import json

class ModelRegistry:
    def __init__(self):
        self.candidates = {}

    def register(self, model_id, version, metrics, *, benchmark_eligible=False):
        if not isinstance(model_id, str) or not model_id.strip() or not isinstance(version, str) or not version.strip():
            raise ValueError("model identity required")
        if not isinstance(metrics, dict) or not metrics:
            raise ValueError("metrics required")
        if any(type(v) not in (int, float) or not (-1e100 < v < 1e100) for v in metrics.values()):
            raise ValueError("metrics must be finite numeric values")
        if type(benchmark_eligible) is not bool:
            raise ValueError("benchmark_eligible must be boolean")
        key = (model_id, version)
        payload = {"model_id": model_id, "version": version, "metrics": metrics,
                   "benchmark_eligible": benchmark_eligible, "promotion_authorized": False,
                   "state": "RESEARCH_CANDIDATE"}
        digest = hashlib.sha256(json.dumps(payload, sort_keys=True).encode()).hexdigest()
        if key in self.candidates and self.candidates[key]["manifest_digest"] != digest:
            raise ValueError("conflicting candidate version")
        self.candidates[key] = {**payload, "manifest_digest": digest}
        return self.candidates[key]

    def promotion_decision(self, model_id, version):
        if (model_id, version) not in self.candidates:
            raise ValueError("unknown candidate")
        return {"decision": "DENY", "reason": "No authenticated independent governance approval or staging validation",
                "candidate": self.candidates[(model_id, version)]}
