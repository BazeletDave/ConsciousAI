"""Independent observation gate and bounded candidate recovery. No actuator access."""
from hashlib import sha256
import json
import math
import statistics

FIELDS={'distance','reported_mu','sensor_valid','model_uncertainty','probe_valid','probe_expected','probe_observed'}

def decide(observation,policy):
    if set(observation)!=FIELDS:raise ValueError('unexpected monitor observation fields')
    for key in FIELDS-{'sensor_valid','probe_valid'}:
        value=observation[key]
        if isinstance(value,bool) or not isinstance(value,(int,float)) or not math.isfinite(value):raise ValueError('nonfinite monitor observation')
    for key in ('sensor_valid','probe_valid'):
        if type(observation[key]) is not bool:raise ValueError('explicit sensor validity required')
    reasons=[]
    if not observation['sensor_valid']:reasons.append('task_sensor_unavailable')
    if not .3<=observation['distance']<=10 or not .08<=observation['reported_mu']<=.18:reasons.append('outside_declared_scope')
    if observation['model_uncertainty']>policy['uncertainty_threshold_m']:reasons.append('model_uncertainty')
    if not observation['probe_valid']:reasons.append('independent_probe_unavailable')
    if observation['probe_expected']<=0:reasons.append('invalid_probe_expectation')
    ratio=None
    if observation['probe_valid'] and observation['probe_expected']>0:
        ratio=abs(observation['probe_observed']-observation['probe_expected'])/max(.1,observation['probe_expected'])
        if ratio>policy['probe_relative_error_threshold']:reasons.append('independent_observation_disagreement')
    return {'hold':bool(reasons),'reasons':reasons,'relative_probe_error':ratio,'human_review_required':bool(reasons),
            'operational_action_authorized':False}

def recovery_candidate(calibration,validation,policy):
    """Use independent displacement measurements; never receive a hidden hazard label."""
    def valid(rows):
        return all(set(r)=={'expected','observed','valid'} and r['valid'] is True and
            all(isinstance(r[k],(int,float)) and not isinstance(r[k],bool) and math.isfinite(r[k]) and r[k]>0 for k in ('expected','observed')) for r in rows)
    if len(calibration)!=policy['calibration_probes'] or len(validation)!=policy['validation_probes'] or not valid(calibration) or not valid(validation):
        return {'state':'HOLD','candidate_scale':None,'validation_passed':False,'human_review_required':True,'operational_action_authorized':False}
    ratios=[r['observed']/r['expected'] for r in calibration]
    scale=1/math.sqrt(statistics.median(ratios))
    errors=[abs(r['observed']-r['expected'])/max(.1,r['expected']) for r in validation]
    passed=policy['minimum_speed_scale']<=scale<=policy['maximum_speed_scale'] and max(errors)<=policy['recovery_validation_threshold']
    payload={'candidate_scale':scale,'validation_errors':errors,'calibration':calibration,'validation':validation}
    return {'state':'REVIEW_REQUIRED' if passed else 'HOLD','candidate_scale':scale,'validation_passed':passed,
            'candidate_digest':sha256(json.dumps(payload,sort_keys=True,separators=(',',':')).encode()).hexdigest(),
            'human_review_required':True,'operational_action_authorized':False}
