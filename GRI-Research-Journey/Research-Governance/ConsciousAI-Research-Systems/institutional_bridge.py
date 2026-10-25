"""Read-only bridge from validated GRI research engineering to the public dashboard.
No model promotion, agent execution, publication, or storage mutation.
"""
from pathlib import Path
import sys

ENGINEERING = Path(__file__).resolve().parents[2] / "engineering"

def research_snapshot():
    if not ENGINEERING.is_dir():
        return {"status":"unavailable","reason":"research engineering directory missing"}
    path = str(ENGINEERING)
    if path in sys.path:
        sys.path.remove(path)
    sys.path.insert(0,path)
    sys.modules.pop("model_registry", None)
    from intelligence_graph import IntelligenceGraph
    from agent_control import authorize
    from model_registry import ModelRegistry
    from release_gate import assess_release
    graph = IntelligenceGraph()
    graph.add_node("research","research_case","GRI institutional intelligence research")
    graph.add_node("governance","institution","GRI governance research")
    graph.add_edge("governance","research","relates_to","0"*64,inferred=True)
    candidate = ModelRegistry().register("governance-research-baseline","research-0.1",
                                         {"accuracy":0.0},benchmark_eligible=False)
    control = authorize({"agent_id":"research-agent","allowed_actions":["publish"]},
                        {"agent_id":"research-agent","action":"publish"})
    release = assess_release({})
    return {"schema_version":"1.0","status":"research_modules_loaded",
            "mode":"read_only_research_integration","graph_nodes":len(graph.nodes),
            "graph_relationships":len(graph.edges),"graph_verification":"synthetic_example_not_source_verified",
            "model_state":candidate["state"],"model_metrics":"synthetic_fixture_not_performance",
            "model_promotion_authorized":candidate["promotion_authorized"],
            "agent_decision":control["decision"],"agent_executed":control["execution_performed"],
            "release_checklist_complete":release["checklist_complete"],
            "deployment_authorized":release["deployment_authorized"],
            "notice":"Live module wiring is verified by this read-only endpoint. Counts are synthetic integration fixtures, not independently validated research observations."}
