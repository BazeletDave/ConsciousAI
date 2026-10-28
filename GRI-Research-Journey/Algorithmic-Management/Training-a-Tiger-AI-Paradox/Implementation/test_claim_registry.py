import unittest
from claim_registry import check,export

def record():
 return {'id':'test','claim':'Synthetic test record','evidence_class':'repository_document','observed_at':'2026-10-28T00:00:00Z','reviewer':'fixture reviewer', 'sources':[{'url':'https://example.org/a','origin_id':'origin-a'}]}
class RegistryTests(unittest.TestCase):
 def test_no_truth_or_action_authority(self):
  r=check(record());self.assertFalse(r['truth_certified']);self.assertFalse(r['autonomous_action_allowed'])
 def test_duplicate_url_is_detected(self):
  r=record();r['sources']*=2;self.assertIn('duplicate_source_url',check(r)['flags'])
 def test_two_publishers_one_origin_not_independent(self):
  r=record();r['sources']+=[{'url':'https://example.net/reprint','origin_id':'origin-a'}];r['asserted_independent_corroboration']=True
  self.assertIn('independence_not_established',check(r)['flags'])
 def test_two_origins_still_need_review(self):
  r=record();r['sources']+=[{'url':'https://example.net/b','origin_id':'origin-b'}];r['asserted_independent_corroboration']=True
  self.assertIn('independence_not_established',check(r)['flags'])
 def test_synthetic_not_empirical(self):
  r=record();r.update(evidence_class='synthetic_fixture',empirical_result=True);self.assertIn('synthetic_not_empirical',check(r)['flags'])
 def test_naive_timestamp_rejected(self):
  r=record();r['observed_at']='2026-10-28T00:00:00'
  with self.assertRaises(ValueError):check(r)
 def test_missing_source(self):
  r=record();r.update(evidence_class='source_observation',sources=[]);self.assertIn('observation_source_missing',check(r)['flags'])
 def test_contradiction_blocks(self):
  r=record();r['contradiction_open']=True;self.assertEqual(check(r)['disposition'],'hold_for_review')
 def test_external_actions_block(self):
  r=record();r['requested_effect']='deployment';self.assertIn('external_action_out_of_scope',check(r)['flags'])
 def test_training_effect_requires_measurement(self):
  r=record();r['claimed_training_effect']=True;self.assertIn('training_effect_not_measured',check(r)['flags'])
 def test_credential_url_rejected(self):
  r=record();r['sources'][0]['url']='https://user:pass@example.org/a'
  with self.assertRaises(ValueError):check(r)
 def test_duplicate_ids_rejected(self):
  with self.assertRaises(ValueError):export([record(),record()])
if __name__=='__main__':unittest.main()
