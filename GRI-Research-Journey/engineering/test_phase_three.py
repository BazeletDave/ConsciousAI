import unittest
from intelligence_graph import IntelligenceGraph
from agent_control import authorize
from model_registry import ModelRegistry

class PhaseThreeTests(unittest.TestCase):
    def test_graph_provenance(self):
        g = IntelligenceGraph()
        g.add_node("institution1", "institution", "Synthetic Institution")
        g.add_node("case1", "research_case", "Synthetic Case")
        edge = g.add_edge("institution1", "case1", "relates_to", "a" * 64, inferred=True)
        self.assertTrue(edge["inferred"])
        self.assertFalse(edge["verified"])
        self.assertFalse(g.snapshot()["publication_authorized"])

    def test_graph_missing_provenance(self):
        g = IntelligenceGraph()
        g.add_node("a", "actor", "A")
        g.add_node("b", "policy", "B")
        with self.assertRaises(ValueError):
            g.add_edge("a", "b", "governs", "not-a-digest")

    def test_agent_restricted_action_denied(self):
        cap = {"agent_id": "research-agent", "allowed_actions": ["deploy"]}
        result = authorize(cap, {"agent_id": "research-agent", "action": "deploy"})
        self.assertEqual(result["decision"], "DENY")
        self.assertFalse(result["execution_performed"])

    def test_agent_approval_not_execution(self):
        cap = {"agent_id": "research-agent", "allowed_actions": ["deploy"]}
        result = authorize(cap, {"agent_id": "research-agent", "action": "deploy", "human_approval": True})
        self.assertEqual(result["decision"], "ALLOW_RESEARCH_SIMULATION")
        self.assertFalse(result["execution_performed"])

    def test_model_promotion_fails_closed(self):
        reg = ModelRegistry()
        reg.register("candidate", "0.1", {"accuracy": 0.9}, benchmark_eligible=True)
        self.assertEqual(reg.promotion_decision("candidate", "0.1")["decision"], "DENY")

    def test_registry_rejects_conflicting_versions(self):
        reg = ModelRegistry()
        reg.register("candidate", "0.1", {"accuracy": 0.9})
        with self.assertRaises(ValueError):
            reg.register("candidate", "0.1", {"accuracy": 0.8})

if __name__ == "__main__":
    unittest.main()
