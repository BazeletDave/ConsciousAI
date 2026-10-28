"""Verify frozen sources and retained results; optionally reproduce in memory."""
import gzip
import json
import math
import sys
from pathlib import Path
import experiment as e

ROOT=Path(__file__).resolve().parent

def load_results():
    path=ROOT/'results.json.gz'
    if path.exists():
        with gzip.open(path,'rt',encoding='utf-8') as f:return json.load(f)
    return json.loads((ROOT/'results.json').read_text())

def verify(rerun=False):
    manifest=e.verify_freeze();result=load_results();p=json.loads((ROOT/'protocol.json').read_text())
    if result['protocol_sha256']!=e.digest(p) or result['freeze_manifest_sha256']!=e.digest(manifest):raise ValueError('protocol lineage mismatch')
    expected={(s,a) for s in p['seeds'] for a in p['arms']}
    if {(r['seed'],r['arm']) for r in result['runs']}!=expected or len(result['runs'])!=len(expected):raise ValueError('seed arm mismatch')
    for r in result['runs']:
        if r['training_trials']!=p['training_trials_per_arm']:raise ValueError('training budget mismatch')
        if set(r['conditions'])!=set(p['conditions']):raise ValueError('condition mismatch')
        if r['exposure_by_stage'] is not None and {x['trials'] for x in r['exposure_by_stage']}!={p['training_trials_per_arm']//5}:raise ValueError('unmatched stage exposure')
        for c in r['conditions'].values():
            if c['n']!=p['holdout_cases_per_condition'] or c['operational_actions_authorized']!=0:raise ValueError('invalid evaluation or release')
            for prefix in ('baseline','monitor'):
                fraction=c[prefix+'_unsafe_action_fraction']
                if c['unsafe_n'] and not math.isclose(fraction,c[prefix+'_unsafe_actions']/c['unsafe_n'],abs_tol=1e-12):raise ValueError('inconsistent hazard metric')
    if result['model_updates_during_evaluation']!=0 or result['operational_actions_authorized']!=0:raise ValueError('unexpected model change or release')
    if rerun:
        expected_result={k:v for k,v in result.items() if k!='freeze_manifest_sha256'}
        if e.digest(e.run(p))!=e.digest(expected_result):raise ValueError('exact reproduction mismatch')
    return {'verified':True,'models':len(expected),'original_baseline_hashes_match':True,'rerun_performed':rerun,'rerun_matched':True if rerun else None,
            'notice':'Engineering reproducibility check; not independent scientific or physical safety validation'}
if __name__=='__main__':print(json.dumps(verify('--rerun' in sys.argv)))
