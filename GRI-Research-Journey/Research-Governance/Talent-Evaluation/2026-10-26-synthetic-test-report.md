# Talent evaluation: synthetic validation harness

This is a **synthetic unit test**, not a candidate evaluation, hiring prediction, fairness audit, or model benchmark. Run: `python3 test_protocol.py`.

```python
import unittest
COMP=['governance','software','leadership','audit']
CASES={'resume':{'leadership'},'portfolio':{'leadership','software','governance'},'verified':{'leadership','software','governance','audit'}}
def coverage(evidence, rubric=COMP):
    if not rubric: raise ValueError('empty rubric')
    return len(set(evidence)&set(rubric))/len(set(rubric))
def precision(claims):
    if not claims: return None
    return sum(x['verified'] for x in claims)/len(claims)
class Tests(unittest.TestCase):
 def test_monotonic(self):
  self.assertLessEqual(coverage(CASES['resume']),coverage(CASES['portfolio']))
  self.assertLessEqual(coverage(CASES['portfolio']),coverage(CASES['verified']))
 def test_no_double_count(self):self.assertEqual(coverage(['software','software']),.25)
 def test_missing_evidence(self):self.assertEqual(coverage([]),0)
 def test_empty_rubric(self):
  with self.assertRaises(ValueError):coverage(['software'],[])
 def test_unsupported(self):self.assertEqual(precision([{'verified':True},{'verified':False}]),.5)
 def test_empty_claims(self):self.assertIsNone(precision([]))
 def test_irrelevant(self):self.assertEqual(coverage(['golf']),0)
 def test_no_identity_proxy(self):self.assertEqual(coverage(['leadership','age:55']),.25)
if __name__=='__main__':unittest.main(verbosity=2)
```

**Local execution, 2026-10-26:** 8/8 passed. This tests arithmetic and invariants only; not job validity or algorithmic bias.

## Evidence inputs inspected

- [GRI institutional governance research architecture](../../institutional-ai-governance-assurance/research-program-architecture.md): Treasury-origin prototype explicitly not federal validated.
- [GRI source and claim register](../SOURCE-AND-CLAIM-REGISTER.md): initial inventory, not verification certificate.
- [Nelson model methodological boundaries](../../Integrated-Research-Journey/nelson-model-methodological-boundaries.md): institutional analysis must not misapply financial crisis indicators.
- [Talent evaluation research protocol](2026-10-26-evidence-based-ai-talent-evaluation.md).

## External methodological authorities

- [NIST AI RMF](https://airc.nist.gov/airmf-resources/airmf/5-sec-core/): Govern, Map, Measure, Manage.
- [OPM Merit Hiring Plan](https://www.opm.gov/policy-data-oversight/latest-memos/merit-hiring-plan): technical and alternative assessments.
- [OPM assessment guidance February 2026](https://www.opm.gov/policy-data-oversight/hiring-information/merit-hiring-plan-resources/guidance-on-use-of-hiring-assessments-when-utilizing-direct-hire-authority.pdf): work samples, structured interviews, and job relevant tests.

## Not yet tested

No private Treasury submission was located or verified in this run. No third-party personal dossiers were ingested. No actual AI model repeated-trial evaluation, protected-group fairness analysis, blinded human review, or predictive validity study was conducted. The three evidence sets are synthetic, not observations about any person. Before empirical execution, obtain consent or public lawful data, preserve original job requirements, verify artifact ownership, and pre-register rubrics.
