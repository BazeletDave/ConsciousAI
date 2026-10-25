import unittest
from dataclasses import replace
from guardrail import Policy, Action, authorize, evaluate

class GuardrailTests(unittest.TestCase):
    def setUp(self):
        self.policy = Policy('mobility', ('book ride',), ('reserve',), ('user:123',), 100)
        self.valid = Action('mobility', 'book ride', 'reserve', 'user:123', 35, True)

    def test_authorized(self):
        self.assertEqual(authorize(self.policy, self.valid), (True, 'authorized'))

    def test_fail_closed_boundaries(self):
        changes = [({'agent_id': 'bank'}, 'agent_mismatch'),
                   ({'intent': 'transfer money'}, 'intent_out_of_scope'),
                   ({'tool': 'transfer'}, 'tool_not_allowed'),
                   ({'resource': 'user:999'}, 'resource_not_allowed'),
                   ({'amount': 101}, 'amount_out_of_bounds'),
                   ({'amount': -1}, 'amount_out_of_bounds'),
                   ({'approved': False}, 'human_approval_required')]
        for change, reason in changes:
            with self.subTest(change=change):
                self.assertEqual(authorize(self.policy, replace(self.valid, **change)), (False, reason))

    def test_evaluation(self):
        result = evaluate(self.policy, [(self.valid, False), (replace(self.valid, approved=False), True)])
        self.assertEqual((result['tp'], result['tn'], result['fp'], result['fn']), (1, 1, 0, 0))
        self.assertEqual(result['accuracy'], 1)

    def test_policy_digest(self):
        self.assertEqual(self.policy.digest, self.policy.digest)
        self.assertNotEqual(self.policy.digest, Policy('other', (), (), ()).digest)

if __name__ == '__main__': unittest.main()
