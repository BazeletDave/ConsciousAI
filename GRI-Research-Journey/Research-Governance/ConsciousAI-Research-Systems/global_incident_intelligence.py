"""GRI global incident relationship intelligence. Read-only, evidence-first extension.

This module does not scrape sources, assert incident truth, or alter production.
Use with the existing dashboard service after review and integration tests.
"""
from __future__ import annotations
from datetime import date, timedelta
from urllib.parse import urlparse

COUNTRY_SOURCES = {
    "Singapore": [{"name": "Cyber Security Agency of Singapore", "url": "https://www.csa.gov.sg/"}],
    "Brazil": [{"name": "CERT.br", "url": "https://www.cert.br/"}, {"name": "CTIR Gov", "url": "https://www.gov.br/ctir/pt-br"}],
    "Costa Rica": [{"name": "MICITT", "url": "https://www.micitt.go.cr/"}],
    "India": [{"name": "CERT-In", "url": "https://www.cert-in.org.in/"}],
    "United States": [{"name": "CISA", "url": "https://www.cisa.gov/"}],
}
EVIDENCE_STATES = {"reported", "officially_acknowledged", "independently_corroborated", "disputed", "unverified"}
RESOLUTION_STATES = {"unknown", "investigating", "mitigation_reported", "resolved_by_vendor", "independently_verified"}
# A person's job title is not proof of fault or direct incident responsibility.
RELATIONS = {"affected", "depends_on", "reported_by", "investigated_by", "remediated_by", "regulated_by", "led_by", "research_connection"}

def valid_https(url):
    try:
        p = urlparse(url)
        return p.scheme == "https" and bool(p.hostname) and not p.username and not p.password
    except (TypeError, ValueError):
        return False

def validate(record):
    """Validate public incident metadata without declaring it true."""
    errors = []
    required = ("id", "title", "event_date", "jurisdiction", "organization", "summary",
                "evidence_status", "resolution_status", "sources")
    for field in required:
        if not record.get(field):
            errors.append("missing_" + field)
    try:
        date.fromisoformat(record["event_date"])
    except (ValueError, KeyError, TypeError):
        errors.append("invalid_event_date")
    if record.get("evidence_status") not in EVIDENCE_STATES:
        errors.append("invalid_evidence_status")
    if record.get("resolution_status") not in RESOLUTION_STATES:
        errors.append("invalid_resolution_status")
    for source in record.get("sources", []):
        if not isinstance(source, dict) or not valid_https(source.get("url")):
            errors.append("invalid_source")
    for link in record.get("relationships", []):
        if not isinstance(link, dict) or link.get("relation") not in RELATIONS or not link.get("source_url") or not valid_https(link["source_url"]):
            errors.append("unsupported_relationship")
    return errors

def snapshot(records, as_of=None, window_days=30):
    """Provide a conservative international intelligence view, without incidence-rate claims."""
    today = as_of or date.today()
    cutoff = today - timedelta(days=window_days - 1)
    valid, rejected = [], []
    for r in records:
        errors = validate(r)
        if errors:
            rejected.append({"id": r.get("id"), "errors": errors})
            continue
        if cutoff <= date.fromisoformat(r["event_date"]) <= today:
            valid.append(r)
    countries = sorted({r["jurisdiction"] for r in valid})
    return {
        "as_of": today.isoformat(), "window_days": window_days,
        "records": valid, "rejected": rejected,
        "country_coverage": {c: sum(r["jurisdiction"] == c for r in valid) for c in countries},
        "source_registry": COUNTRY_SOURCES,
        "methodology": "Counts reflect validated metadata entries, not population-normalized attack rates or independent confirmation.",
    }

def assurance_snapshot(records, as_of=None):
    """Explain geographic source coverage and evidence gaps without fabricating incident counts."""
    report = snapshot(records, as_of=as_of)
    accepted = report["records"]
    coverage = {}
    for country, sources in COUNTRY_SOURCES.items():
        subset = [r for r in accepted if r["jurisdiction"] == country]
        coverage[country] = {
            "registered_official_sources": len(sources),
            "curated_records_in_window": len(subset),
            "verified_source_polling": False,
            "coverage_status": "source_discovery_only",
            "interpretation": "No incident-rate conclusion can be drawn from this registry.",
        }
    review = []
    for record in accepted:
        gaps = []
        if record["evidence_status"] not in {"officially_acknowledged", "independently_corroborated"}:
            gaps.append("incident_not_officially_acknowledged_or_independently_corroborated")
        if record["resolution_status"] != "independently_verified":
            gaps.append("remediation_not_independently_verified")
        if not record.get("relationships"):
            gaps.append("institutional_relationships_not_documented")
        if gaps:
            review.append({"id": record["id"], "gaps": gaps, "review_status": "requires_evidence_review"})
    return {
        "as_of": report["as_of"],
        "window_days": report["window_days"],
        "country_coverage": coverage,
        "evidence_review_queue": review,
        "rejected_records": report["rejected"],
        "methodology": "Source registrations are not active monitoring. Gaps are review prompts, not findings of fault, causality, or attack prevalence.",
    }
