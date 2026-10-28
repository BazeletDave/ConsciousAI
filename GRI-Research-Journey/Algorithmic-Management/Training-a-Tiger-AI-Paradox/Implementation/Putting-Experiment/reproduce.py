"""Verify retained artifacts; optionally rerun the frozen experiment in memory."""
from hashlib import sha256
import json
from pathlib import Path
import sys
from experiment import ROOT, digest, run


def verify():
    manifest=json.loads((ROOT/'run_manifest.json').read_text())
    for name,expected in manifest['files'].items():
        if name not in {'protocol.json','experiment.py','test_experiment.py'}:
            raise ValueError('unexpected source path')
        if sha256((ROOT/name).read_bytes()).hexdigest()!=expected:
            raise ValueError('frozen source mismatch: '+name)
    p=json.loads((ROOT/'protocol.json').read_text())
    result=json.loads((ROOT/'results.json').read_text())
    if result['protocol_sha256']!=digest(p) or manifest['protocol_sha256']!=digest(p):
        raise ValueError('protocol mismatch')
    if len(result['runs'])!=len(p['seeds'])*len(p['arms']):
        raise ValueError('run count mismatch')
    expected={(s,a) for s in p['seeds'] for a in p['arms']}
    actual={(r['seed'],r['arm']) for r in result['runs']}
    if expected!=actual:raise ValueError('seed and arm coverage mismatch')
    for record in result['runs']:
        if record['training_trials']!=p['training_trials_per_arm']:
            raise ValueError('unequal training budget')
        if set(record['conditions'])!=set(p['conditions']):raise ValueError('missing condition')
        for metrics in record['conditions'].values():
            if metrics['n']!=p['holdout_cases_per_condition']:
                raise ValueError('holdout budget mismatch')
    if '--rerun' in sys.argv:
        if digest(run(p))!=digest(result):raise ValueError('reproduction mismatch')
    return {'verified':True,'runs':len(result['runs']), 'rerun_matched':'--rerun' in sys.argv,
            'source_hashes_checked':len(manifest['files'])}


if __name__=='__main__':print(json.dumps(verify()))
