"""Scheduled public GitHub metadata collection. Review-only, append-only first-seen ledger."""
import json, os, tempfile
from datetime import datetime, timezone
from pathlib import Path
from urllib.request import Request, urlopen
from urllib.parse import urlparse

ROOT=Path(__file__).resolve().parent
LEDGER=ROOT/'evidence_ledger.json'
SOURCES=[('uber','ADR'),('waymo-research','waymax'),('BazeletDave','GRI-Institutional-AI-Governance')]
MAX_BYTES=200_000

def collect(fetch=None, now=None):
    now=now or datetime.now(timezone.utc).isoformat()
    if fetch is None:
        def fetch(url):
            req=Request(url,headers={'User-Agent':'GRI-Governance-Research/1.0','Accept':'application/vnd.github+json'})
            with urlopen(req,timeout=15) as res:
                if urlparse(res.url).hostname!='api.github.com':raise ValueError('Untrusted redirect')
                payload=res.read(MAX_BYTES+1)
                if len(payload)>MAX_BYTES:raise ValueError('Oversized metadata')
                return json.loads(payload)
    items=[]
    for owner,repo in SOURCES:
        data=fetch(f'https://api.github.com/repos/{owner}/{repo}')
        expected=f'{owner}/{repo}'
        if data.get('full_name','').lower()!=expected.lower():raise ValueError('Repository identity mismatch')
        items.append({'id':'github:'+expected.lower(),'source_url':'https://github.com/'+expected,
                      'observed_updated_at':data.get('updated_at'),'observed_pushed_at':data.get('pushed_at'),
                      'observed_default_branch':data.get('default_branch'),
                      'last_seen_at':now,'first_seen_at':now,
                      'verification':'PRIMARY_DOCUMENT_METADATA_UNREVIEWED',
                      'review_status':'RESEARCH_LEAD','human_review_required':True,
                      'automated_enforcement':False})
    return items

def merge(existing,incoming):
    prior={x['id']:x for x in existing.get('records',[])}
    for item in incoming:
        old=prior.get(item['id'],{})
        item['first_seen_at']=old.get('first_seen_at',item['first_seen_at'])
        # Do not silently promote review status on repeated polling.
        item['review_status']=old.get('review_status','RESEARCH_LEAD')
        prior[item['id']]=item
    return {'schema_version':'1.0','source':'GitHub public repository metadata',
            'research_only':True,'records':sorted(prior.values(),key=lambda x:x['id'])}

def run(fetch=None):
    existing=json.loads(LEDGER.read_text()) if LEDGER.exists() else {'records':[]}
    result=merge(existing,collect(fetch=fetch))
    with tempfile.NamedTemporaryFile('w',encoding='utf-8',dir=ROOT,delete=False) as tmp:
        json.dump(result,tmp,indent=2);tmp.write('\n');name=tmp.name
    os.replace(name,LEDGER)
    return len(result['records'])

if __name__=='__main__':
    print('Unreviewed public-source records:',run())
