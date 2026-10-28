"""Contract tests for the CISA 2030 research endpoint and dashboard."""
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent

class CisaDashboardContract(unittest.TestCase):
    def test_read_only_route_and_six_domains(self):
        code = (ROOT / "server.py").read_text()
        self.assertIn('if path == "/research/cisa2030/assurance":', code)
        for domain in ("defend", "harden", "prevail", "human_authority", "evidence_integrity", "institutional_legitimacy"):
            self.assertIn('"'+domain+'"', code)
        self.assertIn('"status": "unmeasured"', code)
        self.assertIn('research_only_no_operational_measurements', code)

    def test_dashboard_link_and_safe_rendering(self):
        html = (ROOT / "dashboard.html").read_text()
        module = (ROOT / "cisa2030.html").read_text()
        self.assertIn('href="/research/cisa2030"', html)
        self.assertIn("textContent=x.label", module)
        self.assertIn("textContent=x.status", module)
        self.assertNotIn("innerHTML", module)

if __name__ == "__main__":
    unittest.main()
