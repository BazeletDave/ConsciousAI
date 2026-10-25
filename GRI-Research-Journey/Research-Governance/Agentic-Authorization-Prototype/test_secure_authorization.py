import unittest
from dataclasses import replace
from guardrail import Policy, Action
from secure_authorization import issue_grant, verify_and_authorize, ReplayStore

class SignedAuthorizationTests(unittest.TestCase):
    def setUp(self):
        self.key = b'k' * 32
        self.policy = Policy('mobility', ('book ride',), ('reserve',), ('user:123',), 100)
        self.action = Action('mobility', 'book ride', 'reserve', 'user:123', 35, False)
        self.grant, self.sig = issue_grant(self.key, principal='alice', agent_id='mobility',
            policy_digest=self.policy.digest, intent='book ride', tool='reserve',
            resource='user:123', amount=35, ttl_seconds=60, now=1000)
    def check(self, grant=None, signature=None, action=None, policy=None, principal='alice', store=None, now=1001):
        return verify_and_authorize(self.key, grant or self.grant, signature or self.sig,
            action or self.action, policy or self.policy, principal, store or ReplayStore(), now)
    def test_signed_grant_allows_once(self):
        store = ReplayStore()
        self.assertEqual(self.check(store=store), (True, 'authorized'))
        self.assertEqual(self.check(store=store), (False, 'replay'))
    def test_rejects_forgery_and_expiry(self):
        self.assertEqual(self.check(signature='0'*64)[1], 'invalid_signature')
        self.assertEqual(self.check(now=1060)[1], 'expired')
        self.assertEqual(self.check(principal='bob')[1], 'principal_mismatch')
        self.assertEqual(self.check(grant=replace(self.grant, amount=99))[1], 'invalid_signature')
    def test_rejects_scope_and_policy_change(self):
        self.assertEqual(self.check(action=replace(self.action, amount=36))[1], 'scope_mismatch')
        self.assertEqual(self.check(policy=replace(self.policy, max_amount=50))[1], 'stale_policy')
    def test_no_approval_without_grant(self):
        self.assertEqual(self.check(action=replace(self.action, tool='transfer'))[1], 'scope_mismatch')

if __name__ == '__main__': unittest.main()
