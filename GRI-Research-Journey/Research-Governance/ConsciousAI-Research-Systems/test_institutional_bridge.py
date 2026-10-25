"""Read-only dashboard integration smoke tests; run from research service directory."""
import unittest
from institutional_bridge import research_snapshot

class InstitutionalBridgeTests(unittest.TestCase):
    def test_research_modules_load(self):
        data=research_snapshot()
        self.assertEqual(data["status"],"research_modules_loaded")
        self.assertEqual(data["mode"],"read_only_research_integration")
        self.assertEqual(data["graph_nodes"],2)
        self.assertEqual(data["graph_relationships"],1)
    def test_no_autonomous_actions(self):
        data=research_snapshot()
        self.assertFalse(data["agent_executed"])
        self.assertFalse(data["model_promotion_authorized"])
        self.assertFalse(data["deployment_authorized"])
        self.assertFalse(data["release_checklist_complete"])

if __name__=="__main__":
    unittest.main()
