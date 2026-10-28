import copy
import unittest
from learning_ledger import build, verify
from robotics_snapshot import collect

NOW='2026-10-28T12:00:00Z'


def feed(title='Waymo autonomous vehicle research'):
    return {'generated_at':NOW, 'sources':[{'status':'fetched'}],
            'records':[{'id':'a','source_id':'publisher','title':title,'source_url':'https://example.org/research'}]}


class LearningLedgerTests(unittest.TestCase):
    def test_candidate_results_do_not_promote_active_model(self):
        result=build({}, {}, now=NOW, candidate={'status':'candidate_evaluated_not_promoted'})
        self.assertEqual(result['candidate_evaluation']['status'],'candidate_evaluated_not_promoted')
        self.assertFalse(result['model_updated'])

    def test_http_endpoint_serves_verified_ledger(self):
        import json
        from http.server import ThreadingHTTPServer
        from threading import Thread
        from urllib.request import urlopen
        from unittest.mock import patch
        from server import Handler
        snapshot=build({'test':feed()}, {}, now=NOW)
        server=ThreadingHTTPServer(('127.0.0.1',0),Handler)
        worker=Thread(target=server.serve_forever,daemon=True);worker.start()
        try:
            with patch('learning_ledger.load_snapshot',return_value=snapshot):
                with urlopen(f'http://127.0.0.1:{server.server_port}/institutional/learning-ledger') as r:
                    self.assertEqual(json.load(r)['content_sha256'],snapshot['content_sha256'])
            with patch('learning_ledger.load_snapshot',side_effect=ValueError('corrupt')):
                from urllib.error import HTTPError
                with self.assertRaises(HTTPError) as caught:
                    urlopen(f'http://127.0.0.1:{server.server_port}/institutional/learning-ledger')
                self.assertEqual(caught.exception.code,503)
        finally:
            server.shutdown();server.server_close();worker.join()

    def test_repeat_cycle_does_not_invent_advancement(self):
        first=build({'test':feed()}, {}, now=NOW)
        second=build({'test':feed()}, {}, first, now=NOW)
        self.assertEqual(len(second['events']),1)
        self.assertEqual(second['cycle_count'],2)
        self.assertFalse(second['model_updated'])
        self.assertFalse(second['verification_promoted'])

    def test_revision_preserves_prior_hash(self):
        first=build({'test':feed()}, {}, now=NOW)
        second=build({'test':feed('Zoox updated research')}, {}, first, now=NOW)
        self.assertEqual(second['events'][-1]['kind'],'metadata_revised')
        self.assertEqual(second['events'][-1]['prior_metadata_sha256'], first['events'][0]['metadata_sha256'])
        verify(second)

    def test_outage_keeps_prior_records_without_new_events(self):
        first=build({'test':feed()}, {}, now=NOW)
        second=build({'test':{}}, {}, first, now=NOW)
        self.assertEqual(second['records'],first['records'])
        self.assertEqual(second['records_observed_this_cycle'],0)
        self.assertEqual(second['feed_health'][0]['status'],'invalid_or_missing')

    def test_old_snapshot_is_stale(self):
        self.assertEqual(build({'test':feed()}, {}, now='2026-10-29T12:00:00Z')['feed_health'][0]['status'],'stale')

    def test_malformed_feed_cannot_partly_contribute(self):
        data=feed();data['records'].append({'id':'broken'})
        self.assertEqual(build({'test':data},{},now=NOW)['records'],[])

    def test_corruption_blocks_next_cycle(self):
        first=build({'test':feed()}, {}, now=NOW);first['records'][0]['title']='tampered'
        with self.assertRaises(ValueError):build({}, {}, first, now=NOW)

    def test_capped_chain_remains_verifiable(self):
        from unittest.mock import patch
        with patch('learning_ledger.MAX_EVENTS',2):
            state=None
            for n in range(4):state=build({'test':feed(str(n))},{},state,now=NOW)
            self.assertEqual(state['archived_event_count'],2)
            self.assertEqual(len(state['events']),2)
            verify(state)

    def test_publisher_failure_is_visible(self):
        def fail(source):raise OSError('offline')
        result=collect(fail,now=NOW)
        self.assertFalse(result['records'])
        self.assertTrue(all(s['status']=='failed' for s in result['sources']))

    def test_publisher_bytes_are_observed_not_facts(self):
        result=collect(lambda source:b'<html><title>Publisher safety research</title></html>',now=NOW)
        self.assertEqual(len(result['records']),6)
        self.assertTrue(all(r['human_review_required'] and not r['publication_authorized'] for r in result['records']))

    def test_access_wall_is_not_a_success(self):
        result=collect(lambda source:b'<title>Access denied</title>',now=NOW)
        self.assertEqual(result['records'],[])


if __name__=='__main__':unittest.main()
