import json
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest
from country_topics import EXAMPLES, TopicModel
from research_evolution import build, learning_candidate


class ResearchEvolutionTests(unittest.TestCase):
    def test_added_revised_removed_documents_and_proposed_connections(self):
        with TemporaryDirectory() as folder:
            repo = Path(folder)
            path = repo / 'GRI-Research-Journey/Integrated-Research-Journey/case.md'
            path.parent.mkdir(parents=True)
            path.write_text('# Brazil AI governance\nA working hypothesis.', encoding='utf-8')
            feed = {'records': [{'id': 'r1', 'title': 'Brazil AI governance institutions', 'country_codes': ['BRA'], 'content_sha256': 'record-digest'}]}
            first = build(repo, feed=feed)
            self.assertEqual(first['document_count'], 1)
            self.assertEqual(first['connected_records'], 1)
            self.assertEqual(first['evidence_connections'][0]['research'][0]['relation'], 'suggested_research_connection_not_causation')
            self.assertEqual(build(repo, feed=feed, previous=first)['changes']['added'], [])
            path.write_text('# Brazil AI governance\nRevised hypothesis.', encoding='utf-8')
            second = build(repo, feed=feed, previous=first)
            self.assertEqual(len(second['changes']['revised']), 1)
            self.assertNotEqual(first['catalog_sha256'], second['catalog_sha256'])
            path.unlink()
            self.assertEqual(len(build(repo, previous=second)['changes']['removed']), 1)

    def test_restricted_course_names_and_symlinks_excluded(self):
        with TemporaryDirectory() as folder:
            repo = Path(folder)
            scope = repo / 'GRI-Research-Journey/Integrated-Research-Journey'
            scope.mkdir(parents=True)
            (scope / 'assignment-answers.md').write_text('# Restricted assignment')
            (scope / 'syllabus.md').write_text('# Syllabus')
            (repo / 'private.md').write_text('# Outside configured scope')
            (scope / 'linked.md').symlink_to(repo / 'private.md')
            self.assertEqual(build(repo)['document_count'], 0)

    def test_unreviewed_or_stale_feedback_never_updates_active_model(self):
        records = [{'id': 'r', 'title': 'AI governance', 'source_id': 's', 'content_sha256': 'current'}]
        rows = [{'record_id': 'r', 'content_sha256': 'old', 'label': 'artificial_intelligence', 'split': 'train', 'review_status': 'approved', 'training_rights': 'cleared', 'reviewed_by': 'reviewer'}]
        report = learning_candidate(rows, records)
        self.assertEqual(report['accepted_records'], 0)
        self.assertEqual(report['rejected_records'], 1)
        self.assertEqual(report['status'], 'blocked')
        self.assertFalse(report['active_model_updated'])
        self.assertIsNone(report['candidate_accuracy'])

    def test_candidate_fit_is_isolated_and_source_leakage_blocks(self):
        records, feedback = [], []
        for label in EXAMPLES:
            for split, n in [('train', 10), ('holdout', 5)]:
                for i in range(n):
                    identity = f'{label}-{split}-{i}'
                    records.append({'id': identity, 'title': EXAMPLES[label][0] + ' ' + ('training' if split == 'train' else 'evaluation'), 'source_id': split, 'content_sha256': identity, 'first_seen_at': '2026-01-01T00:00:00Z' if split == 'train' else '2026-02-01T00:00:00Z'})
                    feedback.append({'record_id': identity, 'content_sha256': identity, 'label': label, 'split': split, 'review_status': 'approved', 'training_rights': 'cleared', 'reviewed_by': split + '-reviewer'})
        original = TopicModel().training_sha256
        report = learning_candidate(feedback, records)
        self.assertEqual(report['status'], 'candidate_evaluated_not_promoted')
        self.assertFalse(report['active_model_updated'])
        self.assertEqual(TopicModel().training_sha256, original)
        records[-1]['source_id'] = 'train'
        self.assertIn('train_holdout_source_overlap', learning_candidate(feedback, records)['blocking_reasons'])
