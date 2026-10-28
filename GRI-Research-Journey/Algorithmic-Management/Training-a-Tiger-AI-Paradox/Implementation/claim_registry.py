"""Offline GRI evidence lineage checks. Review support, never truth certification."""
from datetime import datetime
from urllib.parse import urlsplit
import json
from pathlib import Path

CLASSES={'source_observation','repository_document','founder_account','interpretation','synthetic_fixture','proposal','unresolved_lead'}

def check(record):
    if not isinstance(record,dict):raise ValueError('record must be an object')
    for k in ('id','claim','evidence_class','observed_at'):
        if not isinstance(record.get(k),str) or not record[k].strip():raise ValueError('missing '+k)
    if record['evidence_class'] not in CLASSES:raise ValueError('unknown evidence class')
    dt=datetime.fromisoformat(record['observed_at'].replace('Z','+00:00'))
    if dt.tzinfo is None or dt.utcoffset() is None:raise ValueError('timezone required')
    sources=record.get('sources',[])
    if not isinstance(sources,list):raise ValueError('sources must be a list')
    urls=[];lineages=[];flags=[]
    for source in sources:
        if not isinstance(source,dict):raise ValueError('source must be object')
        uri=source.get('url','');u=urlsplit(uri)
        if u.scheme!='https' or not u.hostname or u.username or u.password:raise ValueError('public https source required')
        urls.append(uri.rstrip('/'))
        if not isinstance(source.get('origin_id'),str) or not source['origin_id'].strip():raise ValueError('origin_id required')
        lineages.append(source['origin_id'])
    if len(set(urls))<len(urls):flags.append('duplicate_source_url')
    if len(set(lineages))<len(lineages):flags.append('shared_evidence_origin')
    if record.get('asserted_independent_corroboration') is True:
        if len(set(lineages))<2 or not all(x.get('independence_reviewed') is True for x in sources):flags.append('independence_not_established')
    if record['evidence_class']=='source_observation' and not sources:flags.append('observation_source_missing')
    if record['evidence_class']=='synthetic_fixture' and record.get('empirical_result') is True:flags.append('synthetic_not_empirical')
    if record.get('contradiction_open') is True:flags.append('unresolved_contradiction')
    if record.get('requested_effect') not in (None,'research_record'):flags.append('external_action_out_of_scope')
    if record.get('claimed_training_effect') is True and not record.get('experiment_record'):flags.append('training_effect_not_measured')
    if record.get('reviewer') is None:flags.append('human_review_pending')
    return {'id':record['id'],'evidence_class':record['evidence_class'],'source_count':len(sources),
            'declared_origin_count':len(set(lineages)),'flags':sorted(set(flags)),
            'disposition':'hold_for_review' if flags else 'eligible_for_research_record_review',
            'truth_certified':False,'autonomous_action_allowed':False}

def export(records):
    ids=[r['id'] for r in records]
    if len(ids)!=len(set(ids)):raise ValueError('duplicate claim id')
    return {'schema_version':'1.0','mode':'offline_research_review_only','records':[check(r) for r in records],
            'notice':'Declared origins require source review; passing checks is not verification, ML inference, or deployment authorization.'}

if __name__=='__main__':
    import argparse
    p=argparse.ArgumentParser();p.add_argument('input');p.add_argument('--output');a=p.parse_args()
    result=export(json.loads(Path(a.input).read_text()));text=json.dumps(result,indent=2)+'\n'
    if a.output:Path(a.output).write_text(text)
    else:print(text,end='')
