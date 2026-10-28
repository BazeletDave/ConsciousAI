"""Curated incident research and corpus fitted TF IDF document retrieval.

No student scoring, network access, learned fraud labels, or automatic promotion.
Vectors are fitted only to public institutional reference summaries authored by GRI.
"""
import hashlib
import json
import math
import re
from collections import Counter
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parent
STOP = set("a an the and or of to in for by with as is are from on at not".split())

def tokens(text):
    return [t for t in re.findall(r"[a-z0-9]+", text.lower()) if t not in STOP]

def validate(data):
    if data.get("schema_version") != "1.0" or not isinstance(data.get("records"), list):
        raise ValueError("invalid enrollment research schema")
    seen = set()
    for r in data["records"]:
        for key in ("id", "title", "country", "record_type", "verification", "ai_role", "summary", "source_url", "last_reviewed"):
            if not isinstance(r.get(key), str) or not r[key].strip():
                raise ValueError("missing or invalid " + key)
        if r["id"] in seen or not re.fullmatch(r"[A-Z]{3}", r["country"]):
            raise ValueError("duplicate ID or invalid country")
        seen.add(r["id"])
        u = urlparse(r["source_url"])
        if u.scheme != "https" or not u.hostname or u.username or u.password:
            raise ValueError("invalid public source URL")
        if r.get("contains_personal_data") is not False or r.get("training_eligible") is not False:
            raise ValueError("public research records must exclude personal data and training")
        if type(r.get("retrieval_eligible")) is not bool:
            raise ValueError("explicit retrieval eligibility required")
        if r["retrieval_eligible"] and (r["record_type"] != "institutional_reference" or r["verification"] != "primary_source_reviewed_not_incident_adjudication"):
            raise ValueError("unreviewed or participant record cannot enter retrieval corpus")
    return data

class DocumentIndex:
    """Normalized log TF and smoothed IDF, fitted to eligible summaries."""
    def __init__(self, records):
        self.rows = [r for r in records if r["retrieval_eligible"]]
        docs = [tokens(r["title"] + " " + r["summary"]) for r in self.rows]
        df = Counter(t for doc in docs for t in set(doc))
        self.idf = {t: math.log((1 + len(docs)) / (1 + n)) + 1 for t, n in df.items()}
        self.vectors = [self.vector(doc) for doc in docs]
        self.digest = hashlib.sha256(json.dumps([(r["id"], r["title"], r["summary"]) for r in self.rows], separators=(",", ":")).encode()).hexdigest()

    def vector(self, doc):
        v = {t: (1 + math.log(n)) * self.idf[t] for t, n in Counter(doc).items() if t in self.idf}
        norm = math.sqrt(sum(x*x for x in v.values()))
        return {t: x/norm for t, x in v.items()} if norm else {}

    def search(self, query, country=None):
        q = self.vector(tokens(query))
        matches = []
        for row, v in zip(self.rows, self.vectors):
            score = sum(w * v.get(t, 0) for t, w in q.items())
            if score > 0 and (country is None or row["country"] == country):
                matches.append({"id": row["id"], "title": row["title"], "source_url": row["source_url"], "similarity": round(score, 6), "matched_terms": sorted(set(q) & set(v))})
        return sorted(matches, key=lambda x: (-x["similarity"], x["id"]))

def snapshot(query="", country=None, path=None):
    if not isinstance(query, str) or len(query) > 500:
        raise ValueError("query must be at most 500 characters")
    if country and not re.fullmatch(r"[A-Z]{3}", country):
        raise ValueError("country must be an ISO alpha 3 code")
    data = validate(json.loads((path or ROOT / "enrollment_research.json").read_text(encoding="utf-8")))
    rows = data["records"]
    index = DocumentIndex(rows)
    filtered = [r for r in rows if not country or r["country"] == country]
    return {"schema_version": "1.0", "stream_id": "global_enrollment_identity_fraud", "updated_at": data["updated_at"],
            "status": "curated_research_with_document_retrieval", "collection_mode": "curated_snapshot_no_automatic_global_collection",
            "coverage": {"intended": "global", "countries": sorted({r["country"] for r in rows}), "notice": "Initial sources cover the United States only; counts do not measure prevalence."},
            "selected_country": country, "query": query, "records": filtered,
            "counts": {"records": len(filtered), "attributed_incidents": sum(r["record_type"] == "attributed_incident" for r in filtered), "institutional_references": sum(r["record_type"] == "institutional_reference" for r in filtered)},
            "retrieval": {"model_id": "enrollment-document-tfidf", "version": "1.0", "method": "corpus_fitted_tfidf_cosine", "fitted_documents": len(index.rows), "corpus_digest": index.digest,
                          "evaluation_status": "not_independently_evaluated", "precision": None, "recall": None, "fraud_classifier": False,
                          "matches": index.search(query, country) if query.strip() else [], "notice": "Similarity measures document relevance, not fraud probability or evidence verification. Participant reports are excluded from the fitted corpus."},
            "human_review_required": True, "automated_actions": False}
