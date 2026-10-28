"""Repository wide GRI research catalog and extractive question answering.

No external model, network fetch, private material ingestion or factual certification.
"""
from collections import Counter
from datetime import datetime, timezone
from functools import lru_cache
from threading import Lock
from hashlib import sha256
import json
import math
from pathlib import Path
import re
from urllib.parse import quote

ROOT = Path(__file__).resolve().parent
REPO = ROOT.parents[2]
OUTPUT = ROOT / 'unified_research_index.json'
SCOPES = ('GRI-Research-Journey','Research-Journey','research','autonomous-mobility-research')
ROOT_TEXT = {'README.md','DriverREADME.md','AI2025README.md','AIbyGRIREADME.md',
             '2025 Policy Reports','Algorithmic governance reports','Algorithmic labor governance david_grand.md',
             'Grand Research Institute','Invisible Surveillance Hertz AI Policy-by David Grand.md',
             'Meta-Oakley Rayban Analysis.md','Waymo autonomous vehicle research.md'}
DENY = re.compile(r'(^|/)(private|restricted|confidential|coursework|source_snapshots|node_modules|__pycache__)(/|$)|(^|/)(private|restricted|confidential)([./]|$)|syllabus|assignment|answer.?key|(^|/)exam|resume|appendix-a-interview|participant.transcript|raw.interview',re.I)
TOPICS = {
 'uber': ('Uber research', r'\buber\b|\blyft\b|rideshare|ride.hail'),
 'autonomous_vehicles': ('Autonomous vehicles', r'autonomous.{0,20}(vehicle|mobility|driving)|robotaxi|\bwaymo\b|autopilot|self.driving'),
 'mobility': ('Mobility', r'mobility|rideshare|transport|ride.hail|driver|robotaxi'),
 'fourth_industrial_revolution': ('Fourth Industrial Revolution', r'fourth industrial|\b4ir\b|industry 4[.]0|industrial revolution'),
 'artificial_intelligence': ('Artificial intelligence', r'artificial intelligence|\bai\b|machine learning|agentic|algorithm'),
 'ai_paradox': ('AI Paradox', r'ai paradox|ai.paradox|algorithmic.{0,30}paradox|compliance paradox|learning paradox'),
 'institutional_governance': ('Institutional governance', r'governance|institution|accountab|leadership|political economy'),
}
INDEX_LOCK = Lock()
STOP=set('a an the and or of to in for by with as is are from on at not what how why does do can could would should which who when where about explain research gri grand institute'.split())
ALIASES={'vehicles':'vehicle','institutions':'institution','algorithms':'algorithm','drivers':'driver','4ir':'industrial','av':'autonomous','avs':'autonomous','ml':'learning','ai':'artificial','learning':'learning'}

def terms(text):
    return [ALIASES.get(t,t) for t in re.findall(r'[a-z0-9]+',text.lower()) if t not in STOP and len(t)>1]

def digest(value):
    return sha256(json.dumps(value,sort_keys=True,ensure_ascii=False,separators=(',',':')).encode()).hexdigest()

def candidates(repo):
    paths={p for scope in SCOPES for p in (repo/scope).rglob('*') if p.is_file()}
    paths.update(repo/name for name in ROOT_TEXT if (repo/name).is_file())
    # Include future root research Markdown, keeping novel and personal material outside scope.
    paths.update(repo.glob('*.md'))
    return sorted(paths)

def passages(text):
    rows=[];buffer=[];start=1;in_code=False
    def flush():
        nonlocal buffer
        if buffer:
            value=' '.join(buffer).strip()
            if len(value)>=60 and not value.startswith('|'):
                rows.append({'line':start,'text':value[:1300]})
            buffer=[]
    for number,line in enumerate(text.splitlines(),1):
        if line.strip().startswith('```'):
            flush();in_code=not in_code;continue
        if in_code:continue
        if not line.strip() or line.startswith('#'):
            flush();continue
        if not buffer:start=number
        buffer.append(line.strip())
        if sum(map(len,buffer))>=1100:flush()
    flush()
    return rows

def build(repo=REPO):
    repo=repo.resolve();documents=[];excluded=Counter();seen={};linked=[]
    for path in candidates(repo):
        relative=path.relative_to(repo).as_posix()
        if DENY.search(relative):excluded['restricted_or_mirrored_material']+=1;continue
        if path.is_symlink() or not path.resolve().is_relative_to(repo):excluded['unsafe_path']+=1;continue
        ext=path.suffix.lower()
        url='https://github.com/BazeletDave/ConsciousAI/blob/main/'+quote(relative,safe='/')
        if ext in ('.pdf','.docx','.pptx','.xlsx'):
            linked.append({'path':relative,'title':path.stem.replace('_',' '),'url':url,'content_indexed':False});continue
        if ext not in ('.md','.txt') and relative not in ROOT_TEXT:continue
        if path.stat().st_size>2_000_000:excluded['oversized_text']+=1;continue
        text=path.read_text(encoding='utf-8',errors='strict')
        if len(text.strip())<60:excluded['empty_text']+=1;continue
        title=next((l.lstrip('# ').strip() for l in text.splitlines() if l.startswith('# ')),path.stem)[:240]
        content_hash=sha256(text.encode()).hexdigest()
        if content_hash in seen:
            seen[content_hash]['alternate_paths'].append({'path':relative,'url':url});excluded['exact_duplicate_text']+=1;continue
        tags=[key for key,(_,pattern) in TOPICS.items() if re.search(pattern,title+' '+relative+' '+text,re.I)]
        if not tags:tags=['other_gri_research']
        if title.casefold() in ('readme','overview','research overview'): title=path.parent.name.replace('-',' ')+' research overview'
        status='repository_research_not_independently_verified'
        if 'synthetic-student' in relative:status='attributed_classroom_report_not_independently_verified'
        elif re.search(r'(^|/)archive(/|$)',relative,re.I):status='archived_research_reference'
        elif not path.suffix:status='historical_repository_statement_requires_verification'
        row={'id':sha256(relative.encode()).hexdigest()[:20],'path':relative,'title':title,'url':url,
             'content_sha256':content_hash,'topics':tags,'evidence_status':status,
             'alternate_paths':[],'passages':passages(text)}
        seen[content_hash]=row;documents.append(row)
    external_sources=[]
    external_path=repo/'GRI-Research-Journey/Research-Governance/ConsciousAI-Research-Systems/external_research_sources.json'
    if external_path.is_file():
        external=json.loads(external_path.read_text(encoding='utf-8'))
        external_sources=external.get('sources',[])
        allowed={'BazeletDave/ZERO','BazeletDave/from-code-to-consciousness','BazeletDave/GRI-Institutional-AI-Governance','BazeletDave/Treasury-TTB-Label-Verification'}
        for source in external.get('documents',[]):
            repository=source['repository'];path=source['path'];text=source['content']
            if repository not in allowed or DENY.search(path) or len(text.encode())>200_000:continue
            if not source['url'].startswith('https://github.com/'+repository+'/blob/') or '..' in Path(path).parts:continue
            relative='external/'+repository+'/'+path
            title=next((l.lstrip('# ').strip() for l in text.splitlines() if l.startswith('# ')),Path(path).stem)[:240]
            if title.casefold()=='readme':title=repository.split('/')[-1]+' research overview'
            content_hash=sha256(text.encode()).hexdigest()
            if content_hash in seen:
                seen[content_hash]['alternate_paths'].append({'path':relative,'url':source['url']});continue
            tags=[key for key,(_,pattern) in TOPICS.items() if re.search(pattern,title+' '+text,re.I)] or ['other_gri_research']
            row={'id':sha256(relative.encode()).hexdigest()[:20],'path':relative,'title':title,'url':source['url'],
                 'content_sha256':content_hash,'topics':tags,'evidence_status':'public_repository_research_not_independently_verified',
                 'alternate_paths':[],'passages':passages(text),'repository':repository}
            seen[content_hash]=row;documents.append(row)
    return {'external_sources':external_sources,'schema_version':'1.0','generated_at':datetime.now(timezone.utc).isoformat(),
            'documents':documents,'linked_artifacts':linked,'excluded_counts':dict(excluded),
            'corpus_digest':digest(documents),'scope':list(SCOPES),
            'notice':'Public ConsciousAI research and the listed public GRI repository snapshots. Private chats, restricted material and unlisted repositories are not included. Repository claims require source and evidence review.'}

@lru_cache(maxsize=2)
def load_index(signature):
    data=json.loads(OUTPUT.read_text(encoding='utf-8'))
    if data.get('schema_version')!='1.0' or digest(data['documents'])!=data.get('corpus_digest'):
        raise ValueError('research index integrity mismatch')
    return data

def load():
    if not OUTPUT.exists():
        with INDEX_LOCK:
            if not OUTPUT.exists(): main()
    return load_index(OUTPUT.stat().st_mtime_ns)

def catalog(topic=None):
    if topic and topic not in TOPICS and topic!='other_gri_research':raise ValueError('unknown research topic')
    d=load();docs=[r for r in d['documents'] if not topic or topic in r['topics']]
    return {'schema_version':'1.0','generated_at':d['generated_at'],'corpus_digest':d['corpus_digest'],
        'document_count':len(d['documents']),'selected_document_count':len(docs),
        'passage_count':sum(len(r['passages']) for r in d['documents']),
        'topics':[{'id':key,'title':title,'documents':sum(key in r['topics'] for r in d['documents'])} for key,(title,_) in TOPICS.items()],
        'documents':[{k:v for k,v in r.items() if k!='passages'} for r in docs],
        'linked_artifacts':d['linked_artifacts'],'excluded_counts':d['excluded_counts'],
        'external_sources':d.get('external_sources',[]),'answer_method':'extractive_bm25_passage_retrieval','notice':d['notice']}

@lru_cache(maxsize=2)
def fitted(signature):
    d=load();rows=[]
    for document in d['documents']:
        for passage in document['passages']:
            row={**passage,'document_id':document['id'],'title':document['title'],'url':document['url']+'#L'+str(passage['line']),
                 'path':document['path'],'topics':document['topics'],'evidence_status':document['evidence_status']}
            # Title boosts topic relevance without injecting external facts.
            row['counts']=Counter(terms(document['title']+' '+document['title']+' '+passage['text']))
            row['length']=sum(row['counts'].values());rows.append(row)
    frequency=Counter(t for r in rows for t in r['counts'])
    idf={t:math.log(1+(len(rows)-n+.5)/(n+.5)) for t,n in frequency.items()}
    average=math.fsum(r['length'] for r in rows)/max(1,len(rows))
    return rows,idf,average

def ask(question,topic=None):
    if not isinstance(question,str) or not question.strip() or len(question)>800:raise ValueError('question must contain 1 to 800 characters')
    if topic and topic not in TOPICS and topic!='other_gri_research':raise ValueError('unknown research topic')
    load()
    rows,idf,average=fitted(OUTPUT.stat().st_mtime_ns);query=set(terms(question));ranked=[]
    for r in rows:
        if topic and topic not in r['topics']:continue
        overlap=query & r['counts'].keys()
        if not overlap:continue
        score=math.fsum(idf[t]*(r['counts'][t]*2.2)/(r['counts'][t]+1.2*(.25+.75*r['length']/max(average,1))) for t in overlap)
        # Require meaningful support for multi term questions, not one incidental word.
        if len(overlap)<min(2,len(query)):continue
        ranked.append((score,r,overlap))
    ranked.sort(key=lambda x:(-x[0],x[1]['path'],x[1]['line']))
    sources=[];seen=set();seen_titles=set()
    for score,r,overlap in ranked:
        if r['document_id'] in seen or r['title'].casefold() in seen_titles:continue
        seen.add(r['document_id']);seen_titles.add(r['title'].casefold())
        excerpt=r['text'][:900]
        sources.append({'citation':len(sources)+1,'title':r['title'],'path':r['path'],'url':r['url'],
            'excerpt':excerpt,'line':r['line'],'evidence_status':r['evidence_status'],
            'relevance':round(score,4),'matched_terms':sorted(overlap)})
        if len(sources)==5:break
    return {'schema_version':'1.0','question':question,'topic':topic,'mode':'extractive_research_answer',
        'status':'sources_found' if sources else 'insufficient_indexed_support',
        'answer':'The indexed GRI documents contain these relevant passages. Each is a repository statement with its own evidence limits.' if sources else 'The indexed collection does not provide sufficient matching support. Refine the question or add a documented source; no answer has been inferred.',
        'sources':sources,'unmatched_terms':sorted(query-set().union(*(set(s['matched_terms']) for s in sources))) if sources else sorted(query),
        'corpus_digest':load()['corpus_digest'],
        'limitations':['Extractive retrieval, not a generated synthesis or independent fact check.','Similarity does not establish causation, legal compliance, safety or empirical validity.','Linked PDF and Office artifacts are not searched in full text.'],
        'suggested_next_steps':['Compare the cited methods, assumptions and evidence status.','Trace empirical claims to their primary references before scholarly submission.']}

def main():
    data=build();temp=OUTPUT.with_suffix('.tmp');temp.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');temp.replace(OUTPUT)
    print(json.dumps({'documents':len(data['documents']),'passages':sum(len(r['passages']) for r in data['documents']),'linked_artifacts':len(data['linked_artifacts']),'excluded':data['excluded_counts']}))
if __name__=='__main__':main()
