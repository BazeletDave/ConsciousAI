"""Institutional case explorer built only from the existing public research registry.

Do not infer independent verification from a registry entry, a source path, or an
analytical graph link. No private course material or student assessment is served.
"""
from pathlib import Path
import json

ROOT = Path(__file__).resolve().parent

def public_case_explorer():
    cases=json.loads((ROOT/"cases.json").read_text(encoding="utf-8"))["records"]
    events=json.loads((ROOT/"events.json").read_text(encoding="utf-8"))["records"]
    by_id={case["id"]:case for case in cases}
    connections={key:[] for key in by_id}
    for event in events:
        for key in event.get("research_links",[]):
            if key in connections:
                connections[key].append({"id":event["id"],"title":event["title"],
                    "source_url":event.get("primary_source_url"),
                    "verification_status":event.get("verification_status"),
                    "relation":"analytical_research_link_not_causation"})
    rows=[]
    for case in cases:
        source=case.get("source","")
        rows.append({"id":case["id"],"organization":case.get("organization"),
            "research_type":case.get("type"),"claim":case.get("claim"),
            "verification_status":case.get("verification_status","unspecified"),
            "limitations":case.get("limitations","Not specified"),
            "source_reference":source,
            "source_kind":"public_url" if source.startswith("https://") else "repository_reference",
            "related_public_events":connections[case["id"]],
            "independent_validation":"not_established"})
    return {"schema_version":"1.0","mode":"public_registry_read_only",
        "count":len(rows),"records":rows,
        "research_principles":["evidence provenance","human review","contestability",
            "institutional accountability","documented limitations"],
        "notice":"These are registry claims and analytical links, not independently validated findings, course assessments, or legal determinations."}
