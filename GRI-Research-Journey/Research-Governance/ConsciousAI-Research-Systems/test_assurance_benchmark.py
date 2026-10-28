"""Synthetic fixtures test software only; never published as real performance."""
import copy
import json
import os
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
from assurance_engine import canonical_hash
from assurance_benchmark import evaluate_dataset, public_benchmark, review_queue


def fixture():
    data = {'schema_version': '1.0', 'task': 'evidence_publication_gate',
            'data_origin': 'independently_reviewed_real_evidence',
            'model_version': 'synthetic-fixture-only', 'dataset_version': 'test-only',
            'author_ids': ['author'], 'training_case_families': ['training'],
            'predictions_frozen_at': '2026-10-20T00:00:00Z',
            'steward_approval': {'rights_cleared': True, 'holdout_locked': True,
                                'review_system_reference': 'test-only',
                                'approved_at': '2026-10-23T00:00:00Z'}, 'records': []}
    for i in range(40):
        evidence = {'claim': 'Synthetic claim '+str(i), 'sources': ['synthetic:'+str(i)]}
        digest = canonical_hash(evidence)
        truth = i % 2 == 0
        prediction = truth if i % 5 else not truth
        reviews = [{'reviewer_id': reviewer, 'independence_attested': True,
                    'label': 'supported' if truth else 'unsupported', 'rationale': 'Synthetic test',
                    'audit_reference': 'test-only', 'reviewed_at': '2026-10-21T00:00:00Z',
                    'evidence_digest': digest} for reviewer in ('a', 'b')]
        data['records'].append({'record_id': str(i), 'case_family': 'family'+str(i//4),
                                'holdout': True, 'evidence': evidence, 'evidence_digest': digest,
                                'prediction': prediction, 'probability': .8 if prediction else .2,
                                'predicted_at': '2026-10-19T00:00:00Z', 'reviews': reviews})
    return data


class BenchmarkTests(unittest.TestCase):
    def test_known_confusion_and_calibration(self):
        result = evaluate_dataset(fixture())
        self.assertEqual(result['confusion_matrix'], dict(tp=16, tn=16, fp=4, fn=4))
        self.assertEqual(result['accuracy'], .8)
        self.assertEqual(result['false_negative_rate'], .2)
        self.assertEqual(result['brier_score'], .16)
        self.assertFalse(result['release_authorized'])
        self.assertIsNone(result['drift'])
        self.assertIsNone(result['bias_evaluation'])
        self.assertNotIn('records', result)
        self.assertLess(result['accuracy_interval_95'][0], .8)
    def test_block_tampering_and_invalid_provenance(self):
        mutations = [lambda d: d['records'][0]['evidence'].update(claim='tampered'),
                     lambda d: d['records'][0]['reviews'][0].update(reviewer_id='author'),
                     lambda d: d['records'][0]['reviews'][0].update(reviewer_id='b'),
                     lambda d: d['records'][0].update(case_family='training'),
                     lambda d: d['records'][0].update(predicted_at='2026-10-22T00:00:00Z'),
                     lambda d: d['records'][0]['reviews'][0].update(reviewed_at='2026-10-19T00:00:00Z'),
                     lambda d: d['records'][0]['reviews'][0].update(evidence_digest='bad'),
                     lambda d: d['records'][0].update(probability=float('nan')),
                     lambda d: d['steward_approval'].update(rights_cleared=False),
                     lambda d: d.update(data_origin='synthetic')]
        for change in mutations:
            with self.subTest(change=change):
                data = fixture(); change(data)
                with self.assertRaises(ValueError): evaluate_dataset(data)
    def test_indeterminate_and_disagreement_excluded(self):
        data = fixture()
        for row in data['records'][:12]: row['reviews'][0]['label'] = 'indeterminate'
        result = evaluate_dataset(data)
        self.assertEqual(result['sample_count'], 28)
        self.assertEqual(result['excluded_disputed_or_indeterminate'], 12)
        self.assertIsNone(result['accuracy'])
    def test_no_probability_no_brier(self):
        data = fixture(); data['records'][0].pop('probability')
        self.assertIsNone(evaluate_dataset(data)['brier_score'])
    def test_single_class_not_benchmark(self):
        data = fixture()
        for row in data['records']:
            for review in row['reviews']: review['label'] = 'supported'
        self.assertIsNone(evaluate_dataset(data)['accuracy'])
    def test_public_missing_and_invalid_fail_closed(self):
        with patch.dict(os.environ, {}, clear=True):
            self.assertEqual(public_benchmark()['benchmark_status'], 'awaiting_independent_reviews')
        with patch.dict(os.environ, {'ASSURANCE_EVALUATION_DATASET': '/nonexistent'}):
            self.assertEqual(public_benchmark()['benchmark_status'], 'blocked_invalid_evaluation_dataset')
    def test_queue_is_explicit_seed_not_review_state(self):
        queue = review_queue({'records': [{'id':'x','title':'X','summary':'Claim','sources':[]} ]})
        self.assertEqual(queue['records'][0]['reviews_completed'], 0)
    def test_server_wiring(self):
        import server
        result = server.assurance_dashboard()
        self.assertIn('evaluation', result)
        self.assertEqual(result['review_queue_url'], '/assurance/review-queue')

if __name__ == '__main__': unittest.main()
