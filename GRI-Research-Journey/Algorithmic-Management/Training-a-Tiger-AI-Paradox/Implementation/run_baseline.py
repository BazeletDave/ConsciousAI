"""Reproduce existing checks, source identity, and bounded synthetic counterexamples."""
from pathlib import Path
import subprocess,sys,json,hashlib,importlib.util
from datetime import datetime,timezone
ROOT=Path(__file__).resolve().parent

def module(name,path):
 spec=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m

def main():
 steps=[('existing_engines',[sys.executable,'-m','unittest','discover','-s','source_snapshots/ConsciousAI/GRI-Research-Journey/Research-Governance/ConsciousAI-Research-Systems','-p','test_*engine.py','-v']),('zero_integrity',[sys.executable,'source_snapshots/ZERO/datasets/bias_audit/verify_pilot.py']),('new_lineage_checks',[sys.executable,'-m','unittest','test_claim_registry','-v'])]
 results=[]
 for name,cmd in steps:
  r=subprocess.run(cmd,cwd=ROOT,text=True,capture_output=True);results.append({'name':name,'exit_code':r.returncode,'stdout':r.stdout,'stderr':r.stderr})
 identities=[]
 for f in json.loads((ROOT/'source_manifest.json').read_text()):
  raw=(ROOT/f['snapshot_path']).read_bytes();sha=hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest();identities.append({'path':f['snapshot_path'],'expected_blob':f['blob_sha'],'actual_blob':sha,'matches':sha==f['blob_sha']})
 base=module('source_assurance',ROOT/'source_snapshots/ConsciousAI/GRI-Research-Journey/Research-Governance/ConsciousAI-Research-Systems/assurance_engine.py')
 from claim_registry import check
 same={'id':'synthetic-duplicate-origin','claim':'Synthetic claim for sensitivity testing','observed_at':'2026-10-28T00:00:00Z','verification_status':'verified','sources':[{'publisher':'Publisher A','url':'https://example.org/shared','independently_reviewed':True},{'publisher':'Publisher B','url':'https://example.org/shared','independently_reviewed':True}]}
 extended={'id':same['id'],'claim':same['claim'],'evidence_class':'synthetic_fixture','observed_at':same['observed_at'],'reviewer':'fixture reviewer','asserted_independent_corroboration':True,'sources':[dict(url=s['url'],origin_id='shared-original',independence_reviewed=True) for s in same['sources']]}
 comparison={'scope':'one synthetic duplicate-origin counterexample, not a population benchmark','existing_gate':base.evaluate(same),'lineage_gate':check(extended)}
 z=module('zero_audit',ROOT/'source_snapshots/ZERO/datasets/bias_audit/audit.py').audit(ROOT/'source_snapshots/ZERO/datasets/bias_audit/synthetic_pilot.jsonl')
 report={'generated_at':datetime.now(timezone.utc).isoformat(),'mode':'local_reproducibility_baseline_not_field_validation','checks':results,'source_identities':identities,'synthetic_counterexample':comparison,'zero_audit':z,'all_checks_passed':all(r['exit_code']==0 for r in results) and all(x['matches'] for x in identities)}
 (ROOT/'results').mkdir(exist_ok=True);(ROOT/'results/baseline.json').write_text(json.dumps(report,indent=2)+'\n')
 print(json.dumps({'all_checks_passed':report['all_checks_passed'],'source_files':len(identities),'zero_records':z['records'],'comparison':comparison},indent=2))
 return 0 if report['all_checks_passed'] else 1
if __name__=='__main__':raise SystemExit(main())
