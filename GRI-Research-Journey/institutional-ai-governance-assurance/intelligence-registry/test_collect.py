import unittest
from collect import collect,merge,SOURCES

class CollectorTests(unittest.TestCase):
    def fake(self,url):
        name=url.split('/repos/')[1]
        return {'full_name':name,'updated_at':'2026-10-24T00:00:00Z','pushed_at':'2026-10-24T00:00:00Z','default_branch':'main'}
    def test_collect_only_allowlisted_repos(self):
        items=collect(fetch=self.fake,now='2026-10-24T00:00:00Z')
        self.assertEqual(len(items),len(SOURCES))
        self.assertTrue(all(x['human_review_required'] and not x['automated_enforcement'] for x in items))
    def test_reject_identity_mismatch(self):
        with self.assertRaises(ValueError):
            collect(fetch=lambda url:{'full_name':'attacker/repo'})
    def test_preserve_first_seen_and_review(self):
        item=collect(fetch=self.fake,now='later')[0]
        old={**item,'first_seen_at':'earlier','review_status':'SOURCE_REVIEWED'}
        merged=merge({'records':[old]},[item])
        self.assertEqual(merged['records'][0]['first_seen_at'],'earlier')
        self.assertEqual(merged['records'][0]['review_status'],'SOURCE_REVIEWED')
if __name__=='__main__':unittest.main()
