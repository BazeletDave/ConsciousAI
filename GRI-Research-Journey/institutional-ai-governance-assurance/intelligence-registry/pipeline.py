"""GRI public-source intake: safe offline validation and human review queue."""
import json, hashlib, datetime
from pathlib import Path
from urllib.parse import urlparse
from urllib.request import Request, urlopen

ALLOWED_HOSTS = {'github.com', 'api.github.com', 'www.nist.gov', 'www.federalregister.gov', 'www.gao.gov'}
MAX_BYTES = 300_000

def check_source(url):
    u=urlparse(url)
    if u.scheme != 'https' or u.hostname not in ALLOWED_HOSTS or u.username or u.password or u.port not in (None,443):
        raise ValueError('Source host is not approved')
    return url

def fingerprint(record):
    return hashlib.sha256((record['source_url']+'|'+record['title']).encode()).hexdigest()[:20]

def intake(record):
    for field in ('title','source_url','domain','governance_risk','safeguard','opportunity'):
        if not isinstance(record.get(field),str) or not record[field].strip():
            raise ValueError('Missing '+field)
    check_source(record['source_url'])
    return {'id':fingerprint(record), **{k:record[k] for k in ('title','source_url','domain','governance_risk','safeguard','opportunity')}, 'verification':'UNVERIFIED', 'review_status':'RESEARCH_LEAD', 'ingested_at':datetime.datetime.now(datetime.timezone.utc).isoformat(), 'automated_action':False}

def fetch_github_metadata(owner,repo):
    if not all(s.replace('-','').replace('_','').isalnum() for s in (owner,repo)):
        raise ValueError('Invalid GitHub owner/repo')
    url=f'https://api.github.com/repos/{owner}/{repo}'
    req=Request(url,headers={'User-Agent':'GRI-research-prototype','Accept':'application/vnd.github+json'})
    with urlopen(req,timeout=8) as response:
        if response.url != url or int(response.headers.get('Content-Length','0'))>MAX_BYTES:
            raise ValueError('Redirect or oversized response')
        raw=response.read(MAX_BYTES+1)
        if len(raw)>MAX_BYTES: raise ValueError('Oversized response')
    data=json.loads(raw)
    return {'full_name':data['full_name'],'updated_at':data['updated_at'],'html_url':data['html_url'],'description':data.get('description') or ''}

def export(records, path):
    ids=set(); result=[]
    for rec in records:
        item=intake(rec)
        if item['id'] in ids: continue
        ids.add(item['id']); result.append(item)
    Path(path).write_text(json.dumps({'schema_version':'1.0','production_ready':False,'human_review_required':True,'records':result},indent=2)+'\n',encoding='utf-8')
    return len(result)

if __name__=='__main__':
    import argparse
    p=argparse.ArgumentParser();p.add_argument('--input',required=True);p.add_argument('--output',required=True)
    a=p.parse_args();print('Queued',export(json.loads(Path(a.input).read_text()),a.output),'research leads; no notifications or enforcement performed')
