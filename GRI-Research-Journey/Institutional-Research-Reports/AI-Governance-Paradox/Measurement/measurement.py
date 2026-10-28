"""GRI offline decision episode measurement. No action authorization is issued."""
import argparse
from datetime import datetime
import hashlib
import json
from statistics import median


def timestamp(value):
    try:
        result = datetime.fromisoformat(value.replace('Z', '+00:00'))
        if result.utcoffset() is None:
            raise ValueError('timezone required')
        return result
    except (TypeError, AttributeError, ValueError) as exc:
        raise ValueError('timezone aware ISO timestamp required') from exc


def text(value):
    return isinstance(value, str) and bool(value.strip())


def measure(episodes):
    if not isinstance(episodes, list):
        raise ValueError('episodes must be a list')
    seen, rows, latencies = set(), [], []
    if len({e.get('evidence_status') for e in episodes if isinstance(e, dict)}) > 1:
        raise ValueError('measure synthetic and observational episodes separately')
    for e in episodes:
        if not isinstance(e, dict) or not text(e.get('id')) or e['id'] in seen:
            raise ValueError('unique nonempty episode ids required')
        seen.add(e['id'])
        if e.get('evidence_status') not in {'synthetic', 'observational'}:
            raise ValueError('explicit evidence status required')
        timestamp(e.get('decided_at'))
        for key in ('approved', 'authority_valid', 'intervention_required'):
            if type(e.get(key)) is not bool:
                raise ValueError(key + ' must be boolean')
        for key in ('adjudicated_authorized', 'remediation_verified'):
            if e.get(key) is not None and type(e[key]) is not bool:
                raise ValueError(key + ' must be boolean or null')
        adjudicated = e.get('adjudicated_authorized')
        if adjudicated is not None and not text(e.get('adjudicator_id')):
            raise ValueError('adjudication requires reviewer identity')
        trace = all(text(e.get(k)) for k in ('actor_id', 'accountable_owner', 'policy_version', 'system_version'))
        refs = e.get('evidence_refs')
        trace = trace and isinstance(refs, list) and bool(refs) and all(text(x) for x in refs)
        triggered = e.get('triggered_at')
        intervened = e.get('intervened_at')
        if e['intervention_required'] and triggered is None:
            raise ValueError('required intervention needs trigger timestamp')
        if triggered is not None:
            trigger = timestamp(triggered)
        if intervened is not None:
            if triggered is None:
                raise ValueError('intervention requires trigger')
            latency = (timestamp(intervened) - trigger).total_seconds()
            if latency < 0:
                raise ValueError('intervention precedes trigger')
        else:
            latency = None
        if e['intervention_required'] and latency is not None:
            latencies.append(latency)
        if e.get('remediation_verified') is True and not (text(e.get('remediation_review_id')) and text(e.get('remediation_evidence_ref'))):
            raise ValueError('verified remediation needs review and evidence')
        rows.append({'id': e['id'], 'evidence_status': e['evidence_status'],
                     'trace_complete': bool(trace), 'intervention_seconds': latency,
                     'approval_without_recorded_authority': e['approved'] and not e['authority_valid'],
                     'false_approval': e['approved'] and adjudicated is False,
                     'adjudicated': adjudicated is not None,
                     'decision_correct': e['approved'] == adjudicated if adjudicated is not None else None,
                     'intervention_required': e['intervention_required'],
                     'remediation_evaluated': e.get('remediation_verified') is not None,
                     'remediation_verified': e.get('remediation_verified') is True})
    def metric(numerator, denominator):
        return {'numerator': numerator, 'denominator': denominator,
                'value': numerator / denominator if denominator else None}
    approvals = sum(e['approved'] for e in episodes)
    reviewed_approvals = sum(e['approved'] and e.get('adjudicated_authorized') is not None for e in episodes)
    return {'schema_version': '1.0',
            'dataset_sha256': hashlib.sha256(json.dumps(episodes, sort_keys=True, separators=(',', ':')).encode()).hexdigest(),
            'evidence_counts': {k: sum(r['evidence_status'] == k for r in rows) for k in ('synthetic', 'observational')},
            'metrics': {
                'trace_completeness': metric(sum(r['trace_complete'] for r in rows), len(rows)),
                'approval_without_recorded_authority': metric(sum(r['approval_without_recorded_authority'] for r in rows), approvals),
                'adjudicated_approval_accuracy': metric(sum(r['decision_correct'] is True for r in rows), sum(r['adjudicated'] for r in rows)),
                'false_approvals_among_reviewed_approvals': metric(sum(r['false_approval'] for r in rows), reviewed_approvals),
                'intervention_completion': metric(sum(r['intervention_required'] and r['intervention_seconds'] is not None for r in rows), sum(r['intervention_required'] for r in rows)),
                'verified_remediation': metric(sum(r['remediation_verified'] for r in rows), sum(r['remediation_evaluated'] for r in rows))},
            'intervention_latency': {'completed_n': len(latencies), 'median_seconds': median(latencies) if latencies else None,
                                     'maximum_seconds': max(latencies) if latencies else None},
            'episodes': rows,
            'limitations': ['Recorded authority and reviewer labels require external verification.',
                            'Missing interventions remain in the completion denominator; latency describes completed interventions only.',
                            'Synthetic and observational episodes must be analyzed separately for substantive conclusions.',
                            'No causal learning effect, regulatory compliance, or production authorization is established.']}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('input')
    parser.add_argument('--output', required=True)
    args = parser.parse_args()
    with open(args.input) as stream:
        result = measure(json.load(stream))
    with open(args.output, 'w') as stream:
        json.dump(result, stream, indent=2, allow_nan=False)
        stream.write('\n')
