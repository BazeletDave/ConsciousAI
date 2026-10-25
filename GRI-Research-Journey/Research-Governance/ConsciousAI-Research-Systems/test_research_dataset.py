import unittest
from build_research_dataset import build,group_holdout,manifest
from research_benchmark import validate,majority_baseline
class DatasetGovernanceTests(unittest.TestCase):
 def test_public_metadata_only(self):
  rows=build([{"id":"CASE-A","organization":"Research","source":"https://example.org","claim":"Not to be reproduced"}],[])
  self.assertEqual(len(rows),1)
  self.assertNotIn("claim",rows[0])
  self.assertEqual(rows[0]["rights_status"],"public_metadata_only_review_pending")
 def test_family_grouping(self):
  rows=[{"record_id":str(i),"case_family":"A" if i<5 else "B"} for i in range(10)]
  split=group_holdout(rows)
  self.assertEqual(len({r["split"] for r in split if r["case_family"]=="A"}),1)
  self.assertEqual(len({r["split"] for r in split if r["case_family"]=="B"}),1)
  self.assertEqual({r["split"] for r in split},{"development","holdout"})
 def test_unreviewed_data_blocks_benchmark(self):
  rows=group_holdout(build([{"id":"A","source":"https://example.org"}],[{"id":"B","primary_source_url":"https://example.org/b"}]))
  self.assertFalse(validate(rows)["eligible"])
  self.assertEqual(majority_baseline([x for x in rows if x["split"]=="development"],[x for x in rows if x["split"]=="holdout"])["status"],"blocked")
 def test_leakage_rejected(self):
  rows=[{"record_id":"1","case_family":"same","split":"development"},{"record_id":"2","case_family":"same","split":"holdout"}]
  self.assertIn("group_leakage",validate(rows)["issues"])
if __name__=="__main__":unittest.main()
