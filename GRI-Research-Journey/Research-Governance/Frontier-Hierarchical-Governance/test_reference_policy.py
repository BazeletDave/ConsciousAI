"""Regression tests for the isolated frontier research policy."""
import importlib.util
import pathlib
import unittest
path = pathlib.Path(__file__).with_name("reference_policy.py")
spec = importlib.util.spec_from_file_location("frontier_reference", path)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)
def sample(risk="low",instructions=None):
    return {"schema_version":"1.0","request_id":"regression","risk":risk,
            "findings":[{"id":k,"status":"clear"} for k in mod.CONSTRAINTS],
            "instructions":instructions or []}
class GovernanceRegression(unittest.TestCase):
    def test_low_risk_helpful(self):
        self.assertEqual(mod.evaluate(sample())["decision"],"allow")
    def test_root_allow_cannot_override_elevated(self):
        p=sample("elevated",[{"id":"x","authority":"root","effect":"allow"}])
        self.assertEqual(mod.evaluate(p)["decision"],"escalate")
    def test_root_allow_cannot_override_high(self):
        p=sample("high",[{"id":"x","authority":"root","effect":"allow"}])
        self.assertEqual(mod.evaluate(p)["decision"],"escalate")
    def test_hard_constraints_each(self):
        for k in mod.CONSTRAINTS:
            with self.subTest(constraint=k):
                p=sample()
                for f in p["findings"]:
                    if f["id"]==k:f["status"]="violation"
                result=mod.evaluate(p)
                self.assertEqual((result["decision"],result["constraint"]),("deny",k))
    def test_unknown_escalates(self):
        p=sample()
        p["findings"][0]["status"]="unknown"
        self.assertEqual(mod.evaluate(p)["decision"],"escalate")
    def test_invalid_denies(self):
        self.assertEqual(mod.evaluate({})["decision"],"deny")
    def test_system_over_user(self):
        p=sample(instructions=[{"id":"u","authority":"user","effect":"allow"},{"id":"s","authority":"system","effect":"deny"}])
        self.assertEqual(mod.evaluate(p)["decision"],"deny")
    def test_tie_denies(self):
        p=sample(instructions=[{"id":"a","authority":"system","effect":"allow"},{"id":"d","authority":"system","effect":"deny"}])
        self.assertEqual(mod.evaluate(p)["decision"],"deny")
if __name__=="__main__":unittest.main()
