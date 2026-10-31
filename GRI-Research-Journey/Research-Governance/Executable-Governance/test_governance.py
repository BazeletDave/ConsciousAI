import unittest
from governance import Event, evaluate

class GovernanceTests(unittest.TestCase):
    def event(self, **changes):
        d = dict(event_id="t1", moving=True, handling_detected=True,
                 driver_attribution_verified=True, confidence=0.95)
        d.update(changes)
        return Event(**d)

    def test_warning(self):
        self.assertEqual(evaluate(self.event())["action"],"WARNING_PERMITTED")
    def test_not_moving(self):
        self.assertEqual(evaluate(self.event(moving=False))["action"],"NO_ACTION")
    def test_not_handling(self):
        self.assertEqual(evaluate(self.event(handling_detected=False))["action"],"NO_ACTION")
    def test_no_attribution(self):
        self.assertEqual(evaluate(self.event(driver_attribution_verified=False))["action"],"NO_ACTION")
    def test_uncertain(self):
        self.assertEqual(evaluate(self.event(confidence=0.89))["action"],"REVIEW_EVIDENCE")
    def test_boundary(self):
        self.assertEqual(evaluate(self.event(confidence=0.90))["action"],"WARNING_PERMITTED")
    def test_invalid_confidence(self):
        with self.assertRaises(ValueError): evaluate(self.event(confidence=1.2))
    def test_no_real_world_inputs(self):
        with self.assertRaises(ValueError): evaluate(self.event(source_type="real"))
    def test_reproducible_audit(self):
        self.assertEqual(evaluate(self.event())["decision_hash"],evaluate(self.event())["decision_hash"])


    def test_decision_schema_matches_real_synthetic_policy_records(self):
        """Check policy-generated records against the published contract vocabulary.
        
        This is a standard-library structural smoke test, not full JSON Schema validation.
        """
        import json
        from pathlib import Path
        from datetime import datetime, timezone
        from governance import POLICY_VERSION
        schema=json.loads((Path(__file__).parent/"governance-decision.schema.json").read_text())
        permitted=schema["properties"]["decision"]["properties"]["outcome"]["enum"]
        self.assertEqual(schema["properties"]["source"]["properties"]["source_type"]["const"],"synthetic")
        cases=[
            self.event(),
            self.event(moving=False),
            self.event(handling_detected=False),
            self.event(driver_attribution_verified=False),
            self.event(confidence=0.89),
            self.event(confidence=0.90),
        ]
        for i,event in enumerate(cases):
            with self.subTest(case=i):
                actual=evaluate(event)
                record={
                    "schema_version":"1.0.0",
                    "decision_id":f"synthetic-decision-{i}",
                    "event_id":event.event_id,
                    "recorded_at":datetime.now(timezone.utc).isoformat(),
                    "source":{"source_type":event.source_type,"system_id":"offline-reference"},
                    "provenance":{"generator":"governance.evaluate","artifact_sha256":actual["decision_hash"],
                                  "canonicalization":"none","verification_status":"unverified"},
                    "policy":{"policy_id":"offline-reference","policy_version":actual["policy_version"],
                              "authorization_basis":"synthetic_research_only"},
                    "decision":{"outcome":actual["action"],"reason":actual["reason"],
                                "human_review_required":actual["action"]=="REVIEW_EVIDENCE"},
                    "evidence_classification":"simulation",
                }
                self.assertEqual(set(schema["required"])-set(record),set())
                self.assertEqual(set(record)-set(schema["properties"]),set())
                self.assertIn(record["decision"]["outcome"],permitted)
                self.assertEqual(record["policy"]["policy_version"],POLICY_VERSION)
                self.assertEqual(len(record["provenance"]["artifact_sha256"]),64)
                self.assertEqual(record["source"]["source_type"],"synthetic")
                self.assertEqual(record["policy"]["authorization_basis"],"synthetic_research_only")

if __name__ == "__main__":
    unittest.main()
