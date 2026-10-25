import unittest
from guardrail import Action
from measurable_eval import POLICY, fixtures
from simulated_runtime import Attempt, Simulator, run_experiment, verify_chain

class SimulatorTests(unittest.TestCase):
    def setUp(self):
        self.attempts = [Attempt(r['id'], Action(**r['action']), r['expected_allow'], r['family']) for r in fixtures()]
    def test_enforcement_prevents_unauthorized_side_effects(self):
        report = run_experiment(self.attempts, POLICY, True)
        self.assertEqual(report['unauthorized_executions'], 0)
        self.assertEqual(report['legitimate_block_rate'], 0)
        self.assertTrue(report['audit_chain_valid'])
    def test_monitor_only_exposes_all_unauthorized_actions(self):
        report = run_experiment(self.attempts, POLICY, False)
        self.assertEqual(report['unauthorized_executions'], 8)
        self.assertEqual(report['unauthorized_execution_rate'], 1)
    def test_tampering_detected(self):
        sim = Simulator(POLICY)
        sim.run(self.attempts[0]); sim.run(self.attempts[1])
        self.assertTrue(verify_chain(sim.audit))
        sim.audit[0]['tool_executed'] = False
        self.assertFalse(verify_chain(sim.audit))
    def test_state_changes_only_on_execution(self):
        sim = Simulator(POLICY)
        sim.run(self.attempts[1])
        self.assertEqual(sim.state, {})
        sim.run(self.attempts[0])
        self.assertEqual(len(sim.state['user:123']), 1)
    def test_decision_not_same_as_execution(self):
        sim = Simulator(POLICY, enforce=False)
        result = sim.run(self.attempts[1])
        self.assertFalse(result['decision_allow'])
        self.assertTrue(result['tool_executed'])

if __name__ == '__main__': unittest.main()
