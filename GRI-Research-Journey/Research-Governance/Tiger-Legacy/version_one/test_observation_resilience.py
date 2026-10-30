import unittest
from observation_resilience import run

class ObservationResilienceTests(unittest.TestCase):
    def test_deterministic(self):
        self.assertEqual(run(), run())
    def test_counts(self):
        m = run()['metrics']
        self.assertEqual(m['unauthorized'], {'denominator': 4, 'single_allowed': 0, 'dual_allowed': 0})
        self.assertEqual(m['legitimate'], {'denominator': 3, 'single_allowed': 3, 'dual_allowed': 1})
        self.assertEqual(m['hidden_hazard'], {'denominator': 5, 'single_allowed': 2, 'dual_allowed': 1})
    def test_correlated_failure(self):
        rows = {r['case']: r for r in run()['cases']}
        self.assertTrue(rows['hazard_correlated_bias']['dual'])
        self.assertFalse(rows['hazard_primary_biased']['dual'])
        self.assertTrue(rows['normal_disagreement']['simulated_review_referral'])
    def test_no_human_reviewer_claim(self):
        self.assertIn('synthetic', run()['status'])

if __name__ == '__main__':
    unittest.main()
