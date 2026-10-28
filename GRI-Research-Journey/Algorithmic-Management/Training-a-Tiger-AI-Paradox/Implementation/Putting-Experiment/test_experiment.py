import copy
import json
import random
import unittest
from experiment import ROOT, Learner, case, roll, evaluate, train, run, digest


class ExperimentTests(unittest.TestCase):
    def setUp(self):
        self.p=json.loads((ROOT/'protocol.json').read_text())
        self.world={'gain':1,'drift':.25}
        self.item=dict(distance=2,mu=.12,actual_mu=.12,grade_x=0,grade_y=0,
                       sensor_valid=True,jitter=0,wind=0,unsafe=False)

    def test_zero_speed_and_friction_direction(self):
        self.assertEqual(roll(self.item,0,0,(0,0),self.world),(0,0,2))
        slow=roll(dict(self.item,actual_mu=.18),2,0,(0,0),self.world)[0]
        fast=roll(self.item,2,0,(0,0),self.world)[0]
        self.assertGreater(fast,slow)

    def test_exact_stopping_position_counts_success(self):
        x,_,_=roll(self.item,2,0,(0,0),self.world)
        self.assertAlmostEqual(roll(dict(self.item,distance=x),2,0,(0,0),self.world)[2],0)

    def test_learning_reduces_forward_error(self):
        model=Learner();speed=2
        x,y,_=roll(self.item,speed,0,(0,0),self.world)
        initial=abs(model.predict(speed,self.item)-x)
        for _ in range(50):model.update(self.item,speed,0,x,y)
        self.assertLess(abs(model.predict(speed,self.item)-x),initial/10)

    def test_hold_separates_scope_and_hidden_hazard(self):
        model=Learner()
        self.assertTrue(model.hold(dict(self.item,sensor_valid=False),0,self.p))
        self.assertTrue(model.hold(dict(self.item,distance=12),0,self.p))
        self.assertTrue(model.hold(self.item,.31,self.p))
        self.assertFalse(model.hold(dict(self.item,actual_mu=.03,unsafe=True),0,self.p))

    def test_evaluation_does_not_learn(self):
        model=Learner();before=copy.deepcopy(model.__dict__)
        result=evaluate(model,self.world,[(self.item,(0,0),(0,0))],self.p)
        self.assertEqual(before,model.__dict__)
        self.assertEqual(result['n'],1)

    def test_no_false_safety_label_from_success(self):
        rng=random.Random(4)
        item=case(rng,'hidden_friction_shift')
        self.assertTrue(item['unsafe'])
        self.assertTrue(item['sensor_valid'])
        self.assertNotEqual(item['mu'],item['actual_mu'])

    def test_matched_training_count_and_determinism(self):
        p=dict(self.p,training_trials_per_arm=50,checkpoint_interval=25,checkpoint_cases=5)
        for arm in p['arms']:
            a,_,r=train(arm,2,p);b,_,s=train(arm,2,p)
            self.assertEqual(a.n,50)
            self.assertEqual(digest(r),digest(s))
            self.assertEqual(a.__dict__,b.__dict__)

    def test_small_complete_run_is_paired_and_finite(self):
        p=dict(self.p,seeds=[0,1],training_trials_per_arm=25,checkpoint_interval=25,
               checkpoint_cases=4,holdout_cases_per_condition=4,bootstrap_replicates=40)
        result=run(p)
        self.assertEqual(len(result['runs']),6)
        self.assertEqual(result['evaluation_model_updates'],0)
        json.dumps(result,allow_nan=False)
        for r in result['runs']:
            self.assertEqual(r['training_trials'],25)
            for c in r['conditions'].values():
                self.assertLessEqual(c['autonomous_success'],c['first_attempt_success'])


if __name__=='__main__':unittest.main()
