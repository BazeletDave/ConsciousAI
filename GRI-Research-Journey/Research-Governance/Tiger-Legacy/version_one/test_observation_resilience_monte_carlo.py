import unittest
from observation_resilience_monte_carlo import simulate

class MonteCarloTests(unittest.TestCase):
    def test_reproducible_seed(self):
        self.assertEqual(simulate(seed=41, n=200), simulate(seed=41, n=200))
    def test_denominators_and_authorization(self):
        r = simulate(n=500)
        self.assertEqual(sum(r['denominators'].values()), 500)
        self.assertEqual(r['counts']['single']['unauthorized_allowed'], 0)
        self.assertEqual(r['counts']['dual']['unauthorized_allowed'], 0)
    def test_dual_never_allows_more_than_single_on_paired_cases(self):
        for shared in (0, 0.5, 1):
            r = simulate(n=1000, shared_error=shared)
            self.assertLessEqual(r['counts']['dual']['hazards_allowed'],
                                 r['counts']['single']['hazards_allowed'])
            self.assertLessEqual(r['counts']['dual']['legitimate_allowed'],
                                 r['counts']['single']['legitimate_allowed'])
    def test_perfectly_shared_error_produces_identical_decisions(self):
        r = simulate(n=1000, shared_error=1)
        self.assertEqual(r['counts']['single'], r['counts']['dual'])
    def test_invalid_parameters(self):
        with self.assertRaises(ValueError):
            simulate(n=0)
        with self.assertRaises(ValueError):
            simulate(shared_error=1.1)

if __name__ == '__main__':
    unittest.main()
