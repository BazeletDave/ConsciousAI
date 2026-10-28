"""Versioned public research retrieval and isolated topic learning candidates.

No network, private course materials, automatic publication or model promotion.
"""
from collections import Counter
from datetime import datetime, timezone
from hashlib import sha256
import json
import math
import os
from pathlib import Path
import re
import tempfile

from country_topics import TopicModel, EXAMPLES, tokens

ROOT = Path(__file__).resolve().parent
REPO = ROOT.parents[2]
OUTPUT = ROOT / "country_intelligence/research_evolution.json"
SCOPES = ("GRI-Research-Journey", "Research-Journey", "research", "autonomous-mobility-research")
BASE = "https://github.com/BazeletDave/ConsciousAI/blob/main/"
TERM_MAP = {"brasil": "brazil", "inteligencia": "intelligence", "governanca": "governance",
            "algoritmica": "algorithmic", "algoritmos": "algorithmic", "comercio": "trade",
            "eleicoes": "election", "elecciones": "election", "trabalho": "labor"}


def retrieval_terms(text):
    return [TERM_MAP.get(t, t) for t in tokens(text)]


def digest(value):
    return sha256(json.dumps(value, sort_keys=True, ensure_ascii=False).encode()).hexdigest()


def catalog(repo=REPO):
    rows = []
    candidates = sorted({p for scope in SCOPES for p in (repo / scope).rglob("*.md")})
    for path in candidates:
        if path.is_symlink() or not path.resolve().is_relative_to(repo.resolve()):
            continue
        relative = path.relative_to(repo).as_posix()
        if re.search(r"syllabus|assignment|exam|answer.?key|source_snapshots|private|restricted|appendix-a-interview", relative, re.I) or path.stat().st_size > 2_000_000:
            continue
        text = path.read_text(encoding="utf-8")
        title = next((x.lstrip("# ").strip() for x in text.splitlines() if x.startswith("# ")), path.stem)[:200]
        rows.append({"path": relative, "title": title, "content_sha256": sha256(text.encode()).hexdigest(),
                     "url": BASE + relative.replace(" ", "%20"),
                     "status": "public_repository_document_not_independently_validated"})
    return rows[:500], len(rows) > 500


def connect(records, documents):
    """TF-IDF cosine similarity over titles; associations are proposed, not facts."""
    document_tokens = [Counter(retrieval_terms(d["title"])) for d in documents]
    frequency = Counter(t for row in document_tokens for t in row)
    idf = {t: math.log((len(documents) + 1) / (count + 1)) + 1 for t, count in frequency.items()}
    vectors = [{t: n * idf[t] for t, n in row.items()} for row in document_tokens]
    norms = [math.sqrt(sum(v * v for v in row.values())) for row in vectors]
    links = []
    for record in records:
        geography = " ".join({"BRA": "Brazil", "ISR": "Israel", "USA": "United States"}.get(c, "") for c in record.get("country_codes", []))
        counts = Counter(retrieval_terms(record["title"] + " " + geography))
        query = {t: n * idf[t] for t, n in counts.items() if t in idf}
        norm = math.sqrt(sum(v * v for v in query.values()))
        ranked = []
        for doc, vector, docnorm in zip(documents, vectors, norms):
            overlap = query.keys() & vector.keys()
            score = sum(query[t] * vector[t] for t in overlap) / (norm * docnorm) if norm and docnorm else 0
            if len(overlap) >= 2 and score >= 0.12:
                ranked.append(dict(doc, similarity=round(score, 4),
                                   relation="suggested_research_connection_not_causation"))
        ranked.sort(key=lambda x: (-x["similarity"], x["path"]))
        if ranked:
            links.append({"record_id": record["id"], "content_sha256": record["content_sha256"], "research": ranked[:3]})
    return links


def learning_candidate(feedback, records):
    """Only fit a separate candidate from recorded review and rights-cleared data.

    Review fields are repository records, not authenticated independent assurance.
    Active model parameters are never changed by this function.
    """
    lookup = {r["id"]: r for r in records}
    accepted, rejected, seen = [], 0, set()
    for row in feedback:
        record = lookup.get(row.get("record_id")) if isinstance(row, dict) else None
        valid = (record and record["id"] not in seen and row.get("content_sha256") == record["content_sha256"]
                 and row.get("label") in EXAMPLES and row.get("split") in ("train", "holdout")
                 and row.get("review_status") == "approved" and row.get("training_rights") == "cleared"
                 and isinstance(row.get("reviewed_by"), str) and row["reviewed_by"].strip())
        if valid:
            accepted.append((row, record)); seen.add(record["id"])
        else:
            rejected += 1
    train = [(a, b) for a, b in accepted if a["split"] == "train"]
    holdout = [(a, b) for a, b in accepted if a["split"] == "holdout"]
    reasons = []
    if any(sum(a["label"] == label for a, _ in train) < 10 for label in EXAMPLES):
        reasons.append("requires_ten_reviewed_training_records_per_topic")
    if any(sum(a["label"] == label for a, _ in holdout) < 5 for label in EXAMPLES):
        reasons.append("requires_five_reviewed_holdout_records_per_topic")
    if {b["source_id"] for _, b in train} & {b["source_id"] for _, b in holdout}:
        reasons.append("train_holdout_source_overlap")
    if {tuple(tokens(b["title"])) for _, b in train} & {tuple(tokens(b["title"])) for _, b in holdout}:
        reasons.append("train_holdout_text_overlap")
    if {a["reviewed_by"] for a, _ in train} & {a["reviewed_by"] for a, _ in holdout}:
        reasons.append("requires_separate_recorded_holdout_reviewers")
    try:
        def observed(record):
            value = datetime.fromisoformat(record["first_seen_at"].replace("Z", "+00:00"))
            if value.tzinfo is None:
                raise ValueError("Timezone required")
            return value
        if train and holdout and max(observed(b) for _, b in train) >= min(observed(b) for _, b in holdout):
            reasons.append("requires_chronological_holdout")
    except (KeyError, ValueError, TypeError):
        reasons.append("requires_valid_observation_times")
    result = {"status": "blocked" if reasons else "candidate_evaluated_not_promoted",
              "accepted_records": len(accepted), "rejected_records": rejected, "blocking_reasons": reasons,
              "active_model_updated": False, "independent_review_authenticated": False,
              "promotion": "requires_separate_validated_and_authorized_release",
              "feedback_sha256": digest(feedback), "candidate_accuracy": None, "baseline_accuracy": None}
    if not reasons:
        examples = {label: [b["title"] for a, b in train if a["label"] == label] for label in EXAMPLES}
        candidate, baseline = TopicModel(examples), TopicModel()
        result.update(candidate_training_sha256=candidate.training_sha256,
                      candidate_accuracy=sum(candidate.predict(b["title"])["label"] == a["label"] for a, b in holdout) / len(holdout),
                      baseline_accuracy=sum(baseline.predict(b["title"])["label"] == a["label"] for a, b in holdout) / len(holdout))
    return result


def build(repo=REPO, feed=None, feedback=None, previous=None, now=None):
    documents, truncated = catalog(repo)
    feed, previous = feed or {}, previous or {}
    old = {d["path"]: d["content_sha256"] for d in previous.get("documents", [])}
    current = {d["path"]: d["content_sha256"] for d in documents}
    connections = connect(feed.get("records", []), documents)
    return {"schema_version": "1.0", "generated_at": now or datetime.now(timezone.utc).isoformat(),
            "mode": "evolving_repository_retrieval_with_governed_learning_candidates",
            "catalog_sha256": digest(documents), "document_count": len(documents), "truncated": truncated,
            "changes": {"added": sorted(current.keys() - old.keys()), "removed": sorted(old.keys() - current.keys()),
                        "revised": sorted(k for k in current.keys() & old.keys() if current[k] != old[k])},
            "documents": documents, "evidence_connections": connections, "connected_records": len(connections),
            "learning_candidate": learning_candidate(feedback or [], feed.get("records", [])),
            "active_topic_model": "fixed_instructional_baseline_no_automatic_promotion",
            "notice": "Repository indexing and research retrieval evolve with committed documents. Similarity is not factual verification or causation. No access to private chats, course systems or other repositories is implied. Academic references do not imply university endorsement."}


def load():
    try:
        return json.loads(OUTPUT.read_text(encoding="utf-8"))
    except FileNotFoundError:
        return {"status": "awaiting_first_index", "documents": [], "evidence_connections": []}


def main():
    feed = json.loads((ROOT / "country_intelligence/feed.json").read_text(encoding="utf-8"))
    feedback = json.loads((ROOT / "country_intelligence/topic_feedback.json").read_text(encoding="utf-8"))["records"]
    result = build(feed=feed, feedback=feedback, previous=load())
    with tempfile.NamedTemporaryFile("w", dir=OUTPUT.parent, encoding="utf-8", delete=False) as handle:
        json.dump(result, handle, ensure_ascii=False, indent=2); handle.write("\n"); name = handle.name
    os.replace(name, OUTPUT)
    print(json.dumps({"documents": result["document_count"], "connected_records": result["connected_records"], "candidate": result["learning_candidate"]["status"]}))


if __name__ == "__main__":
    main()

