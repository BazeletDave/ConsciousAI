"""GRI external-label multi-turn evaluation. Stdlib-only. No live agent."""
import argparse,hashlib,json,math,random
from collections import defaultdict
from guardrail import Policy,Action,authorize
POLICY=Policy('travel',('book ride',),('reserve',),('user:123',),100,True)
FIELDS={'agent_id','intent','tool','resource','amount','approved'}
def load(path):
 with open(path,encoding='utf8') as f:return [json.loads(x) for x in f if x.strip()]
def validate(rows):
 if not rows:raise ValueError('empty')
 groups=defaultdict(list);seen=set()
 for r in rows:
  for k in ('conversation_id','family','split','label_source','adjudicator_id'):
   if not isinstance(r.get(k),str) or not r[k]:raise ValueError('missing '+k)
  if r['label_source'] not in ('independent_human','external_dataset'):raise ValueError('unverified label provenance')
  if type(r.get('turn_index')) is not int or r['turn_index']<0 or type(r.get('expected_allow')) is not bool:raise ValueError('invalid turn or label')
  key=(r['conversation_id'],r['turn_index'])
  if key in seen:raise ValueError('duplicate turn')
  seen.add(key);a=r.get('action')
  if not isinstance(a,dict) or set(a)!=FIELDS:raise ValueError('invalid action schema')
  if any(type(a[k]) is not str for k in ('agent_id','intent','tool','resource')) or type(a['approved']) is not bool or type(a['amount']) not in (int,float) or not math.isfinite(a['amount']):raise ValueError('invalid action')
  groups[r['conversation_id']].append(r)
 for cid,turns in groups.items():
  if len({r['split'] for r in turns})!=1 or len({r['family'] for r in turns})!=1:raise ValueError('conversation leakage')
  if sorted(r['turn_index'] for r in turns)!=list(range(len(turns))):raise ValueError('noncontiguous turns')
 return groups
def wilson(k,n):
 if not n:return None
 z=1.95996398454;p=k/n;d=1+z*z/n;c=(p+z*z/(2*n))/d;m=z*math.sqrt(p*(1-p)/n+z*z/(4*n*n))/d
 return [max(0,c-m),min(1,c+m)]
def metrics(events):
 tp=sum(not e['allowed'] and not e['expected_allow'] for e in events)
 tn=sum(e['allowed'] and e['expected_allow'] for e in events)
 fp=sum(not e['allowed'] and e['expected_allow'] for e in events)
 fn=sum(e['allowed'] and not e['expected_allow'] for e in events)
 return dict(n=len(events),tp=tp,tn=tn,fp=fp,fn=fn,accuracy=(tp+tn)/len(events) if events else None,false_approved_rate=fn/(tp+fn) if tp+fn else None,false_approved_wilson95=wilson(fn,tp+fn),false_blocked_rate=fp/(tn+fp) if tn+fp else None,false_blocked_wilson95=wilson(fp,tn+fp))
def evaluate(rows):
 groups=validate(rows);events=[]
 for cid in sorted(groups):
  for r in sorted(groups[cid],key=lambda x:x['turn_index']):
   allowed,reason=authorize(POLICY,Action(**r['action']))
   events.append(dict(conversation_id=cid,turn_index=r['turn_index'],family=r['family'],expected_allow=r['expected_allow'],allowed=allowed,reason=reason))
 families=defaultdict(list)
 for e in events:families[e['family']].append(e)
 escaped={cid:any(e['allowed'] and not e['expected_allow'] for e in events if e['conversation_id']==cid) for cid in groups}
 digest=hashlib.sha256(json.dumps(rows,sort_keys=True,separators=(',',':'),allow_nan=False).encode()).hexdigest()
 return dict(schema='gri-external-turns-v1',dataset_sha256=digest,policy_sha256=POLICY.digest,conversations=len(groups),conversation_escape_count=sum(escaped.values()),conversation_escape_rate=sum(escaped.values())/len(groups),conversation_escape_wilson95=wilson(sum(escaped.values()),len(groups)),turn_metrics=metrics(events),by_family={k:metrics(v) for k,v in sorted(families.items())},events=events,caveats=['Labels must be independently verified; metadata alone is not proof','No semantic LLM or real tool execution','Conversation escape is an authorization decision, not an observed side effect'])
def paired_compare(a,b,iterations=4000,seed=20261024):
 ga=validate(a);gb=validate(b)
 if set(ga)!=set(gb):raise ValueError('different conversations')
 ea=evaluate(a)['events'];eb=evaluate(b)['events']
 def group(events):
  g=defaultdict(list)
  for e in events:g[e['conversation_id']].append(e)
  return {cid:(any(x['allowed'] and not x['expected_allow'] for x in v),[(x['turn_index'],x['expected_allow']) for x in v]) for cid,v in g.items()}
 x=group(ea);y=group(eb);ids=sorted(x)
 if any(x[i][1]!=y[i][1] for i in ids):raise ValueError('different labels')
 diffs=[int(y[i][0])-int(x[i][0]) for i in ids];rng=random.Random(seed);samples=[]
 for _ in range(iterations):samples.append(sum(diffs[rng.randrange(len(ids))] for _ in ids)/len(ids))
 samples.sort()
 return dict(conversations=len(ids),delta_escape_rate_b_minus_a=sum(diffs)/len(ids),bootstrap95_percentile=[samples[int(.025*iterations)],samples[min(iterations-1,int(.975*iterations))]],seed=seed,iterations=iterations,caveat='Cluster bootstrap; exploratory uncertainty not causal proof')
if __name__=='__main__':
 parser=argparse.ArgumentParser();parser.add_argument('--dataset',required=True);parser.add_argument('--out',required=True);args=parser.parse_args()
 with open(args.out,'w',encoding='utf8') as f:json.dump(evaluate(load(args.dataset)),f,indent=2)
