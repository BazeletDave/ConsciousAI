import unittest
from experiment import run

class ExperimentTests(unittest.TestCase):
    def test_reproducible(self):
        self.assertEqual(run(n=200,seed=4),run(n=200,seed=4))
    def test_accounting(self):
        x=run(n=200)
        self.assertEqual(sum(x[k] for k in ("true_positive","false_positive","false_negative","true_negative")),200)
    def test_synthetic_label(self):
        self.assertEqual(run(n=10)["dataset"],"synthetic")

if __name__=="__main__": unittest.main()
