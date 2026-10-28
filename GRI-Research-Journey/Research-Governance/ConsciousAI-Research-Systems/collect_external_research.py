"""Refresh a fixed set of public GRI repositories; retain failures explicitly."""
import base64
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
import json
import os
from pathlib import Path
from urllib.parse import quote, urlparse
from urllib.request import Request, urlopen
from unified_research import DENY
ROOT=Path(__file__).resolve().parent
OUTPUT=ROOT/'external_research_sources.json'
REPOSITORIES=('BazeletDave/ZERO','BazeletDave/from-code-to-consciousness','BazeletDave/GRI-Institutional-AI-Governance','BazeletDave/Treasury-TTB-Label-Verification')

def api(path):
    if not any(path.startswith('/repos/'+repo+'/') or path=='/repos/'+repo for repo in REPOSITORIES):raise ValueError('repository outside allowlist')
    headers={'User-Agent':'GRI-Public-Research-Index/1.0','Accept':'application/vnd.github+json'}
    if os.environ.get('GITHUB_TOKEN'):headers['Authorization']='Bearer '+os.environ['GITHUB_TOKEN']
    with urlopen(Request('https://api.github.com'+path,headers=headers),timeout=20) as r:
        if r.url!='https://api.github.com'+path:raise ValueError('unexpected API redirect')
        data=r.read(2_000_001)
        if len(data)>2_000_000:raise ValueError('oversized API response')
        return json.loads(data)

def collect(previous=None,request=api):
    previous=previous or {};now=datetime.now(timezone.utc).isoformat();documents=[];sources=[]
    old={s['repository']:s for s in previous.get('sources',[])}
    for repo in REPOSITORIES:
        try:
            info=request('/repos/'+repo)
            if info.get('private') is not False:raise ValueError('only public repositories permitted')
            branch=info.get('default_branch','main')
            tree=request('/repos/'+repo+'/git/trees/'+quote(branch,safe='')+'?recursive=1')
            if tree.get('truncated'):raise ValueError('incomplete repository tree')
            eligible=[r for r in tree['tree'] if r.get('type')=='blob' and Path(r['path']).suffix.lower() in ('.md','.txt') and not DENY.search(r['path']) and not r['path'].startswith('.github/') and r['path']!='author.md']
            if len(eligible)>100:raise ValueError('repository exceeds reviewed collection bound')
            def read(row):
                if row.get('size',0)>200_000:raise ValueError('oversized public document')
                blob=request('/repos/'+repo+'/git/blobs/'+row['sha'])
                if blob.get('encoding')!='base64':raise ValueError('unexpected blob encoding')
                content=base64.b64decode(blob['content']).decode('utf-8')
                if len(content.encode())>200_000:raise ValueError('oversized public document')
                return {'repository':repo,'path':row['path'],'content':content,'source_blob':row['sha'],
                    'url':'https://github.com/'+repo+'/blob/'+branch+'/'+quote(row['path'],safe='/')}
            with ThreadPoolExecutor(max_workers=4) as pool:rows=list(pool.map(read,eligible))
            documents.extend(rows);sources.append({'repository':repo,'status':'fetched','documents':len(rows),'failed':0,'source_tree':tree['sha'],'last_attempt_at':now,'last_success_at':now})
        except (OSError,ValueError,KeyError,TypeError) as e:
            retained=[d for d in previous.get('documents',[]) if d['repository']==repo]
            documents.extend(retained);sources.append({'repository':repo,'status':'failed_retained_previous','documents':len(retained),'error_type':type(e).__name__,'last_attempt_at':now,'last_success_at':old.get(repo,{}).get('last_success_at')})
    return {'schema_version':'1.0','generated_at':now,'sources':sources,'documents':documents}

def main():
    previous=json.loads(OUTPUT.read_text()) if OUTPUT.exists() else None
    result=collect(previous);tmp=OUTPUT.with_suffix('.tmp');tmp.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n');tmp.replace(OUTPUT)
    print(json.dumps({'repositories':result['sources'],'documents':len(result['documents'])}))
    if all(s['status']!='fetched' for s in result['sources']):raise SystemExit('No public repository refreshed')
if __name__=='__main__':main()
