"""Bounded official-source discovery and adaptive metadata retrieval.

Collection learns title vocabulary and similarities, never fraud labels or facts.
No article bodies, student records, arbitrary URLs, or executable source content.
"""
from __future__ import annotations
from collections import Counter
import hashlib
import json
import math
import os
import re
import tempfile
from datetime import datetime, timezone, timedelta
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlparse, urljoin
from urllib.request import Request, build_opener, HTTPRedirectHandler
from concurrent.futures import ThreadPoolExecutor
from enrollment_research import DocumentIndex, tokens

ROOT = Path(__file__).resolve().parent
MAX_BYTES = 2_000_000
MAX_RECORDS = 300
STATE = ROOT / 'enrollment_discovery.json'
# This is a fixed institutional allowlist, not user supplied configuration.
HOSTS = {'www.gov.uk', 'home.treasury.gov', 'www.counterfraud.gov.au', 'www.asqa.gov.au', 'oig.ed.gov', 'www.justice.gov'}
EDUCATION = re.compile(r'student|enrol|college|universit|higher education|vocational|skills quality|vet\b|education', re.I)
RISK = re.compile(r'fraud|identity|ghost|integrity|financial aid|student (?:loan|finance)|franchis|qualification', re.I)

def utcnow():
    return datetime.now(timezone.utc).isoformat()

def canonical(url, host):
    u = urlparse(url)
    if u.scheme != 'https' or u.hostname != host or host not in HOSTS or u.username or u.password or u.port not in (None, 443):
        raise ValueError('URL outside source boundary')
    return u._replace(query='', fragment='').geturl().rstrip('/')

class SafeRedirect(HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        if urlparse(newurl).hostname != urlparse(req.full_url).hostname:
            raise ValueError('cross host redirect blocked')
        canonical(newurl, urlparse(req.full_url).hostname)
        return super().redirect_request(req, fp, code, msg, headers, newurl)

def fetch(url):
    canonical(url, urlparse(url).hostname)
    request = Request(url, headers={'User-Agent':'GRI-Institutional-Research/1.0 (metadata discovery)', 'Accept':'application/json,text/html'})
    with build_opener(SafeRedirect()).open(request, timeout=18) as response:
        canonical(response.url, urlparse(url).hostname)
        data = response.read(MAX_BYTES + 1)
        if len(data) > MAX_BYTES:
            raise ValueError('source exceeds byte limit')
        return data

class Links(HTMLParser):
    def __init__(self):
        super().__init__(); self.href = None; self.text = []; self.rows = []
    def handle_starttag(self, tag, attrs):
        if tag == 'a': self.href = dict(attrs).get('href'); self.text = []
    def handle_data(self, data):
        if self.href is not None: self.text.append(data)
    def handle_endtag(self, tag):
        if tag == 'a' and self.href is not None:
            self.rows.append((self.href, ' '.join(' '.join(self.text).split()), None))
            self.href = None; self.text = []

def parse(data, source):
    if source['mode'] == 'govuk_json':
        body = json.loads(data)
        if not isinstance(body.get('results'), list): raise ValueError('unexpected search API schema')
        raw = [(r.get('link',''), r.get('title',''), r.get('public_timestamp')) for r in body['results'] if isinstance(r,dict)]
    else:
        parser = Links(); parser.feed(data.decode('utf-8', 'replace')); raw = parser.rows
    rows = {}
    for href, title, published in raw:
        if not isinstance(href,str) or not isinstance(title,str): continue
        title = ' '.join(title.split())[:350]
        if len(title) < 15 or not EDUCATION.search(title) or not RISK.search(title): continue
        try: url = canonical(urljoin(source['url'], href), source['allowed_host'])
        except ValueError: continue
        if not urlparse(url).path.startswith(source['path_prefix']): continue
        if url == canonical(source['url'], source['allowed_host']): continue
        if any(x in urlparse(url).path for x in ('/search', '/page/', '/tags/', '/topics/', '/organisations/')): continue
        identifier = hashlib.sha256(url.encode()).hexdigest()[:24]
        rows[identifier] = {'id':identifier, 'title':title, 'source_url':url,
            'publisher':source['publisher'], 'country':source['country'], 'source_id':source['id'],
            'source_date':published if isinstance(published,str) else None,
            'verification':'unreviewed_publisher_metadata', 'ai_role':'not_established',
            'human_review_required':True, 'fraud_training_eligible':False}
    return sorted(rows.values(), key=lambda r:r['id'])[:50]

def fit_metadata(rows, previous=None):
    """Fit statistical vocabulary to publisher titles, not participant reports."""
    documents = [{'id':r['id'], 'title':r['title'], 'summary':'', 'retrieval_eligible':True} for r in sorted(rows,key=lambda r:r['id'])]
    index = DocumentIndex(documents)
    old = (previous or {}).get('model', {})
    changed = old.get('corpus_digest') != index.digest
    vectors = {r['id']:v for r,v in zip(index.rows,index.vectors)}
    model = {'id':'enrollment-discovery-tfidf','method':'adaptive_publisher_title_tfidf_cosine','version':old.get('version',0)+int(changed),
        'corpus_digest':index.digest,'documents':len(rows),'vocabulary_size':len(index.idf),
        'idf':index.idf,'vectors':vectors,'predictive_model_trained':False,
        'evaluation_status':'independent_relevance_evaluation_pending', 'precision':None,'recall':None,
        'notice':'Unsupervised metadata adaptation only. Similarity is not evidence verification or fraud probability.'}
    return model

def validate_state(state):
    if not isinstance(state,dict) or state.get('schema_version') != '1.0' or not isinstance(state.get('records'),list):
        raise ValueError('invalid discovery state')
    if len(state['records']) > MAX_RECORDS: raise ValueError('oversized state')
    seen = set()
    for r in state['records']:
        if r['id'] in seen: raise ValueError('duplicate discovery ID')
        seen.add(r['id'])
        if not re.fullmatch('[A-Z]{3}', r['country']): raise ValueError('invalid country')
        canonical(r['source_url'],urlparse(r['source_url']).hostname)
        if r['verification'] != 'unreviewed_publisher_metadata' or r.get('human_review_required') is not True or r.get('fraud_training_eligible') is not False:
            raise ValueError('discovery evidence promotion forbidden')
    expected = fit_metadata(state['records'],state)
    for k in ('corpus_digest','idf','vectors','documents','vocabulary_size'):
        if state['model'].get(k) != expected[k]: raise ValueError('model and corpus do not match')
    return state

def collect(previous=None, fetcher=fetch, sources=None, now=None):
    previous = validate_state(previous) if previous else {}
    now = now or utcnow()
    when = datetime.fromisoformat(now.replace('Z','+00:00'))
    sources = sources if sources is not None else json.loads((ROOT/'enrollment_sources.json').read_text())['sources']
    old_rows = {r['id']:r for r in previous.get('records',[])}
    rows = {k:dict(v) for k,v in old_rows.items() if '/organisations/' not in urlparse(v['source_url']).path and datetime.fromisoformat(v['last_seen_at'].replace('Z','+00:00')) >= when-timedelta(days=365)}
    old_health = {r['source_id']:r for r in previous.get('sources',[])}
    def request(source):
        try:
            canonical(source['url'],source['allowed_host'])
            parsed=parse(fetcher(source['url']),source)
            return source, parsed, None
        except (OSError, ValueError, KeyError, TypeError) as e:
            return source, [], type(e).__name__
    health=[];new_ids=set();changed_ids=set()
    with ThreadPoolExecutor(max_workers=3) as pool:
        fetched = list(pool.map(request,sources))
    for source, incoming, error in fetched:
        prior=old_health.get(source['id'],{})
        health.append({'source_id':source['id'],'publisher':source['publisher'],'country':source['country'],
            'source_url':source['url'],'status':'failed' if error else ('fetched' if incoming else 'fetched_no_relevant_titles'),
            'error_type':error,'items':len(incoming),'attempted_at':now,
            'last_success_at':prior.get('last_success_at') if error else now})
        for row in incoming:
            old=old_rows.get(row['id'])
            row['first_seen_at']=old['first_seen_at'] if old else now
            row['last_seen_at']=now
            if old is None: new_ids.add(row['id'])
            if old is not None and old['title'] != row['title']: changed_ids.add(row['id'])
            rows[row['id']]=row
    retained=sorted(rows.values(),key=lambda r:(r['last_seen_at'],r['id']),reverse=True)[:MAX_RECORDS]
    model=fit_metadata(retained,previous)
    entry={'at':now,'new_records':len(new_ids),'changed_titles':len(changed_ids),'retained_records':len(retained),
        'successful_sources':sum(h['status']!='failed' for h in health),'failed_sources':sum(h['status']=='failed' for h in health),
        'model_version':model['version'],'corpus_digest':model['corpus_digest']}
    state={'schema_version':'1.0','generated_at':now,'sources':health,'records':retained,'model':model,
        'history':(previous.get('history',[])+[entry])[-40:],
        'collection_policy':{'cadence_hours':6,'max_records':MAX_RECORDS,'retention_days':365,'metadata_only':True},
        'last_success_at':now if entry['successful_sources'] else previous.get('last_success_at')}
    return validate_state(state)

def related(state, query, country=None):
    model=state['model']; terms=Counter(tokens(query))
    v={t:(1+math.log(n))*model['idf'][t] for t,n in terms.items() if t in model['idf']}
    norm=math.sqrt(sum(n*n for n in v.values())); v={t:n/norm for t,n in v.items()} if norm else {}
    matches=[]
    for r in state['records']:
        if country and r['country']!=country:continue
        vector=model['vectors'][r['id']]
        relevance=sum(w*vector.get(t,0) for t,w in v.items())
        if relevance>0:matches.append({**r,'similarity':round(relevance,6),'matched_terms':sorted(set(v)&set(vector))})
    return sorted(matches,key=lambda r:(-r['similarity'],r['id']))[:30]

def snapshot(query='',country=None,path=None):
    if not isinstance(query,str) or len(query)>500 or (country and not re.fullmatch('[A-Z]{3}',country)):
        raise ValueError('invalid discovery query')
    p=path or STATE
    if not p.is_file():return {'status':'awaiting_first_collection','records':[],'matches':[],'sources':[],'model':None,'opportunities':[]}
    state=validate_state(json.loads(p.read_text(encoding='utf-8')))
    age=(datetime.now(timezone.utc)-datetime.fromisoformat(state['generated_at'].replace('Z','+00:00'))).total_seconds()/3600
    rows=[r for r in state['records'] if not country or r['country']==country]
    public_model={k:v for k,v in state['model'].items() if k not in ('idf','vectors')}
    successes=sum(s['status']!='failed' for s in state['sources'])
    return {'status':'collection_failed' if not successes else ('stale' if age>18 else ('partial_source_failures' if successes<len(state['sources']) else 'current')),
        'generated_at':state['generated_at'],'last_success_at':state['last_success_at'],'age_hours':round(max(age,0),2),
        'countries':sorted({r['country'] for r in state['records']}),'records':rows,
        'matches':related(state,query,country) if query.strip() else [],'sources':state['sources'],
        'model':public_model,'history':state['history'][-10:],'collection_policy':state['collection_policy'],
        'notice':'Automated publisher title discovery. Records are research leads, not verified cases. Model adaptation is limited to metadata retrieval.'}

def main():
    previous=json.loads(STATE.read_text()) if STATE.exists() else None
    result=collect(previous)
    with tempfile.NamedTemporaryFile('w',dir=ROOT,encoding='utf-8',delete=False) as f:
        json.dump(result,f,indent=2,sort_keys=True);f.write('\n');name=f.name
    os.replace(name,STATE)
    print(json.dumps({'records':len(result['records']),'model_version':result['model']['version'],'sources':result['sources']}))
    if all(s['status']=='failed' for s in result['sources']):raise SystemExit('All source requests failed; last known records retained')
if __name__=='__main__':main()
