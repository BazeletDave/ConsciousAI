import json
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest
from unittest.mock import patch
import test_server
import unified_research as research

class UnifiedResearchTests(unittest.TestCase):
    def test_required_domains_have_documents_and_cited_answers(self):
        d=research.catalog()
        topics={t['id']:t['documents'] for t in d['topics']}
        for topic in ('uber','autonomous_vehicles','mobility','fourth_industrial_revolution','artificial_intelligence','ai_paradox'):
            self.assertGreater(topics[topic],0)
        answer=research.ask('How does Uber use agentic engineering?','uber')
        self.assertEqual(answer['status'],'sources_found')
        self.assertTrue(any('Uber' in s['title'] for s in answer['sources']))
        for source in answer['sources']:
            self.assertTrue(source['url'].startswith('https://github.com/BazeletDave/ConsciousAI/blob/main/'))
            self.assertIn('#L',source['url'])
            self.assertTrue(source['evidence_status'])
            self.assertGreaterEqual(source['line'],1)
        self.assertEqual(len({s['title'] for s in answer['sources']}),len(answer['sources']))

    def test_unknown_question_has_no_invented_answer(self):
        d=research.ask('xyzzzz quantumfrobnitz')
        self.assertEqual(d['status'],'insufficient_indexed_support')
        self.assertEqual(d['sources'],[])
        self.assertIn('no answer has been inferred',d['answer'])

    def test_question_and_topic_validation(self):
        for q,topic in [('',None),('a'*801,None),('Uber','invalid')]:
            with self.subTest(q=q[:10]),self.assertRaises(ValueError):research.ask(q,topic)
        with self.assertRaises(ValueError):research.catalog('../private')

    def test_restricted_duplicate_binary_and_novel_boundaries(self):
        with TemporaryDirectory() as folder:
            repo=Path(folder);scope=repo/'GRI-Research-Journey';scope.mkdir()
            text='# Uber governance research\n\nThis research examines algorithmic management, institutional accountability and driver discretion in mobility systems.\n'
            (scope/'paper.md').write_text(text)
            (scope/'duplicate.md').write_text(text)
            (scope/'private').mkdir();(scope/'private'/'notes.md').write_text(text)
            (scope/'assignment-answers.md').write_text(text)
            (scope/'source_snapshots').mkdir();(scope/'source_snapshots'/'mirror.md').write_text(text)
            (scope/'appendix-a-interview.md').write_text(text)
            (repo/'the-back-door').mkdir();(repo/'the-back-door'/'novel.md').write_text(text)
            (scope/'paper.pdf').write_bytes(b'%PDF-metadata-only')
            (scope/'link.md').symlink_to(scope/'paper.md')
            d=research.build(repo)
            self.assertEqual(len(d['documents']),1)
            self.assertEqual(len(d['documents'][0]['alternate_paths']),1)
            self.assertEqual(len(d['linked_artifacts']),1)
            self.assertFalse(d['linked_artifacts'][0]['content_indexed'])
            self.assertGreater(d['excluded_counts']['restricted_or_mirrored_material'],0)

    def test_line_provenance_and_code_exclusion(self):
        text='# Title\n\nThis passage has sufficient text to establish the first source line and provide a reproducible research excerpt.\n\n```python\nsecret = "not indexed"\n```\n'
        rows=research.passages(text)
        self.assertEqual(rows[0]['line'],3)
        self.assertNotIn('secret',json.dumps(rows))

    def test_integrity_check_rejects_changed_cache(self):
        with TemporaryDirectory() as directory:
            p=Path(directory)/'index.json';p.write_text(json.dumps({'schema_version':'1.0','documents':[],'corpus_digest':'bad'}))
            research.load_index.cache_clear()
            with patch.object(research,'OUTPUT',p),self.assertRaises(ValueError):research.load_index(123456)
            research.load_index.cache_clear()

    def test_title_and_body_are_indexed_without_external_inference(self):
        answer=research.ask('Fourth Industrial Revolution mobility')
        self.assertEqual(answer['mode'],'extractive_research_answer')
        self.assertTrue(answer['sources'])
        self.assertTrue(answer['limitations'])
        for s in answer['sources']:
            lines=(research.REPO/s['path']).read_text().splitlines()
            self.assertIn(lines[s['line']-1].strip(),s['excerpt'] if len(lines[s['line']-1].strip())<800 else lines[s['line']-1])

class UnifiedResearchHTTPTests(unittest.TestCase):
    setUpClass=classmethod(test_server.ResearchServiceTests.setUpClass.__func__)
    tearDownClass=classmethod(test_server.ResearchServiceTests.tearDownClass.__func__)
    fetch=test_server.ResearchServiceTests.fetch

    def test_live_question_catalog_and_assets(self):
        from urllib.request import urlopen
        from urllib.error import HTTPError
        d=self.fetch('/research/catalog')
        self.assertGreater(d['document_count'],100)
        answer=self.fetch('/research/ask?q=Uber%20agentic%20engineering&topic=uber')
        self.assertTrue(answer['sources'])
        for url in ['/research/ask?q=','/research/catalog?topic=invalid']:
            with self.assertRaises(HTTPError) as ctx:self.fetch(url)
            self.assertEqual(ctx.exception.code,400)
        with urlopen(f'http://127.0.0.1:{self.port}/research-library.js') as response:
            self.assertIn(b'textContent',response.read())
        with urlopen(f'http://127.0.0.1:{self.port}/dashboard') as response:
            self.assertIn(b'id="gri-research-library"',response.read())
