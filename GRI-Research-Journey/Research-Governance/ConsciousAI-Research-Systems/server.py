"""GRI local research service. Python 3.10+, standard library only. NOT production-ready."""
from __future__ import annotations
import json
import os
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from assurance_engine import evaluate
from mobility_engine import public_summary
from model_registry import platform_capabilities
from evaluation_pipeline import evaluation_capabilities
from risk_triage import triage
from urllib.parse import urlparse, parse_qs, unquote

ROOT = Path(__file__).resolve().parent
MAX_BODY = 16_384

def load(name):
    with (ROOT / name).open(encoding="utf-8") as f:
        return json.load(f)

def records():
    return load("cases.json")["records"]

def case_by_id(case_id):
    return next((x for x in records() if x["id"] == case_id), None)

def graph():
    nodes = [{"id": x["id"], "label": x["claim"], "organization": x["organization"],
              "type": x["type"], "verification_status": x["verification_status"],
              "source": x["source"]} for x in records()]
    event_records = load("events.json")["records"]
    nodes.extend({"id": e["id"], "label": e["title"], "organization": e["organization"],
                  "type": "event", "verification_status": e["verification_status"],
                  "source": e["primary_source_url"], "claim": e["summary"],
                  "jurisdiction": e["jurisdiction"]} for e in event_records)
    edges = list(load("graph.json")["edges"])
    for e in event_records:
        for linked in e.get("research_links", []):
            edges.append({"source": e["id"], "target": linked, "relation": "research_connection",
                          "evidence_status": "analytical_link_not_causality"})
    valid = {n["id"] for n in nodes}
    if any(e["source"] not in valid or e["target"] not in valid for e in edges):
        raise ValueError("Graph edge references an unknown record")
    return {"nodes": nodes, "edges": edges,
            "notice": "Analytical comparisons do not establish causation or shared systems."}

def assessment(case_id):
    case = case_by_id(case_id)
    if case is None:
        return None
    return {"case_id": case_id, "assessment_type": "evidence_completeness_only",
            "determination": "not_assessed_for_ethics_or_legal_compliance",
            "verification_status": case["verification_status"],
            "known_limitations": [case["limitations"]],
            "review_required": True,
            "notice": "This output is not an ethical certification, compliance determination, or finding of misconduct."}


def assurance_dashboard():
    """Read-only evidence assessment; no synthetic benchmark performance is presented as real."""
    watchlist = load("ai_intelligence.json")
    items = []
    for item in watchlist["records"]:
        # Watchlist publisher homepages are references, not independently reviewed evidence.
        record = {"id": item["id"], "claim": item["summary"],
                  "observed_at": watchlist["updated_at"] + "T00:00:00+00:00",
                  "verification_status": "unreviewed",
                  "sources": [{"publisher": source["name"], "url": source["url"],
                               "independently_reviewed": False} for source in item["sources"]]}
        result = evaluate(record)
        items.append({"id": item["id"], "title": item["title"],
                      "domain": item["domain"], "verification_status": item["verification_status"],
                      "assessment": result})
    return {"schema_version": "1.0", "mode": "research_prototype_read_only",
            "data_origin": "curated_watchlist_not_verified_incident_evidence",
            "evaluated_at": None, "watchlist_updated_at": watchlist["updated_at"],
            "records_assessed": len(items),
            "review_required": sum(x["assessment"]["review_required"] for x in items),
            "eligible_for_human_publication_review": sum(x["assessment"]["decision"] == "eligible_for_human_publication_review" for x in items),
            "accuracy": None, "precision": None, "recall": None,
            "false_positive_rate": None, "false_negative_rate": None,
            "brier_score": None, "drift": None, "bias_evaluation": None,
            "benchmark_status": "not_evaluated_no_independently_labeled_dataset",
            "items": items,
            "notice": "Evidence gating is operational; model performance, fairness and drift are not measured until independent labeled evaluation data are available."}

class Handler(BaseHTTPRequestHandler):
    def send_json(self, status, data):
        payload = json.dumps(data, ensure_ascii=False, indent=2).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Cache-Control", "no-store")
        self.send_header("Access-Control-Allow-Origin", "http://localhost:8000")
        self.send_header("Content-Length", str(len(payload)))
        self.end_headers()
        self.wfile.write(payload)

    def do_HEAD(self):
        path = urlparse(self.path).path
        if path in ("/", "/dashboard", "/dashboard.html", "/health"):
            self.send_response(200)
            self.send_header("Content-Length", "0")
            self.send_header("Cache-Control", "no-store")
            self.end_headers()
        else:
            self.send_response(404)
            self.send_header("Content-Length", "0")
            self.end_headers()

    def do_GET(self):
        path = urlparse(self.path).path
        query = parse_qs(urlparse(self.path).query)
        try:
            if path in ("/dashboard", "/dashboard.html"):
                payload = (ROOT / "dashboard.html").read_bytes()
                self.send_response(200)
                self.send_header("Content-Type", "text/html; charset=utf-8")
                self.send_header("X-Content-Type-Options", "nosniff")
                self.send_header("Content-Length", str(len(payload)))
                self.end_headers()
                self.wfile.write(payload)
                return
            if path == "/intelligence/summary":
                cases = records()
                events = load("events.json")["records"]
                policies = load("policies.json")["records"]
                counts = {}
                for item in cases + events + policies:
                    status = item.get("verification_status", "unspecified")
                    counts[status] = counts.get(status, 0) + 1
                return self.send_json(200, {"schema_version": "1.0",
                    "assessment_type": "registry_inventory_not_independent_verification",
                    "counts": {"cases": len(cases), "events": len(events), "policies": len(policies)},
                    "verification_status_counts": counts,
                    "notice": "Record counts do not establish independent verification, legal compliance, or causation."})
            if path == "/assurance/overview":
                return self.send_json(200, assurance_dashboard())
            if path == "/intelligence/triage":
                items = load("events.json")["records"]
                return self.send_json(200, {"schema_version": "1.3", "method": "deterministic_missing_evidence_heuristic", "records": [triage(item) for item in items], "count": len(items), "notice": "Research triage only; no trained model or compliance determination."})
            if path == "/ai-intelligence":
                return self.send_json(200, load("ai_intelligence.json"))
            if path == "/events":
                return self.send_json(200, load("events.json"))
            if path == "/policy-sources":
                return self.send_json(200, load("policy_sources.json"))
            if path == "/platform/evaluation":
                return self.send_json(200, evaluation_capabilities())
            if path == "/platform/capabilities":
                return self.send_json(200, platform_capabilities())
            if path == "/mobility/summary":
                return self.send_json(200, public_summary())
            if path == "/health":
                return self.send_json(200, {"status": "ok", "service": "GRI local research prototype"})
            if path == "/cases":
                items = records()
                if "organization" in query:
                    items = [x for x in items if x["organization"].casefold() == query["organization"][0].casefold()]
                return self.send_json(200, {"records": items, "count": len(items)})
            if path.startswith("/cases/"):
                case = case_by_id(unquote(path[len("/cases/"):]))
                return self.send_json(200 if case else 404, case or {"error": "unknown_case"})
            if path == "/graph":
                return self.send_json(200, graph())
            if path == "/policies":
                return self.send_json(200, load("policies.json"))
            if path == "/":
                return self.send_json(200, {"service": "GRI Research Systems", "endpoints": ["/health", "/cases", "/graph", "/policies", "/events", "/assurance/overview", "/ai-intelligence", "/policy-sources", "/dashboard", "POST /assessments"], "deployment": "local_prototype"})
            return self.send_json(404, {"error": "unknown_route"})
        except (ValueError, OSError, KeyError, json.JSONDecodeError):
            return self.send_json(500, {"error": "invalid_research_data"})

    def do_POST(self):
        if urlparse(self.path).path != "/assessments":
            return self.send_json(404, {"error": "unknown_route"})
        length = self.headers.get("Content-Length")
        if not length or not length.isdecimal() or int(length) > MAX_BODY:
            return self.send_json(413, {"error": "invalid_or_excessive_body"})
        if self.headers.get("Content-Type", "").split(";")[0].strip().lower() != "application/json":
            return self.send_json(415, {"error": "json_required"})
        try:
            body = json.loads(self.rfile.read(int(length)))
        except (json.JSONDecodeError, UnicodeDecodeError):
            return self.send_json(400, {"error": "invalid_json"})
        if not isinstance(body, dict) or not isinstance(body.get("case_id"), str):
            return self.send_json(400, {"error": "case_id_required"})
        result = assessment(body["case_id"])
        return self.send_json(200 if result else 404, result or {"error": "unknown_case"})

if __name__ == "__main__":
    host = os.environ.get("GRI_HOST", "127.0.0.1")
    port = int(os.environ.get("PORT", os.environ.get("GRI_PORT", "8000")))
    print(f"GRI local research prototype at http://{host}:{port}", flush=True)
    ThreadingHTTPServer((host, port), Handler).serve_forever()
