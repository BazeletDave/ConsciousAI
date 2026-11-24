"""Discover official advisory candidates; never promote them to verified incidents."""
import json
import ssl
from datetime import datetime, timezone
from urllib.request import Request, urlopen, build_opener, HTTPRedirectHandler, HTTPSHandler
from urllib.parse import urlsplit
from xml.etree import ElementTree

SOURCE = "https://www.cisa.gov/cybersecurity-advisories/all.xml"
MAX_BYTES = 2_000_000

class NoRedirect(HTTPRedirectHandler):
    def redirect_request(self, *args, **kwargs):
        return None

def parse_candidates(raw):
    if len(raw) > MAX_BYTES or b"<!DOCTYPE" in raw.upper() or b"<!ENTITY" in raw.upper():
        raise ValueError("Unsupported feed")
    root = ElementTree.fromstring(raw)
    if root.tag != "rss" or root.find("channel") is None:
        raise ValueError("Unexpected feed format")
    results = {}
    for item in root.findall("./channel/item")[:100]:
        link = (item.findtext("link") or "").strip()
        title = (item.findtext("title") or "").strip()
        url = urlsplit(link)
        if url.scheme != "https" or url.hostname not in {"www.cisa.gov", "cisa.gov"} or url.username or url.password or not title:
            continue
        results[link] = {"title": title[:500], "url": link, "published": (item.findtext("pubDate") or "")[:100], "classification": "unreviewed_advisory_candidate"}
    return list(results.values())

def collect():
    report = {"checked_at": datetime.now(timezone.utc).isoformat(), "source": SOURCE, "verification": "TLS transport only; incident facts not verified", "candidates": []}
    try:
        opener = build_opener(NoRedirect(), HTTPSHandler(context=ssl.create_default_context()))
        with opener.open(Request(SOURCE, headers={"User-Agent": "GRI research metadata collector"}), timeout=20) as response:
            raw = response.read(MAX_BYTES + 1)
        report["candidates"] = parse_candidates(raw)
        report["status"] = "collected_for_review"
    except Exception as exc:
        report["status"] = "collection_failed"
        report["error_type"] = type(exc).__name__
    return report

if __name__ == "__main__":
    print(json.dumps(collect(), indent=2))
