import unittest
from php_case_study import classify, analyze, render_markdown

class CaseStudyTests(unittest.TestCase):
    def test_upstream_thresholds(self):
        for minor, old, fixed in [(2,34,35),(3,35,36),(4,26,27),(5,11,12)]:
            self.assertEqual(classify(f"8.{minor}.{old}"), "update_required")
            self.assertEqual(classify(f"8.{minor}.{fixed}"), "fixed_version_reported")
    def test_unknown_is_not_safe(self):
        self.assertEqual(classify("8.6.0"), "unknown_branch_review")
        self.assertEqual(classify("bad"), "unknown_version")
        self.assertEqual(classify("7.4.33"), "unsupported_review")
    def test_backport_needs_verification(self):
        self.assertEqual(classify("8.3.35", "vendor advisory #123"), "vendor_verification_required")
    def test_report(self):
        rows=analyze({"assets":[{"name":"test","php_version":"8.3.35","internet_facing":True}]})
        self.assertEqual(rows[0]["priority"],"urgent_review")
        self.assertIn("test",render_markdown(rows))

if __name__ == "__main__":
    unittest.main()
