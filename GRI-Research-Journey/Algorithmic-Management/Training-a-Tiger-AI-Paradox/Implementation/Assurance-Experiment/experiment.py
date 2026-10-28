"""Frozen second experiment; original putting files are imported without edits."""
from datetime import datetime,timezone
from hashlib import sha256
import importlib.util
import json
import math
from pathlib import Path
import random
import statistics
from monitor import decide,recovery_candidate

ROOT=Path(__file__).resolve().parent
BASE=ROOT.parent/'Putting-Experiment'
spec=importlib.util.spec_from_file_location('frozen_putting_baseline',BASE/'experiment.py')
base=importlib.util.module_from_spec(spec);spec.loader.exec_module(base)

def digest(value):return sha256(json.dumps(value,sort_keys=True,separators=(',',':')).encode()).hexdigest()

def train(arm,seed,p,original):
    if arm in ('fixed','forward_gated','goal_gated'):
        name={'fixed':'fixed','forward_gated':'forward','goal_gated':'goal_proximal'}[arm]
        model,world,record=base.train(name,seed,{**original,'training_trials_per_arm':p['training_trials_per_arm']})
        record['arm']=arm;record['exposure_by_stage']=None
        return model,world,record
    rng=random.Random(1000+seed);w=random.Random(7000+seed)
    world={'gain':w.uniform(.88,1.12),'drift':w.uniform(.18,.32)};model=base.Learner()
    stages=list(original['stages_m'])
    if arm=='forward_equal_exposure':stages.reverse()
    if p['training_trials_per_arm']%len(stages):raise ValueError('equal exposure requires divisible trial count')
    exposure=p['training_trials_per_arm']//len(stages)
    for step in range(p['training_trials_per_arm']):
        item=base.case(rng,bounds=stages[min(step//exposure,len(stages)-1)])
        speed,angle,_=model.action(item)
        if rng.random()<original['exploration_probability']:
            speed*=rng.uniform(.85,1.15);angle+=rng.uniform(-.03,.03)
        x,y,_=base.roll(item,speed,angle,base.noise(rng),world);model.update(item,speed,angle,x,y)
    return model,world,{'seed':seed,'arm':arm,'training_trials':model.n,'stage_transitions':[],
        'exposure_by_stage':[{'bounds':b,'trials':exposure} for b in stages]}

def observation_item(item):
    # Explicit projection: no actual_mu, unsafe, condition or measurement_bias.
    return {k:item[k] for k in ('distance','mu','grade_x','grade_y','sensor_valid')}

def probe(item,world,speed,angle,p,noise_pair):
    x,_,_=base.roll(item,speed,angle,noise_pair,world)
    return x*item.get('measurement_bias',1.0)+noise_pair[1]*p['probe_measurement_noise_m']

def recovery(model,world,item,p,noises,task_noise):
    reported=observation_item(item)
    calibration=[]
    for speed,n in zip(p['calibration_speeds'],noises[:3]):
        calibration.append({'expected':model.predict(speed,reported),'observed':probe(item,world,speed,0,p,n),'valid':True})
    if any(r['expected']<=0 or r['observed']<=0 for r in calibration):return None
    scale=1/math.sqrt(statistics.median(r['observed']/r['expected'] for r in calibration))
    validation=[]
    for speed,n in zip(p['validation_speeds'],noises[3:]):
        validation.append({'expected':model.predict(speed,reported),'observed':probe(item,world,speed*scale,0,p,n),'valid':True})
    candidate=recovery_candidate(calibration,validation,p)
    speed,angle,_=model.action(reported)
    # Counterfactual diagnostic only, not a released task or physical recovery.
    error=base.roll(item,speed*scale,angle,task_noise,world)[2]
    return {'validation_passed':candidate['validation_passed'],'state':candidate['state'],
        'counterfactual_success':error<=p['success_radius_m'],'residual_m':error,
        'operational_action_authorized':candidate['operational_action_authorized'],'probe_count':5}

def evaluate(model,world,cases,p,original):
    out={k:0 for k in ('n','unsafe_n','safe_n','baseline_unsafe_actions','monitor_unsafe_actions','baseline_holds','monitor_holds','baseline_safe_holds','monitor_safe_holds','baseline_successes','monitor_successes','raw_successes','recovery_attempts','recovery_validation_passes','validated_counterfactual_successes','recovery_probe_count','monitor_valid_preflight_probes')}
    examples=[]
    for i,(item,n,probe_noise,recovery_noises) in enumerate(cases):
        reported=observation_item(item)
        speed,angle,uncertainty=model.action(reported)
        baseline_hold=model.hold(reported,uncertainty,original)
        expected=model.predict(p['probe_speed'],reported)
        valid=item.get('probe_valid',True) and item['sensor_valid']
        measured=probe(item,world,p['probe_speed'],0,p,probe_noise) if valid else 0.0
        decision=decide({'distance':reported['distance'],'reported_mu':reported['mu'],'sensor_valid':reported['sensor_valid'],
            'model_uncertainty':uncertainty,'probe_valid':bool(valid),'probe_expected':expected,'probe_observed':measured},p)
        held=decision['hold'];out['monitor_valid_preflight_probes']+=valid;success=base.roll(item,speed,angle,n,world)[2]<=p['success_radius_m']
        unsafe=item['unsafe'];out['n']+=1;out['unsafe_n']+=unsafe;out['safe_n']+=not unsafe
        out['baseline_unsafe_actions']+=unsafe and not baseline_hold;out['monitor_unsafe_actions']+=unsafe and not held
        out['baseline_holds']+=baseline_hold;out['monitor_holds']+=held
        out['baseline_safe_holds']+=not unsafe and baseline_hold;out['monitor_safe_holds']+=not unsafe and held
        out['baseline_successes']+=success and not baseline_hold;out['monitor_successes']+=success and not held;out['raw_successes']+=success
        if held and valid and .3<=reported['distance']<=10 and .08<=reported['mu']<=.18:
            r=recovery(model,world,item,p,recovery_noises,n)
            if r:
                out['recovery_attempts']+=1;out['recovery_validation_passes']+=r['validation_passed'];out['recovery_probe_count']+=r['probe_count']
                out['validated_counterfactual_successes']+=r['validation_passed'] and r['counterfactual_success']
                if len(examples)<2:examples.append({'case':i,'reasons':decision['reasons'],'candidate':r})
    for prefix in ('baseline','monitor'):
        out[prefix+'_unsafe_action_fraction']=out[prefix+'_unsafe_actions']/out['unsafe_n'] if out['unsafe_n'] else None
        out[prefix+'_unnecessary_hold_fraction']=out[prefix+'_safe_holds']/out['safe_n'] if out['safe_n'] else None
        out[prefix+'_hold_fraction']=out[prefix+'_holds']/out['n']
        out[prefix+'_autonomous_success_fraction']=out[prefix+'_successes']/out['n']
    out['raw_success_fraction']=out['raw_successes']/out['n']
    out['recovery_validation_fraction']=out['recovery_validation_passes']/out['recovery_attempts'] if out['recovery_attempts'] else None
    out['validated_counterfactual_success_per_assigned_case']=out['validated_counterfactual_successes']/out['n']
    out['monitor_preflight_attempts']=out['n'];out['operational_actions_authorized']=0;out['examples']=examples
    return out

def holdouts(seed,p):
    rng=random.Random(910000+seed);result={}
    for condition in p['conditions']:
        rows=[]
        for _ in range(p['holdout_cases_per_condition']):
            underlying='hidden_friction_shift' if condition=='hidden_shift_biased_probe' else ('nominal' if condition=='probe_dropout' else condition)
            item=base.case(rng,underlying)
            if condition=='probe_dropout':item['probe_valid']=False;item['unsafe']=True
            if condition=='hidden_shift_biased_probe':item['measurement_bias']=.45
            rows.append((item,base.noise(rng),base.noise(rng),[base.noise(rng) for _ in range(5)]))
        result[condition]=rows
    return result

def run(p):
    original=json.loads((BASE/'protocol.json').read_text());runs=[]
    for seed in p['seeds']:
        cases=holdouts(seed,p)
        for arm in p['arms']:
            model,world,record=train(arm,seed,p,original);before=digest(model.__dict__)
            record['conditions']={c:evaluate(model,world,rows,p,original) for c,rows in cases.items()}
            if before!=digest(model.__dict__):raise ValueError('evaluation or recovery changed model')
            runs.append(record)
    rng=random.Random(p['bootstrap_seed']);aggregates={}
    metrics=('baseline_unsafe_action_fraction','monitor_unsafe_action_fraction','baseline_unnecessary_hold_fraction','monitor_unnecessary_hold_fraction','baseline_hold_fraction','monitor_hold_fraction','raw_success_fraction','baseline_autonomous_success_fraction','monitor_autonomous_success_fraction','recovery_validation_fraction','validated_counterfactual_success_per_assigned_case')
    for arm in p['arms']:
        selected=[r for r in runs if r['arm']==arm]
        aggregates[arm]={c:{m:base.interval([r['conditions'][c][m] for r in selected if r['conditions'][c][m] is not None],rng,p['bootstrap_replicates']) for m in metrics if any(r['conditions'][c][m] is not None for r in selected)} for c in p['conditions']}
    lookup={(r['seed'],r['arm']):r for r in runs};comparisons={}
    for arm in p['arms']:
        values=[lookup[s,arm]['conditions']['hidden_friction_shift']['baseline_unsafe_action_fraction']-lookup[s,arm]['conditions']['hidden_friction_shift']['monitor_unsafe_action_fraction'] for s in p['seeds']]
        comparisons['hidden_hazard_action_reduction_'+arm]=base.interval(values,rng,p['bootstrap_replicates'])
    for name,a,b in [('equal_exposure_order','goal_equal_exposure','forward_equal_exposure'),('gated_order','goal_gated','forward_gated')]:
        values=[lookup[s,a]['conditions']['nominal']['raw_success_fraction']-lookup[s,b]['conditions']['nominal']['raw_success_fraction'] for s in p['seeds']]
        comparisons[name]=base.interval(values,rng,p['bootstrap_replicates'])
    return {'protocol_sha256':digest(p),'runs':runs,'aggregates':aggregates,'paired_comparisons':comparisons,
        'trained_models':len(runs),'training_interactions':len(runs)*p['training_trials_per_arm'],
        'assigned_holdout_cases':len(runs)*len(p['conditions'])*p['holdout_cases_per_condition'],
        'model_updates_during_evaluation':0,'operational_actions_authorized':0,
        'scope':'offline synthetic assurance study; probe information advantage and counterfactual recovery are explicit; not real world safety validation'}

FROZEN=('protocol.json','monitor.py','experiment.py','test_assurance.py')

def verify_freeze():
    manifest=json.loads((ROOT/'freeze_manifest.json').read_text())
    for name,expected in manifest['files'].items():
        if name not in FROZEN:raise ValueError('unexpected frozen source')
        if sha256((ROOT/name).read_bytes()).hexdigest()!=expected:raise ValueError('frozen source changed: '+name)
    for name,expected in manifest['baseline_files'].items():
        if name not in ('protocol.json','experiment.py','results.json'):raise ValueError('unexpected baseline source')
        if sha256((BASE/name).read_bytes()).hexdigest()!=expected:raise ValueError('original baseline changed')
    return manifest

def main():
    if (ROOT/'results.json').exists():raise SystemExit('Refusing to replace retained experiment results')
    manifest=verify_freeze();p=json.loads((ROOT/'protocol.json').read_text())
    result=run(p);result['freeze_manifest_sha256']=digest(manifest)
    (ROOT/'results.json').write_text(json.dumps(result,indent=2,allow_nan=False)+'\n')
    print(json.dumps({'models':result['trained_models'],'comparisons':result['paired_comparisons']}))
if __name__=='__main__':main()
