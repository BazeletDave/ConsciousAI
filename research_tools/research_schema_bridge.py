"""Fail-closed adapter from staging evidence candidates to GRI research intake drafts."""
import json
from datetime import datetime

def candidate_to_draft(candidate, domain="algorithmic_management"):
    if not isinstance(candidate, dict) or candidate.get("review_status") != "HUMAN_REVIEW_REQUIRED" or candidate.get("publication_approved") is not False or candidate.get("training_eligible") is not False:
        raise ValueError("candidate is not a quarantined research intake")
    digest = candidate.get("digest", "")
    if not isinstance(digest, str) or len(digest) != 64 or any(c not in "0123456789abcdef" for c in digest):
        raise ValueError("invalid evidence digest")
    if candidate.get("source_type") not in ("reddit", "youtube"):
        raise ValueError("unsupported source type")
    if domain not in {"algorithmic_management", "ai_governance", "institutional_accountability", "mobility", "leadership", "financial_value_creation", "cybersecurity"}:
        raise ValueError("invalid domain")
    observed = candidate.get("observed_at", "")
    try:
        dt = datetime.fromisoformat(observed.replace("Z", "+00:00"))
        if dt.tzinfo is None:
            raise ValueError()
    except (ValueError, AttributeError):
        raise ValueError("invalid observed_at") from None
    return {"id": "GRI-" + digest[:16].upper(), "title": candidate["title"], "date": dt.date().isoformat(),
            "domain": domain, "claim_type": "source_report", "summary": candidate["summary"],
            "source_type": candidate["source_type"], "provenance": candidate["url"] + " | sha256:" + digest,
            "limitations": "Unverified source candidate. Human verification, rights review, and independent corroboration required.",
            "review_status": "draft", "publication_authorized": False}

def export_drafts(database_path):
    import sqlite3
    with sqlite3.connect(database_path) as db:
        rows = db.execute("SELECT payload FROM evidence WHERE status='HUMAN_REVIEW_REQUIRED' ORDER BY digest").fetchall()
    return {"records": [candidate_to_draft(json.loads(row[0])) for row in rows]}
