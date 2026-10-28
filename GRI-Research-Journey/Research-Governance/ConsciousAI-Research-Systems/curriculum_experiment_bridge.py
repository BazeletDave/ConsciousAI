"""Read only connection to the frozen synthetic experiment. Never trains a model."""
from hashlib import sha256
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parent
REPORT='GRI-Research-Journey/Algorithmic-Management/Training-a-Tiger-AI-Paradox/Implementation/Putting-Experiment'
FILES={'protocol.json','experiment.py','test_experiment.py','reproduce.py','run_manifest.json',
       'results.json','reproduction_result.json','README.md','figure.svg'}


def snapshot(root=ROOT,repo=None):
    repo=repo or root.parents[2]
    summary=json.loads((root/'learning_ledger/putting_experiment_summary.json').read_text())
    hashes=summary.get('artifact_hashes',{})
    if set(hashes)!=FILES:raise ValueError('unexpected artifact manifest')
    for name,expected in hashes.items():
        if sha256((repo/REPORT/name).read_bytes()).hexdigest()!=expected:
            raise ValueError('experiment artifact hash mismatch')
    if summary.get('model_promoted') is not False:raise ValueError('invalid promotion flag')
    return dict(summary,integrity_status='artifact_hashes_match_not_independent_validation')


if __name__=='__main__':
    result=snapshot()
    print(json.dumps({'status':result['status'],'models':result['trained_models'],'integrity':result['integrity_status']}))
