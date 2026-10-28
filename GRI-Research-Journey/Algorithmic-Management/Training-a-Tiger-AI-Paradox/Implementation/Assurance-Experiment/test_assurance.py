import copy
import json
from pathlib import Path
import unittest
from monitor import decide,recovery_candidate
import experiment as e

P=json.loads((Path(__file__).parent/'protocol.json').read_text())

def nominal():return {'distance':2.,'reported_mu':.12,'sensor_valid':True,'model_uncertainty':.02,'probe_valid':True,'probe_expected':1.,'probe_observed':1.}

class AssuranceTests(unittest.TestCase):
    def test_independent_disagreement_holds_without_hidden_label(self):
        x=nominal();x['probe_observed']=2.2
        d=decide(x,P)
        self.assertTrue(d['hold']);self.assertIn('independent_observation_disagreement',d['reasons'])
        self.assertFalse(d['operational_action_authorized'])

    def test_hidden_ground_truth_is_rejected(self):
        for key in ('actual_mu','unsafe','condition','measurement_bias'):
            x=nominal();x[key]=1
            with self.subTest(key=key),self.assertRaises(ValueError):decide(x,P)

    def test_missing_probe_and_task_sensor_hold(self):
        for key in ('probe_valid','sensor_valid'):
            x=nominal();x[key]=False;self.assertTrue(decide(x,P)['hold'])

    def test_nonfinite_and_invalid_observations_fail_closed(self):
        for key,value in [('probe_observed',float('nan')),('model_uncertainty',float('inf')),('sensor_valid',1)]:
            x=nominal();x[key]=value
            with self.subTest(key=key),self.assertRaises(ValueError):decide(x,P)

    def test_nominal_observation_does_not_hold(self):
        self.assertFalse(decide(nominal(),P)['hold'])

    def test_scope_and_model_uncertainty_remain_enforced(self):
        for key,value in [('distance',15),('reported_mu',.3),('model_uncertainty',.5)]:
            x=nominal();x[key]=value;self.assertTrue(decide(x,P)['hold'])

    def test_recovery_validation_never_authorizes_operation(self):
        cal=[{'expected':1.,'observed':2.,'valid':True}]*3
        val=[{'expected':1.,'observed':1.03,'valid':True}]*2
        r=recovery_candidate(cal,val,P)
        self.assertTrue(r['validation_passed']);self.assertEqual(r['state'],'REVIEW_REQUIRED')
        self.assertTrue(r['human_review_required']);self.assertFalse(r['operational_action_authorized'])

    def test_recovery_holds_on_bad_validation_or_missing_measurements(self):
        cal=[{'expected':1.,'observed':2.,'valid':True}]*3
        val=[{'expected':1.,'observed':2.,'valid':True}]*2
        self.assertFalse(recovery_candidate(cal,val,P)['validation_passed'])
        self.assertEqual(recovery_candidate(cal[:1],val,P)['state'],'HOLD')
        self.assertEqual(recovery_candidate(cal,[{**val[0],'observed':float('nan')}]*2,P)['state'],'HOLD')

    def test_projection_excludes_hazard_and_condition_information(self):
        item=e.base.case(__import__('random').Random(1),'hidden_friction_shift')
        self.assertEqual(set(e.observation_item(item)),{'distance','mu','grade_x','grade_y','sensor_valid'})

    def test_equal_exposure_and_shared_world(self):
        p={**P,'training_trials_per_arm':50}
        original=json.loads((e.BASE/'protocol.json').read_text())
        a,w,ra=e.train('forward_equal_exposure',100,p,original)
        b,v,rb=e.train('goal_equal_exposure',100,p,original)
        self.assertEqual(w,v);self.assertEqual(a.n,50);self.assertEqual(b.n,50)
        self.assertEqual(sorted((tuple(s['bounds']),s['trials']) for s in ra['exposure_by_stage']),sorted((tuple(s['bounds']),s['trials']) for s in rb['exposure_by_stage']))

    def test_evaluation_does_not_update_learner_or_release_model(self):
        original=json.loads((e.BASE/'protocol.json').read_text())
        p={**P,'training_trials_per_arm':50,'holdout_cases_per_condition':4}
        m,w,_=e.train('goal_equal_exposure',100,p,original);before=e.digest(m.__dict__)
        rows=e.holdouts(100,p)['hidden_friction_shift'];r=e.evaluate(m,w,rows,p,original)
        self.assertEqual(before,e.digest(m.__dict__))
        self.assertEqual(r['operational_actions_authorized'],0)
        self.assertEqual(r['n'],4)

    def test_biased_probe_is_a_negative_control_not_privileged_signal(self):
        x=nominal()
        # Different worlds can produce an identical observable input.
        self.assertFalse(decide(x,P)['hold'])
        self.assertEqual(decide(x,P),decide(copy.deepcopy(x),P))

    def test_seed_and_probe_generation_are_reproducible(self):
        p={**P,'holdout_cases_per_condition':2}
        self.assertEqual(e.digest(e.holdouts(100,p)),e.digest(e.holdouts(100,p)))
        self.assertNotEqual(e.digest(e.holdouts(100,p)),e.digest(e.holdouts(101,p)))
