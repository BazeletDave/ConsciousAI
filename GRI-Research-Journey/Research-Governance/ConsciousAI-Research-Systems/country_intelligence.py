"""Source governed country intelligence collection and dashboard snapshots.

Publisher metadata is collected for review. No sentiment, ideology, election
prediction, legal status inference, or causal business impact is asserted.
"""
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
from email.utils import parsedate_to_datetime
from hashlib import sha256
from html.parser import HTMLParser
import json
import os
from pathlib import Path
import re
import tempfile
import socket
from urllib.error import HTTPError, URLError
from urllib.parse import urlparse
from urllib.request import Request, build_opener, HTTPRedirectHandler
from xml.etree import ElementTree as ET

from country_topics import TopicModel, normalize

ROOT = Path(__file__).resolve().parent
DATA = ROOT / "country_intelligence"
MAX_BYTES = 2_000_000
SOURCES = [
    {"id": "USA-FEDERAL-REGISTER", "publisher": "Office of the Federal Register", "url": "https://www.federalregister.gov/api/v1/documents.json", "host": "www.federalregister.gov", "mode": "federal_register_snapshot", "country": "USA"},
    {"id": "WTO", "publisher": "WTO news", "url": "https://www.wto.org/library/rss/latest_news_e.xml", "host": "www.wto.org", "mode": "rss", "country": None},
    {"id": "UN-AMERICAS", "publisher": "UN News", "url": "https://news.un.org/feed/subscribe/en/news/region/americas/feed/rss.xml", "host": "news.un.org", "mode": "rss", "country": None},
    {"id": "BRA-MDIC", "publisher": "Brazil Ministry of Development, Industry, Trade and Services", "url": "https://www.gov.br/mdic/pt-br/assuntos/noticias/ultimas-noticias/@@RSS", "host": "www.gov.br", "mode": "rss", "country": "BRA", "article_path": r"/mdic/pt-br/assuntos/noticias/\d{4}/[^/]+/[^/]+"},
    {"id": "BRA-CAMARA", "publisher": "Brazil Chamber of Deputies", "url": "https://dadosabertos.camara.leg.br/api/v2/proposicoes?keywords=intelig%C3%AAncia%20artificial&ordem=DESC&ordenarPor=id&itens=30", "host": "dadosabertos.camara.leg.br", "mode": "camara", "country": "BRA"},
    {"id": "UN-MIDDLE-EAST", "publisher": "UN News", "url": "https://news.un.org/feed/subscribe/en/news/region/middle-east/feed/rss.xml", "host": "news.un.org", "mode": "rss", "country": None},
    {"id": "ISR-BOI-FORECAST", "publisher": "Bank of Israel", "url": "https://boi.org.il/en/communication-and-publications/press-releases/21-10-26-aen/", "host": "boi.org.il", "mode": "official_document", "country": "ISR", "expected_title": "Research Department Staff Forecast"},
    {"id": "ISR-CEC-DIGITAL", "publisher": "Israel Central Elections Committee", "url": "https://www.gov.il/en/pages/dover_21", "host": "www.gov.il", "mode": "official_document", "country": "ISR", "expected_title": "26th Knesset"},
]
CHANNELS = {
    "political_institutions": "Review governing authority, coalition support, institutional constraints and effective dates.",
    "trade_investment": "Review market access, tariffs, investment rules and supply chain exposure.",
    "organizational_management": "Review operating requirements, workforce capabilities and managerial discretion.",
    "algorithmic_management": "Review automated workplace decisions, platform labor protections and appeal mechanisms.",
    "artificial_intelligence": "Review AI rules, adoption, procurement, compute infrastructure and accountable authority.",
}
US_TERMS = ("artificial intelligence", "machine learning", "automated", "algorithm", "algorithmic", "platform", "workforce", "labor", "employment", "trade", "tariff", "investment", "export", "import", "election", "electoral", "voting", "autonomous", "vehicle", "transportation")


class PlainText(HTMLParser):
    def __init__(self):
        super().__init__()
        self.parts = []

    def handle_data(self, text):
        self.parts.append(text)


class DocumentTitle(HTMLParser):
    def __init__(self):
        super().__init__()
        self.in_title = False
        self.parts = []

    def handle_starttag(self, tag, attrs):
        if tag == "title":
            self.in_title = True

    def handle_endtag(self, tag):
        if tag == "title":
            self.in_title = False

    def handle_data(self, text):
        if self.in_title:
            self.parts.append(text)


def plain(text, limit=350):
    parser = PlainText()
    parser.feed(str(text or ""))
    return " ".join(" ".join(parser.parts).split())[:limit]


def permitted(url, host):
    p = urlparse(url)
    return p.scheme == "https" and p.hostname == host and p.port in (None, 443) and not p.username and not p.password


class TrustedRedirect(HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        if not permitted(newurl, urlparse(req.full_url).hostname):
            raise ValueError("Redirect outside configured publisher")
        return super().redirect_request(req, fp, code, msg, headers, newurl)


def fetch(source):
    if not permitted(source["url"], source["host"]):
        raise ValueError("Invalid source")
    request = Request(source["url"], headers={"User-Agent": "GRI-Country-Research/0.1", "Accept": "application/json, application/rss+xml, application/atom+xml, application/xml, text/xml, */*;q=0.1"})
    with build_opener(TrustedRedirect()).open(request, timeout=15) as response:
        if not permitted(response.url, source["host"]):
            raise ValueError("Invalid response host")
        raw = response.read(MAX_BYTES + 1)
        if len(raw) > MAX_BYTES:
            raise ValueError("Response exceeds collection bound")
        return raw


def fetch_with_recovery(source, fetcher):
    """Retry one transient transport failure; never retry access or validation blocks."""
    for attempt in range(2):
        try:
            return fetcher(source), attempt + 1
        except (OSError, URLError) as error:
            transient = (isinstance(error, HTTPError) and error.code in (500, 502, 503, 504)) or (
                not isinstance(error, HTTPError) and (
                    isinstance(error, (TimeoutError, socket.timeout, ConnectionError)) or
                    isinstance(getattr(error, "reason", None), (TimeoutError, socket.timeout, ConnectionError))))
            if not transient or attempt:
                raise


def publication_time(value):
    if not value:
        return None
    try:
        date = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        try:
            date = parsedate_to_datetime(value)
        except (ValueError, TypeError):
            return None
    return date.astimezone(timezone.utc).isoformat() if date.tzinfo else None


def parse(raw, source):
    if source["mode"] == "federal_register_snapshot":
        data = json.loads(raw)
        if not isinstance(data, dict) or not isinstance(data.get("records"), list):
            raise ValueError("Invalid Federal Register snapshot")
        collected = datetime.fromisoformat(data["last_collection_at"].replace("Z", "+00:00"))
        if collected.tzinfo is None:
            raise ValueError("Collection timestamp requires a timezone")
        rows = []
        for item in data["records"]:
            if not isinstance(item, dict):
                continue
            text = str(item.get("title") or "") + " " + str(item.get("abstract") or "")
            matches = [term for term in US_TERMS if re.search(r"(?<!\w)" + re.escape(term) + r"(?:s|ed|ing)?(?!\w)", normalize(text))]
            if not matches:
                continue
            kind = str(item.get("instrument_type") or "unknown")
            legal = "proposed_rule_not_final" if kind.casefold() in ("proposed rule", "prorule") else "notice_not_a_final_rule" if kind.casefold() == "notice" else "document_type_reported_effective_status_requires_review"
            rows.append({"title": plain(item.get("title")), "source_url": item.get("official_source_url", ""),
                         "published_at": None, "publication_date": item.get("publication_date"),
                         "source_observed_at": item.get("last_seen_at", data["last_collection_at"]),
                         "document_type": "federal_register_metadata", "instrument_type": kind,
                         "publishing_office": item.get("issuing_authority"), "legal_status": legal,
                         "document_number": item.get("document_number"), "triage_terms": matches,
                         "classification_input_sha256": sha256(text.encode()).hexdigest(),
                         "_classification_text": text})
    elif source["mode"] == "official_document":
        parser = DocumentTitle()
        parser.feed(raw.decode("utf-8", "replace"))
        title = plain(" ".join(parser.parts))
        if normalize(source["expected_title"]) not in normalize(title):
            raise ValueError("Expected official document title absent; possible access wall")
        rows = [{"title": title, "source_url": source["url"], "published_at": None,
                 "document_type": "fixed_official_document_metadata", "legal_status": "not_assessed"}]
    elif source["mode"] == "camara":
        data = json.loads(raw)
        if not isinstance(data, dict) or not isinstance(data.get("dados"), list):
            raise ValueError("Invalid Chamber response")
        rows = [{"title": plain(f"{r['siglaTipo']} {r['numero']}/{r['ano']}: {r['ementa']}"),
                 "source_url": r["uri"], "published_at": None,
                 "document_type": "legislative_proposal_metadata",
                 "legal_status": "proposal_record_not_evidence_of_enactment"}
                for r in data["dados"] if isinstance(r, dict)]
    else:
        root = ET.fromstring(raw)
        if root.tag.rsplit("}", 1)[-1] not in ("rss", "RDF", "feed"):
            raise ValueError("Publisher did not return a feed")
        rows = []
        for node in root.iter():
            if node.tag.rsplit("}", 1)[-1] not in ("item", "entry"):
                continue
            fields = {}
            for child in node:
                key = child.tag.rsplit("}", 1)[-1]
                value = "".join(child.itertext()).strip()
                if key == "link" and child.get("href"):
                    if child.get("rel", "alternate") != "alternate":
                        continue
                    value = child.get("href")
                fields.setdefault(key, value)
            rows.append({"title": plain(fields.get("title")), "source_url": fields.get("link", ""),
                         "published_at": publication_time(fields.get("pubDate") or fields.get("published") or fields.get("date")),
                         "document_type": "publisher_news_metadata", "legal_status": "not_assessed"})
    return [r for r in rows if r["title"] and permitted(r["source_url"], source["host"])
            and (not source.get("article_path") or re.fullmatch(source["article_path"], urlparse(r["source_url"]).path.rstrip("/")))][:250 if source["mode"] == "federal_register_snapshot" else 60]


def country_mentions(title, countries):
    text = normalize(title)
    return [c["code"] for c in countries if any(re.search(r"(?<!\w)" + re.escape(normalize(alias)) + r"(?!\w)", text) for alias in c["aliases"])]


def collect(previous=None, fetcher=fetch, sources=None, countries=None, now=None):
    now = now or datetime.now(timezone.utc).isoformat()
    sources = SOURCES if sources is None else sources
    countries = load_catalog()["countries"] if countries is None else countries
    previous = previous or {}
    prior = {r["id"]: r for r in previous.get("records", [])}
    source_prior = {s["id"]: s for s in previous.get("sources", [])}
    exclusions = list(previous.get("quality_exclusions", []))
    for source in sources:
        if source.get("article_path"):
            for identity, row in list(prior.items()):
                if row["source_id"] == source["id"] and not re.fullmatch(source["article_path"], urlparse(row["source_url"]).path.rstrip("/")):
                    exclusions.append({"record_id": identity, "source_id": source["id"], "reason": "directory_or_nonarticle_path", "observed_at": now})
                    del prior[identity]
    model = TopicModel()
    health, seen, changes = [], set(), []

    def retrieve(source):
        try:
            raw = (ROOT / "policy_candidates.json").read_bytes() if source["mode"] == "federal_register_snapshot" else fetch_with_recovery(source, fetcher)[0]
            collected_at = json.loads(raw)["last_collection_at"] if source["mode"] == "federal_register_snapshot" else now
            return source, parse(raw, source), sha256(raw).hexdigest(), None, collected_at, None
        except (OSError, ValueError, KeyError, TypeError, ET.ParseError) as error:
            return source, [], None, type(error).__name__, None, ("expected_document_not_returned" if source["mode"] == "official_document" and isinstance(error, ValueError) and str(error).startswith("Expected official document title absent") else "source_response_unavailable_or_invalid")

    with ThreadPoolExecutor(max_workers=4) as pool:
        for source, rows, digest, error, collected_at, reason in pool.map(retrieve, sources):
            prior_health = source_prior.get(source["id"], {})
            health.append({"id": source["id"], "publisher": source["publisher"], "url": source["url"],
                           "status": "failed" if error else "fetched" if rows else "empty",
                           "items": len(rows), "attempted_at": now,
                           "last_success_at": prior_health.get("last_success_at") if error else collected_at,
                           "collection_method": source["mode"],
                           "response_sha256": digest, "error_type": error,
                           "availability_reason": reason, "recheck_policy": "next_scheduled_collection" if error else None})
            for row in rows:
                classification_text = row.pop("_classification_text", row["title"])
                codes = sorted(set(country_mentions(row["title"], countries) + ([source["country"]] if source.get("country") else [])))
                if not codes:
                    continue
                identity = sha256((source["id"] + "|" + row["source_url"]).encode()).hexdigest()[:24]
                fingerprint = sha256(json.dumps(row, sort_keys=True, ensure_ascii=False).encode()).hexdigest()
                old = prior.get(identity)
                changed = bool(old and old["content_sha256"] != fingerprint)
                record = dict(row, id=identity, source_id=source["id"], publisher=source["publisher"],
                              country_codes=codes, country_assignment="publisher_jurisdiction_or_title_mention_requires_review",
                              topic=model.predict(classification_text), content_sha256=fingerprint,
                              previous_content_sha256=old["content_sha256"] if changed else (old or {}).get("previous_content_sha256"),
                              first_seen_at=(old or {}).get("first_seen_at", now), last_seen_at=now,
                              content_changed_at=now if changed else (old or {}).get("content_changed_at"),
                              change_count=(old or {}).get("change_count", 0) + int(changed),
                              review_status="unreviewed", human_review_required=True, publication_authorized=False,
                              political_direction=None, causal_impact=None)
                prior[identity] = record
                seen.add(identity)
                if not old or changed:
                    changes.append({"record_id": identity, "kind": "metadata_changed" if changed else "newly_discovered", "observed_at": now})
    records = sorted(prior.values(), key=lambda r: (r["last_seen_at"], r["id"]), reverse=True)[:1000]
    return {"schema_version": "1.0", "generated_at": now, "mode": "publisher_metadata_with_experimental_ml_topic_triage",
            "collection_status": "all_sources_failed" if health and all(s["status"] == "failed" for s in health) else "partial_failure" if any(s["status"] == "failed" for s in health) else "completed",
            "sources": health, "records": records, "changes": changes,
            "quality_exclusions": exclusions[-100:],
            "retention_limit": 1000, "collection_count": len(seen), "model": model.evaluation(),
            "notice": "Country mentions and ML topics are review candidates. New discovery is not a new political event. No ideology, election outcome, legal force, or causal economic impact is inferred."}


def load_catalog():
    return json.loads((DATA / "countries.json").read_text(encoding="utf-8"))


def read_feed():
    try:
        data = json.loads((DATA / "feed.json").read_text(encoding="utf-8"))
        if not isinstance(data.get("records"), list) or not isinstance(data.get("sources"), list):
            raise ValueError("Invalid snapshot")
        return data
    except FileNotFoundError:
        return {"schema_version": "1.0", "generated_at": None, "sources": [], "records": [], "changes": [], "status": "awaiting_first_collection"}


def snapshot(code=None, topic=None):
    catalog = load_catalog()
    countries = catalog["countries"]
    if code and code not in {c["code"] for c in countries}:
        raise LookupError("Unknown country code")
    if topic and topic not in CHANNELS and topic != "needs_review":
        raise ValueError("Unknown topic")
    data = read_feed()
    all_records = data.get("records", [])
    selected = [r for r in all_records if (not code or code in r["country_codes"]) and (not topic or r["topic"]["label"] == topic)]
    from research_evolution import load as load_evolution
    evolution = load_evolution()
    links = {(x["record_id"], x["content_sha256"]): x["research"] for x in evolution.get("evidence_connections", [])}
    selected = [dict(r, related_research=links.get((r["id"], r["content_sha256"]), [])) for r in selected]
    counts = {c["code"]: sum(c["code"] in r["country_codes"] for r in all_records) for c in countries}
    return dict(data, records=selected, count=len(selected),
                research_evolution={k: v for k, v in evolution.items() if k not in ("documents", "evidence_connections")},
                countries=[dict(c, record_count=counts[c["code"]]) for c in countries],
                selected_country=code, selected_topic=topic, channels=CHANNELS,
                comparative_research=json.loads((DATA / "comparative_research.json").read_text(encoding="utf-8")),
                coverage="South America pilot with Israel and United States comparative cases; limited publisher coverage, not comprehensive worldwide monitoring",
                brazil_research_url="https://github.com/BazeletDave/ConsciousAI/blob/main/GRI-Research-Journey/Integrated-Research-Journey/2026-10-23-brazil-election-ai-platform-governance-tam505.md")


def main():
    path = DATA / "feed.json"
    previous = read_feed()
    result = collect(previous)
    # Preserve prior records and last success times even on complete collection failure.
    DATA.mkdir(exist_ok=True)
    with tempfile.NamedTemporaryFile("w", dir=DATA, encoding="utf-8", delete=False) as handle:
        json.dump(result, handle, ensure_ascii=False, indent=2)
        handle.write("\n")
        temporary = handle.name
    os.replace(temporary, path)
    print(json.dumps({"records": len(result["records"]), "changes": len(result["changes"]), "sources": result["sources"]}))
    if result["collection_status"] == "all_sources_failed":
        raise RuntimeError("All sources failed; prior evidence retained and failure recorded")


if __name__ == "__main__":
    main()
