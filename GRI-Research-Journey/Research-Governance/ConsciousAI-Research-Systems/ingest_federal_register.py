"""Collect official US Federal Register metadata into a review queue.

Python standard library only. Does not certify legal interpretation.
"""
import argparse
import json
import os
import tempfile
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlencode
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parent
API = "https://www.federalregister.gov/api/v1/documents.json"
QUEUE = ROOT / "policy_candidates.json"
TERMS = ("artificial intelligence", "machine learning", "automated decision")
MAX_RESULTS_PER_TERM = 20

def collect(fetch=None, now=None):
    if fetch is None:
        def fetch(url):
            with urlopen(Request(url, headers={"User-Agent": "GRI-Research-Policy-Monitor/0.1 (research)"}), timeout=25) as response:
                return json.load(response)
    now = now or datetime.now(timezone.utc).isoformat()
    entries = {}
    for term in TERMS:
        params = urlencode({"conditions[term]": term, "per_page": MAX_RESULTS_PER_TERM, "order": "newest"})
        payload = fetch(API + "?" + params)
        for doc in payload.get("results", []):
            number = doc.get("document_number")
            url = doc.get("html_url")
            if not number or not url or not url.startswith("https://www.federalregister.gov/"):
                continue
            entries[number] = {
                "id": "US-FR-" + number,
                "jurisdiction": "United States",
                "issuing_authority": "Office of the Federal Register",
                "title": doc.get("title", ""),
                "instrument_type": doc.get("type", "unknown"),
                "publication_date": doc.get("publication_date"),
                "document_number": number,
                "official_source_url": url,
                "official_pdf_url": doc.get("pdf_url"),
                "abstract": (doc.get("abstract") or "")[:1800],
                "verification_status": "official_api_metadata_unreviewed",
                "first_seen_at": now,
                "last_seen_at": now,
                "review_required": True,
                "source_api": API,
            }
    return entries

def merge(existing, incoming):
    by_id = {r["id"]: r for r in existing.get("records", [])}
    for row in incoming.values():
        prior = by_id.get(row["id"])
        if prior:
            row["first_seen_at"] = prior.get("first_seen_at", row["first_seen_at"])
            row["verification_status"] = prior.get("verification_status", row["verification_status"])
            row["review_required"] = prior.get("review_required", True)
        by_id[row["id"]] = row
    return {"schema_version": "0.1", "status": "official_api_metadata_pending_human_review",
            "last_collection_at": datetime.now(timezone.utc).isoformat(),
            "records": sorted(by_id.values(), key=lambda x: (x.get("publication_date") or "", x["id"]), reverse=True)[:500]}

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    incoming = collect()
    existing = json.loads(QUEUE.read_text()) if QUEUE.exists() else {"records": []}
    result = merge(existing, incoming)
    if not args.dry_run:
        with tempfile.NamedTemporaryFile("w", encoding="utf-8", dir=ROOT, delete=False) as tmp:
            json.dump(result, tmp, indent=2)
            tmp.write("\n")
            path = tmp.name
        os.replace(path, QUEUE)
    print(json.dumps({"newly_fetched": len(incoming), "total_queue": len(result["records"]),
                      "dry_run": args.dry_run}))

if __name__ == "__main__":
    main()
