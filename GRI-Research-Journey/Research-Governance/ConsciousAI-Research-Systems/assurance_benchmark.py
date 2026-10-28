"""Offline, steward attested evaluation. Attestations are not identity authentication."""
import argparse
from datetime import datetime
import json
import math
import os
from pathlib import Path
from assurance_engine import canonical_hash, classification_metrics, calibration_metrics

METRICS = ('accuracy', 'precision', 'recall', 'false_positive_rate',
           'false_negative_rate', 'brier_score', 'drift', 'bias_evaluation')


def timestamp(value):
    try:
        date = datetime.fromisoformat(value.replace('Z', '+00:00'))
        if date.tzinfo is None:
            raise ValueError('timezone required')
        return date
    except (TypeError, AttributeError, ValueError) as exc:
        raise ValueError('valid timezone aware timestamp required') from exc


def evaluate_dataset(data):
    if not isinstance(data, dict) or data.get('schema_version') != '1.0':
        raise ValueError('unsupported benchmark schema')
    if data.get('task') != 'evidence_publication_gate' or data.get('data_origin') != 'independently_reviewed_real_evidence':
        raise ValueError('real reviewed gate evidence required; synthetic tests are separate')
    if not data.get('model_version') or not data.get('dataset_version'):
        raise ValueError('model and dataset versions required')
    authors = set(data.get('author_ids', []))
    approval = data.get('steward_approval', {})
    if not authors or not approval.get('review_system_reference') or approval.get('rights_cleared') is not True or approval.get('holdout_locked') is not True:
        raise ValueError('authors, steward rights approval and locked holdout required')
    frozen = timestamp(data.get('predictions_frozen_at'))
    if timestamp(approval.get('approved_at')) < frozen:
        raise ValueError('approval must follow freeze')
    rows = data.get('records')
    if not isinstance(rows, list) or not rows:
        raise ValueError('nonempty records required')
    if not isinstance(data.get("training_case_families"), list):
        raise ValueError("explicit training case family manifest required")
    training = set(data["training_case_families"])
    ids, hashes, samples, probabilities = set(), set(), [], []
    excluded = 0
    for row in rows:
        rid, family = row.get('record_id'), row.get('case_family')
        if not isinstance(rid, str) or not rid or rid in ids:
            raise ValueError('unique record IDs required')
        ids.add(rid)
        if not isinstance(family, str) or not family or family in training or row.get('holdout') is not True:
            raise ValueError('missing holdout family or training overlap')
        evidence = row.get('evidence')
        if not isinstance(evidence, dict) or not evidence.get('claim') or not evidence.get('sources'):
            raise ValueError('bounded claim and source evidence required')
        digest = canonical_hash(evidence)
        if row.get('evidence_digest') != digest or digest in hashes:
            raise ValueError('evidence changed or duplicated')
        hashes.add(digest)
        if type(row.get('prediction')) is not bool or timestamp(row.get('predicted_at')) > frozen:
            raise ValueError('boolean prediction must precede freeze')
        reviews = row.get('reviews', [])
        if len(reviews) != 2:
            raise ValueError('two independent reviews required')
        reviewers, labels = set(), []
        for review in reviews:
            reviewer = review.get('reviewer_id')
            if not isinstance(reviewer, str) or not reviewer or reviewer in reviewers or reviewer in authors:
                raise ValueError('distinct nonauthor reviewers required')
            reviewers.add(reviewer)
            if review.get('independence_attested') is not True or not review.get('rationale') or not review.get('audit_reference'):
                raise ValueError('review independence, rationale and audit reference required')
            if review.get('evidence_digest') != digest or timestamp(review.get('reviewed_at')) <= frozen or timestamp(review.get('reviewed_at')) > timestamp(approval['approved_at']):
                raise ValueError('review must bind frozen evidence, follow freeze and precede approval')
            if review.get('label') not in ('supported', 'unsupported', 'indeterminate'):
                raise ValueError('invalid review label')
            labels.append(review['label'])
        probability = row.get('probability')
        if probability is not None and (type(probability) not in (int, float) or not math.isfinite(probability) or not 0 <= probability <= 1):
            raise ValueError('finite probability in [0,1] required')
        if labels[0] != labels[1] or labels[0] == 'indeterminate':
            excluded += 1
            continue
        sample = {'truth': labels[0] == 'supported', 'prediction': row['prediction']}
        samples.append(sample)
        if probability is not None:
            probabilities.append({'truth': sample['truth'], 'probability': probability})
    summary = {'benchmark_status': 'insufficient_reviewed_holdout', 'sample_count': len(samples),
               'minimum_samples': 30, 'case_family_count': len({r['case_family'] for r in rows}),
               'excluded_disputed_or_indeterminate': excluded,
               'dataset_digest': canonical_hash(data), 'dataset_version': data['dataset_version'],
               'model_version': data['model_version'], 'task': data['task'],
               'review_approved_at': approval['approved_at'], 'release_authorized': False,
               'label_authentication': 'steward_attested_not_authenticated_by_software',
               'limitations': ['Sample may not represent deployment conditions',
                              'Reviewer independence and permissions require external audit',
                              'No truth certification or automatic model promotion',
                              'Drift requires separate baseline and current windows',
                              'Bias evaluation requires an approved subgroup study'],
               **{name: None for name in METRICS}}
    if len(samples) < 30 or len({x['truth'] for x in samples}) != 2:
        return summary
    metrics = classification_metrics(samples)
    summary.update({key: metrics[key] for key in METRICS if key in metrics})
    summary['confusion_matrix'] = metrics['confusion_matrix']
    n, p, z = len(samples), metrics['accuracy'], 1.959963984540054
    center = (p + z*z/(2*n))/(1+z*z/n)
    half = z*math.sqrt(p*(1-p)/n+z*z/(4*n*n))/(1+z*z/n)
    summary['accuracy_interval_95'] = [round(center-half,6), round(center+half,6)]
    summary['majority_baseline_accuracy'] = round(max(sum(s['truth'] for s in samples), sum(not s['truth'] for s in samples))/n,6)
    if len(probabilities) == n:
        summary['brier_score'] = calibration_metrics(probabilities)['brier_score']
    summary['benchmark_status'] = 'measured_steward_attested_holdout_not_certified'
    return summary


def public_benchmark():
    path = os.environ.get('ASSURANCE_EVALUATION_DATASET')
    empty = {'sample_count': 0, 'minimum_samples': 30, 'release_authorized': False,
             **{name: None for name in METRICS}}
    if not path:
        return dict(empty, benchmark_status='awaiting_independent_reviews')
    try:
        return evaluate_dataset(json.loads(Path(path).read_text(encoding='utf-8')))
    except (ValueError, OSError, TypeError, KeyError, AttributeError):
        return dict(empty, benchmark_status='blocked_invalid_evaluation_dataset')


def review_queue(watchlist):
    items = []
    for item in watchlist['records']:
        evidence = {'claim': item['summary'], 'sources': item['sources']}
        items.append({'record_id': item['id'], 'title': item['title'],
                      'evidence': evidence, 'evidence_digest': canonical_hash(evidence),
                      'status': 'source_documents_and_human_reviews_required',
                      'required_next_steps': ['Collect claim specific source documents',
                                              'Obtain steward rights approval',
                                              'Freeze predictions and case family holdout',
                                              'Obtain two independent human reviews'],
                      'reviews_completed': 0})
    return {'schema_version': '1.0', 'task': 'evidence_publication_gate', 'records': items,
            'notice': 'Candidate references only. Queue is a seed manifest, not review system state.'}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('dataset', type=Path)
    parser.add_argument('--output', required=True, type=Path)
    args = parser.parse_args()
    report = evaluate_dataset(json.loads(args.dataset.read_text(encoding='utf-8')))
    args.output.write_text(json.dumps(report, indent=2)+'\n', encoding='utf-8')
    print(report['benchmark_status'])
