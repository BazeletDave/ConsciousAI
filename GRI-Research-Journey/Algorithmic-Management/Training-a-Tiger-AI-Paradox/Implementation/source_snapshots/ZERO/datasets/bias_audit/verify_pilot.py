import importlib.util,json,tempfile
from pathlib import Path
root=Path(__file__).parent
spec=importlib.util.spec_from_file_location('gri_audit',root/'audit.py')
module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
rows=[json.loads(s) for s in (root/'synthetic_pilot.jsonl').read_text().splitlines()]
report=module.audit(root/'synthetic_pilot.jsonl')
assert report['integrity_passed'] and report['records']==36 and report['scenarios']==18
assert report['by_split']['train']['records']==24
assert report['by_split']['validation']['records']==6
assert report['by_split']['test']['records']==6
assert not report['training_release_approved']
with tempfile.TemporaryDirectory() as d:
 p=Path(d)/'input.jsonl'
 def check(mutator,fragment):
  changed=json.loads(json.dumps(rows));mutator(changed)
  p.write_text(''.join(json.dumps(r)+'\n' for r in changed))
  result=module.audit(p)
  assert not result['integrity_passed']
  assert any(fragment in e for e in result['errors']),result
 check(lambda r:r[0].update(split='test'),'scenario split leakage')
 check(lambda r:r[0].update(expected_label='unsupported'),'invalid expected_label')
 check(lambda r:r[0].pop('policy'),'missing or invalid fields')
 check(lambda r:r[0].update(record_id=r[1]['record_id']),'duplicate record_id')
 check(lambda r:r[0].update(expected_label='prohibited'),'paired label inconsistency')
print('PASS: valid fixture, partition counts, pending release, and five injected data failures')
