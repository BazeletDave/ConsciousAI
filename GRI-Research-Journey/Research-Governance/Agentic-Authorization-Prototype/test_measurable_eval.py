import unittest
from measurable_eval import evaluate, fixtures, scores, wilson

class MeasurableEvalTests(unittest.TestCase):
    def test_fixture_decisions(self):
        report = evaluate(fixtures())
        self.assertEqual(report['overall']['n'], 9)
        self.assertEqual(report['overall']['fn'], 0)
        self.assertEqual(report['overall']['fp'], 0)
        self.assertIsNone(report['overall']['unauthorized_tool_executions'])
    def test_stable_digest(self):
        self.assertEqual(evaluate(fixtures())['dataset_sha256'],evaluate(fixtures())['dataset_sha256'])
    def test_detects_false_approval(self):
        self.assertEqual(scores([{'actual_allow':True,'expected_allow':False}])['false_approved_rate'],1)
    def test_wilson_small_sample(self):
        lo,hi = wilson(0,9)
        self.assertEqual(lo,0)
        self.assertGreater(hi,0.2)
    def test_rejects_duplicate(self):
        rows = fixtures()
        with self.assertRaises(ValueError):
            evaluate(rows + [rows[0]])
    def test_invalid_action_fails_closed(self):
        row = fixtures()[0]
        row['action']['amount'] = float('nan')
        self.assertFalse(evaluate([row])['decisions'][0]['actual_allow'])
    def test_execution_escape_detected(self):
        row = fixtures()[1]
        row['tool_executed'] = True
        self.assertEqual(evaluate([row])['overall']['unauthorized_tool_executions'],1)

if __name__ == '__main__':
    unittest.main()
