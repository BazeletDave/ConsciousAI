import base64
import unittest
from collect_external_research import collect, REPOSITORIES

class ExternalResearchTests(unittest.TestCase):
    def request(self,path):
        if '/git/trees/' in path:
            return {'sha':'tree','truncated':False,'tree':[{'path':'README.md','type':'blob','sha':'blob','size':100}]}
        if '/git/blobs/' in path:
            return {'encoding':'base64','content':base64.b64encode(b'# GRI research\nPublic institutional governance and artificial intelligence research.').decode()}
        return {'private':False,'default_branch':'main'}

    def test_public_repository_refresh_is_complete_and_auditable(self):
        d=collect(request=self.request)
        self.assertEqual(len(d['documents']),4)
        self.assertTrue(all(s['status']=='fetched' and s['last_success_at'] for s in d['sources']))
        self.assertTrue(all(r['source_blob']=='blob' for r in d['documents']))

    def test_private_repositories_are_not_ingested(self):
        calls=[]
        def private(path):calls.append(path);return {'private':True}
        d=collect(request=private)
        self.assertEqual(d['documents'],[])
        self.assertEqual(len(calls),4)
        self.assertTrue(all(s['status']=='failed_retained_previous' for s in d['sources']))

    def test_network_failure_preserves_prior_snapshot(self):
        first=collect(request=self.request)
        def fail(path):raise OSError('offline')
        second=collect(first,request=fail)
        self.assertEqual(first['documents'],second['documents'])
        self.assertEqual(first['sources'][0]['last_success_at'],second['sources'][0]['last_success_at'])

    def test_deleted_documents_are_removed_on_successful_tree_refresh(self):
        first=collect(request=self.request)
        def empty(path):
            if '/git/trees/' in path:return {'sha':'new','truncated':False,'tree':[]}
            return self.request(path)
        self.assertEqual(collect(first,request=empty)['documents'],[])

    def test_restricted_paths_and_incomplete_trees_are_not_indexed(self):
        def restricted(path):
            if '/git/trees/' in path:return {'sha':'tree','truncated':False,'tree':[{'path':'private/notes.md','type':'blob','sha':'blob'}]}
            return self.request(path)
        self.assertEqual(collect(request=restricted)['documents'],[])
        def truncated(path):
            if '/git/trees/' in path:return {'sha':'tree','truncated':True,'tree':[]}
            return self.request(path)
        d=collect(request=truncated)
        self.assertTrue(all(s['status']=='failed_retained_previous' for s in d['sources']))
