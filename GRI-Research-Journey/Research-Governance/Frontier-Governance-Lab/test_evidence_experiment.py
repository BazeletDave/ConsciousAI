import copy
import unittest
from governance import Metrics, Policy, Request
from evidence import Evidence, EvidenceLedger, digest, verify_chain
from experiment import run_experiment


class EvidenceExperimentTests(unittest.TestCase):
    def setUp(self):
        self.ev = Evidence("synthetic-1", "fixture", "SYNTHETIC", "test-fixture", digest("fixture"))
        self.req = Request("r1", "agent", "simulate", True, Metrics(.1, .01, .04, 2))

    def test_valid_chain_and_external_tip(self):
        ledger = EvidenceLedger()
        ledger.append(self.req, Policy(), self.ev)
        entries = ledger.export()
        self.assertTrue(verify_chain(entries, entries[-1]["entry_digest"]))
        self.assertFalse(verify_chain(entries, "0" * 64))

    def test_mutation_detected(self):
        ledger = EvidenceLedger()
        ledger.append(self.req, Policy(), self.ev)
        entries = ledger.export()
        entries[0]["decision"]["decision"] = "DENY"
        self.assertFalse(verify_chain(entries))

    def test_reordering_detected(self):
        ledger = EvidenceLedger()
        ledger.append(self.req, Policy(), self.ev)
        ledger.append(Request("r2", "agent", "simulate", True, self.req.metrics), Policy(), self.ev)
        entries = ledger.export()
        self.assertFalse(verify_chain(list(reversed(entries))))

    def test_synthetic_only_gate(self):
        with self.assertRaises(ValueError):
            EvidenceLedger().append(self.req, Policy(), Evidence("public", "web", "PUBLIC_SOURCE", "url", digest("source")))

    def test_repeatable_experiment(self):
        self.assertEqual(run_experiment(n=80), run_experiment(n=80))

    def test_experiment_counts(self):
        result = run_experiment(n=80)
        self.assertEqual(sum(result["confusion"].values()), 80)
        self.assertTrue(result["chain_verified"])
        self.assertEqual(result["mode"], "SYNTHETIC_ONLY")

    def test_invalid_experiment_size(self):
        with self.assertRaises(ValueError):
            run_experiment(n=0)


if __name__ == "__main__":
    unittest.main()
