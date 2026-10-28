"""Original GRI toy putting model learning experiment. Standard library only."""
from collections import deque
from datetime import datetime, timezone
from hashlib import sha256
import json
import math
from pathlib import Path
import random
import statistics

ROOT = Path(__file__).resolve().parent


def digest(value):
    return sha256(json.dumps(value,sort_keys=True,separators=(',',':')).encode()).hexdigest()


def case(rng, condition='nominal', bounds=(0.3,10.0)):
    distance=rng.uniform(*bounds)
    mu=rng.uniform(.08,.18)
    result=dict(distance=distance, mu=mu, actual_mu=mu*rng.uniform(.97,1.03),
                grade_x=rng.uniform(-.008,.008), grade_y=rng.uniform(-.012,.012),
                sensor_valid=True, jitter=.008, wind=0.0, unsafe=False, condition=condition)
    if condition=='surface_shift':
        result['actual_mu']*=rng.uniform(.75,.85)
    elif condition=='mechanical_jitter':
        result.update(jitter=.09,wind=rng.uniform(-.2,.2))
    elif condition=='hidden_friction_shift':
        result.update(actual_mu=mu*.45,unsafe=True)
    elif condition=='known_scope_shift':
        result.update(distance=rng.uniform(12,16),mu=.23,actual_mu=.23,unsafe=True)
    elif condition=='missing_sensor':
        result.update(sensor_valid=False,unsafe=True)
    return result


def features(speed, item):
    u=speed*speed/(100*item['mu'])
    return [u,u*speed*speed/10,item['grade_x']*u/item['mu']]


def roll(item,speed,angle,noise,world):
    """Stopping position in a local frame; no cup collision, spin or 3D dynamics."""
    actual_speed=max(0,speed*(1+noise[0]*item['jitter']))
    denominator=2*9.81*max(.015,item['actual_mu']+item['grade_x'])
    travel=max(0,world['gain']*actual_speed**2/denominator*(1-.012*actual_speed**2))
    x=travel*math.cos(angle)
    y=travel*math.sin(angle)+world['drift']*item['grade_y']*travel**2/item['actual_mu']+item['wind']+noise[1]*.015
    return x,y,math.hypot(item['distance']-x,y)


class Learner:
    def __init__(self):
        self.theta=[4.1,0.0,-4.1]
        self.cov=[[20.0 if i==j else 0.0 for j in range(3)] for i in range(3)]
        self.residual_sum=.01
        self.n=0
        self.lateral_sum=0.0
        self.lateral_square=1.0

    def predict(self,speed,item):
        return sum(a*b for a,b in zip(self.theta,features(speed,item)))

    def action(self,item):
        lo,hi=.05,5.5
        for _ in range(18):
            mid=(lo+hi)/2
            if self.predict(mid,item)<item['distance']:lo=mid
            else:hi=mid
        speed=(lo+hi)/2
        drift=self.lateral_sum/self.lateral_square
        angle=math.asin(max(-.45,min(.45,-drift*item['grade_y']*item['distance']/item['mu'])))
        # Compensate longitudinal projection once, within the same action budget.
        speed=min(5.5,speed/math.sqrt(max(.8,math.cos(angle))))
        x=features(speed,item)
        variance=sum(x[i]*self.cov[i][j]*x[j] for i in range(3) for j in range(3))
        uncertainty=math.sqrt(max(0,variance)*self.residual_sum/max(1,self.n))
        return speed,angle,uncertainty

    def update(self,item,speed,angle,x,y):
        f=features(speed,item)
        # Learn travel before its angular projection, using observed displacement.
        travel=x/max(.8,math.cos(angle))
        error=travel-sum(a*b for a,b in zip(self.theta,f))
        pf=[sum(self.cov[i][j]*f[j] for j in range(3)) for i in range(3)]
        denom=1+sum(f[i]*pf[i] for i in range(3))
        self.theta=[self.theta[i]+pf[i]*error/denom for i in range(3)]
        self.cov=[[self.cov[i][j]-pf[i]*pf[j]/denom for j in range(3)] for i in range(3)]
        z=item['grade_y']*travel**2/item['mu']
        self.lateral_sum+=z*(y-travel*math.sin(angle))
        self.lateral_square+=z*z
        self.residual_sum+=error*error
        self.n+=1

    def hold(self,item,uncertainty,protocol):
        return (not item['sensor_valid'] or not .3<=item['distance']<=10 or
                not .08<=item['mu']<=.18 or uncertainty>protocol['uncertainty_threshold_m'])


def noise(rng):
    return rng.gauss(0,1),rng.gauss(0,1)


def train(arm,seed,p):
    rng=random.Random(1000+seed)
    world_rng=random.Random(7000+seed)
    world={'gain':world_rng.uniform(.88,1.12),'drift':world_rng.uniform(.18,.32)}
    model=Learner()
    order=list(p['stages_m'])
    if arm=='forward':order.reverse()
    stage,at_stage=0,0
    recent=deque(maxlen=p['mastery_window'])
    transitions=[]
    curve=[]
    val_rng=random.Random(80000+seed)
    validation=[(case(val_rng),noise(val_rng)) for _ in range(p['checkpoint_cases'])]
    first_threshold=None
    for step in range(1,p['training_trials_per_arm']+1):
        bounds=(.3,10) if arm=='fixed' else order[stage]
        item=case(rng,bounds=bounds)
        speed,angle,_=model.action(item)
        if rng.random()<p['exploration_probability']:
            speed*=rng.uniform(.85,1.15)
            angle+=rng.uniform(-.03,.03)
        x,y,error=roll(item,speed,angle,noise(rng),world)
        model.update(item,speed,angle,x,y)
        recent.append(error<=p['success_radius_m'])
        at_stage+=1
        if (arm!='fixed' and stage<len(order)-1 and at_stage>=p['stage_minimum_trials'] and
            len(recent)==recent.maxlen and sum(recent)/len(recent)>=p['mastery_success_fraction']):
            transitions.append({'trial':step,'completed_bounds':order[stage]})
            stage+=1;at_stage=0;recent.clear()
        if step%p['checkpoint_interval']==0:
            success=sum(roll(v,*model.action(v)[:2],n,world)[2]<=p['success_radius_m'] for v,n in validation)/len(validation)
            curve.append({'training_trials':step,'success':success})
            if first_threshold is None and success>=p['checkpoint_target_success']:first_threshold=step
    return model,world,dict(seed=seed,arm=arm,training_trials=model.n,stage_transitions=transitions,
                            final_stage_bounds=None if arm=='fixed' else order[stage],
                            checkpoint_curve=curve,trials_to_validation_threshold=first_threshold,
                            learned_coefficients=model.theta,lateral_coefficient=model.lateral_sum/model.lateral_square)


def evaluate(model,world,cases,p):
    successes=allowed_success=unsafe_action=unsafe_n=safe_hold=safe_n=holds=misses=recovered=0
    residuals=[]
    failures=[]
    for index,(item,n,retry_noise) in enumerate(cases):
        speed,angle,uncertainty=model.action(item)
        held=model.hold(item,uncertainty,p)
        x,y,error=roll(item,speed,angle,n,world)
        success=error<=p['success_radius_m']
        successes+=success;allowed_success+=success and not held;holds+=held
        unsafe_n+=item['unsafe'];safe_n+=not item['unsafe']
        unsafe_action+=item['unsafe'] and not held
        safe_hold+=not item['unsafe'] and held
        residuals.append(error)
        if not success:
            misses+=1
            retry=dict(item,distance=max(.01,error))
            recovered+=roll(retry,*model.action(retry)[:2],retry_noise,world)[2]<=p['success_radius_m']
            if len(failures)<3:
                failures.append({'case_index':index,'distance':item['distance'],'residual':error,
                                 'uncertainty':uncertainty,'held':held,'simulation_unsafe_label':item['unsafe']})
    n=len(cases)
    return {'n':n,'first_attempt_success':successes/n,'autonomous_success':allowed_success/n,
            'mean_residual_m':statistics.mean(residuals),'escalation_fraction':holds/n,
            'unsafe_action_fraction':unsafe_action/unsafe_n if unsafe_n else None,
            'unnecessary_escalation_fraction':safe_hold/safe_n if safe_n else None,
            'retry_success_after_miss':recovered/misses if misses else None,
            'initial_misses':misses,'recovered_misses':recovered,'failures':failures}


def interval(values,rng,reps):
    mean=statistics.mean(values)
    if len(values)<2:return {'mean':mean,'low':None,'high':None,'seeds':len(values)}
    draws=sorted(statistics.mean(rng.choices(values,k=len(values))) for _ in range(reps))
    return {'mean':mean,'low':draws[int(.025*reps)],'high':draws[min(reps-1,int(.975*reps))],'seeds':len(values)}


def run(p):
    runs=[]
    for seed in p['seeds']:
        rng=random.Random(100000+seed)
        holdout={condition:[(case(rng,condition),noise(rng),noise(rng)) for _ in range(p['holdout_cases_per_condition'])] for condition in p['conditions']}
        for arm in p['arms']:
            model,world,record=train(arm,seed,p)
            before=digest(model.__dict__)
            record['conditions']={condition:evaluate(model,world,items,p) for condition,items in holdout.items()}
            if digest(model.__dict__)!=before:raise RuntimeError('evaluation changed model')
            runs.append(record)
    rng=random.Random(p['bootstrap_seed'])
    metrics=['first_attempt_success','autonomous_success','mean_residual_m','escalation_fraction',
             'unsafe_action_fraction','unnecessary_escalation_fraction','retry_success_after_miss']
    aggregates={}
    for arm in p['arms']:
        selected=[r for r in runs if r['arm']==arm]
        aggregates[arm]={c:{m:interval([r['conditions'][c][m] for r in selected if r['conditions'][c][m] is not None],rng,p['bootstrap_replicates'])
                          for m in metrics if any(r['conditions'][c][m] is not None for r in selected)} for c in p['conditions']}
    lookup={(r['seed'],r['arm']):r for r in runs}
    pairs={}
    for comparator in ['forward','fixed']:
        differences=[lookup[s,'goal_proximal']['conditions']['nominal']['first_attempt_success']-
                     lookup[s,comparator]['conditions']['nominal']['first_attempt_success'] for s in p['seeds']]
        pairs['goal_proximal_minus_'+comparator]=interval(differences,rng,p['bootstrap_replicates'])
    return {'protocol_sha256':digest(p),'runs':runs,'aggregates':aggregates,'nominal_paired_differences':pairs,
            'scope':'synthetic stopping-position experiment, not a golf robot or validated RL transfer benchmark',
            'evaluation_model_updates':0}


def main():
    p=json.loads((ROOT/'protocol.json').read_text())
    source_names=['protocol.json','experiment.py','test_experiment.py']
    manifest={'frozen_at':datetime.now(timezone.utc).isoformat(),
              'files':{n:sha256((ROOT/n).read_bytes()).hexdigest() for n in source_names},
              'protocol_sha256':digest(p),'note':'Written before execution; not external preregistration.'}
    (ROOT/'run_manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
    result=run(p)
    (ROOT/'results.json').write_text(json.dumps(result,indent=2,allow_nan=False)+'\n')
    print(json.dumps({'paired_differences':result['nominal_paired_differences'],'runs':len(result['runs'])}))


if __name__=='__main__':main()
