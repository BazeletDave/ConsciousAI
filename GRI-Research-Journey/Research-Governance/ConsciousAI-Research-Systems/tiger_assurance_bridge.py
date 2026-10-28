"""Read only publishing of the retained Tiger assurance experiment; never trains."""
import gzip
from hashlib import sha256
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parent
REPORT='GRI-Research-Journey/Algorithmic-Management/Training-a-Tiger-AI-Paradox/Implementation/Assurance-Experiment'
FILES={'protocol.json','monitor.py','experiment.py','test_assurance.py','freeze_manifest.json','results.json.gz','verify.py','reproduction_result.json','run_record.json','README.md','figure.svg','make_report.py'}

def snapshot(root=ROOT,repo=None):
    repo=repo or root.parents[2]
    summary=json.loads((root/'learning_ledger/tiger_assurance_summary.json').read_text())
    hashes=summary.get('artifact_hashes',{})
    if set(hashes)!=FILES:raise ValueError('unexpected assurance artifact manifest')
    for name,expected in hashes.items():
        if sha256((repo/REPORT/name).read_bytes()).hexdigest()!=expected:raise ValueError('assurance artifact integrity mismatch')
    if summary.get('model_promoted') is not False or summary.get('operational_actions_authorized')!=0:raise ValueError('unexpected operational authorization')
    with gzip.open(repo/REPORT/'results.json.gz','rt',encoding='utf-8') as f:result=json.load(f)
    if any(result[k]!=summary[k] for k in ('trained_models','training_interactions','assigned_holdout_cases')) or result['model_updates_during_evaluation']!=0:raise ValueError('invalid experiment summary')
    if summary['paired_comparisons']!=result['paired_comparisons']:raise ValueError('comparison mismatch')
    reproduction=json.loads((repo/REPORT/'reproduction_result.json').read_text())
    if summary['reproduction']!=reproduction or reproduction.get('rerun_matched') is not True:raise ValueError('reproduction record mismatch')
    record=json.loads((repo/REPORT/'run_record.json').read_text())
    if summary['source_freeze_commit']!=record['source_freeze_commit']:raise ValueError('freeze provenance mismatch')
    if {a['arm'] for a in summary['arms']}!=set(result['aggregates']) or len(summary['arms'])!=len(result['aggregates']):raise ValueError('incomplete curriculum coverage')
    for arm in summary['arms']:
        a=result['aggregates'][arm['arm']]
        expected={'nominal_success':('nominal','raw_success_fraction'),'nominal_unnecessary_hold':('nominal','monitor_unnecessary_hold_fraction'),
          'hidden_baseline_allow':('hidden_friction_shift','baseline_unsafe_action_fraction'),'hidden_monitor_allow':('hidden_friction_shift','monitor_unsafe_action_fraction'),
          'biased_probe_monitor_allow':('hidden_shift_biased_probe','monitor_unsafe_action_fraction'),'probe_dropout_hold':('probe_dropout','monitor_hold_fraction'),
          'recovery_validation':('hidden_friction_shift','recovery_validation_fraction'),'recovery_task_success_per_assigned_case':('hidden_friction_shift','validated_counterfactual_success_per_assigned_case'),
          'moderate_surface_hold':('surface_shift','monitor_hold_fraction'),'mechanical_jitter_hold':('mechanical_jitter','monitor_hold_fraction')}
        for field,(condition,metric) in expected.items():
            if arm[field]!=a[condition][metric]:raise ValueError('summary metric differs from retained result')
    return dict(summary,integrity_status='retained_artifacts_and_summary_match_not_independent_validation')
