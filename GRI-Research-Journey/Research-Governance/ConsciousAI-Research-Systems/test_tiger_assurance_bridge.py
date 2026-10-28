import json
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest
from unittest.mock import patch
import test_server
from tiger_assurance_bridge import snapshot,ROOT

class TigerBridgeTests(unittest.TestCase):
    def test_summary_matches_retained_results_without_model_release(self):
        d=snapshot()
        self.assertEqual(d['trained_models'],100)
        self.assertEqual(d['training_interactions'],600000)
        self.assertEqual(d['assigned_holdout_cases'],120000)
        self.assertFalse(d['model_promoted'])
        self.assertTrue(d['reproduction']['rerun_matched'])
        self.assertEqual(len(d['arms']),5)
        self.assertTrue(all(a['biased_probe_monitor_allow']['mean']==1 for a in d['arms']))

    def test_changed_dashboard_metric_is_rejected(self):
        with TemporaryDirectory() as directory:
            root=Path(directory)/'service';(root/'learning_ledger').mkdir(parents=True)
            d=json.loads((ROOT/'learning_ledger/tiger_assurance_summary.json').read_text())
            d['arms'][0]['hidden_monitor_allow']['mean']=.99
            (root/'learning_ledger/tiger_assurance_summary.json').write_text(json.dumps(d))
            with self.assertRaises(ValueError):snapshot(root,ROOT.parents[2])

    def test_manifest_tamper_is_rejected(self):
        with TemporaryDirectory() as directory:
            root=Path(directory)/'service';(root/'learning_ledger').mkdir(parents=True)
            d=json.loads((ROOT/'learning_ledger/tiger_assurance_summary.json').read_text());d['artifact_hashes']['../escape']='bad'
            (root/'learning_ledger/tiger_assurance_summary.json').write_text(json.dumps(d))
            with self.assertRaises(ValueError):snapshot(root,ROOT.parents[2])

class TigerHTTPTests(unittest.TestCase):
    setUpClass=classmethod(test_server.ResearchServiceTests.setUpClass.__func__)
    tearDownClass=classmethod(test_server.ResearchServiceTests.tearDownClass.__func__)
    fetch=test_server.ResearchServiceTests.fetch
    def test_endpoint_is_read_only_and_preserves_baseline(self):
        d=self.fetch('/institutional/tiger-assurance');self.assertFalse(d['model_promoted'])
        self.assertEqual(self.fetch('/institutional/curriculum-experiment')['trained_models'],60)
