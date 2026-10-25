import unittest
from evaluation_suite import benchmark

class EvaluationSuiteTests(unittest.TestCase):
    def test_expected_decisions(self):
        result = benchmark()
        self.assertEqual(result['n'], 8)
        self.assertTrue(all(c['expected_block']==c['actual_block'] for c in result['cases']))
        self.assertEqual(result['false_approved_rate'], 0)
        self.assertEqual(result['false_blocked_rate'], 0)

if __name__ == '__main__':
    unittest.main()
