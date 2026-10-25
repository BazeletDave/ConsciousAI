"""Read-only intake-to-governance bridge. No real-world action authorization."""
from dataclasses import dataclass
from hashlib import sha256
import json
from pathlib import Path
from governance import Metrics, Policy, Request, assess
from evidence import digest

@dataclass(frozen=True)
class IntakeRecord:
    record_id: str
    source_status: str
    summary: str
    source_urls: tuple
    snapshot_digest: str

def load_watchlist(path):
    """Load only local, checked-in watchlist data; never fetch source URLs."""
    path = Path(path)
    payload = path.read_bytes()
    data = json.loads(payload)
    if data.get("schema_version") != "1.0" or not isinstance(data.get("records"), list):
        raise ValueError("unsupported watchlist schema")
    result = []
    seen = set()
    for item in data["records"]:
        rid = item.get("id")
        if not isinstance(rid, str) or not rid.strip() or rid in seen:
            raise ValueError("invalid or duplicate record ID")
        seen.add(rid)
        urls = tuple(s["url"] for s in item.get("sources", []) if isinstance(s, dict) and isinstance(s.get("url"), str) and s["url"].startswith("https://"))
        result.append(IntakeRecord(rid, str(item.get("verification_status", "unreviewed")), str(item.get("summary", "")), urls, sha256(payload).hexdigest()))
    return result

def evaluate_intake(record, *, metrics, policy=None, reviewer_approved=False):
    """Produce a review-gated simulation; a watchlist is not proof of an incident.

    Metrics MUST be independently supplied for a synthetic scenario. This
    function never infers safety metrics from a news item or authorizes tools.
    """
    if not isinstance(record, IntakeRecord) or not isinstance(metrics, Metrics):
        raise TypeError("typed intake record and synthetic metrics required")
    if not isinstance(reviewer_approved, bool):
        raise TypeError("reviewer_approved must be bool")
    policy = policy if policy is not None else Policy()
    if not isinstance(policy, Policy):
        raise TypeError("policy must be Policy")
    req = Request("intake:" + record.record_id, "gri-research-simulator", "evaluate_record_only", False, metrics)
    # Fail closed: this is never authorization for operational agent action.
    decision = assess(req, policy, human_approved=False)
    body = {
        "schema_version": "gri.intake-assessment.v1",
        "mode": "READ_ONLY_SYNTHETIC_METRICS",
        "record_id": record.record_id,
        "source_status": record.source_status,
        "source_urls": list(record.source_urls),
        "snapshot_sha256": record.snapshot_digest,
        "reviewer_approved_for_publication": reviewer_approved,
        "requires_human_review": True,
        "operational_authorization": False,
        "policy_decision": decision,
        "notice": "Source URLs and status are metadata only; no source verified by this adapter. Approval flag is not trusted identity or action permission.",
    }
    return {**body, "assessment_sha256": digest(body)}
