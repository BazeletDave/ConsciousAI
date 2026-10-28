import copy
import unittest
from measurement import measure


def episode():
    return dict(id='e1', evidence_status='synthetic', decided_at='2026-10-28T12:00:00Z',
                actor_id='synthetic-agent', accountable_owner='synthetic-owner', policy_version='p1',
                system_version='s1', evidence_refs=['fixture:1'], approved=True, authority_valid=True,
                adjudicated_authorized=True, adjudicator_id='synthetic-reviewer', intervention_required=True,
                triggered_at='2026-10-28T12:00:01Z', intervened_at='2026-10-28T12:00:11Z',
                remediation_verified=True, remediation_review_id='review:1', remediation_evidence_ref='fixture:remedy')


class MeasurementTests(unittest.TestCase):
    def test_known_outcomes(self):
        a=episode(); b=episode(); b.update(id='e2', approved=True, authority_valid=False, adjudicated_authorized=False, intervened_at=None, remediation_verified=False)
        result=measure([a,b]); m=result['metrics']
        self.assertEqual(m['false_approvals_among_reviewed_approvals']['value'], .5)
        self.assertEqual(m['intervention_completion']['value'], .5)
        self.assertEqual(result['intervention_latency']['median_seconds'], 10)

    def test_unreviewed_is_unknown(self):
        a=episode(); a['adjudicated_authorized']=None
        self.assertIsNone(measure([a])['metrics']['adjudicated_approval_accuracy']['value'])

    def test_empty_denominators(self):
        self.assertIsNone(measure([])['metrics']['trace_completeness']['value'])

    def test_incomplete_trace(self):
        a=episode(); a['evidence_refs']=[]
        self.assertEqual(measure([a])['metrics']['trace_completeness']['value'], 0)

    def test_invalid_records(self):
        changes=[{'id':' '}, {'approved':1}, {'authority_valid':'yes'}, {'decided_at':'2026-10-28'},
                 {'adjudicator_id':''}, {'intervened_at':'2026-10-28T11:00:00Z'},
                 {'triggered_at':None}, {'remediation_evidence_ref':''}, {'evidence_status':'verified'}]
        for change in changes:
            with self.subTest(change=change):
                a=episode(); a.update(change)
                with self.assertRaises(ValueError): measure([a])

    def test_duplicate_episode(self):
        with self.assertRaises(ValueError): measure([episode(),episode()])

    def test_evidence_types_cannot_be_pooled(self):
        b=episode(); b.update(id='e2', evidence_status='observational')
        with self.assertRaises(ValueError): measure([episode(),b])

    def test_fingerprint_changes_and_input_is_preserved(self):
        a=episode(); before=copy.deepcopy(a); first=measure([a])
        self.assertEqual(a,before)
        a['system_version']='s2'
        self.assertNotEqual(first['dataset_sha256'],measure([a])['dataset_sha256'])


if __name__=='__main__': unittest.main()
