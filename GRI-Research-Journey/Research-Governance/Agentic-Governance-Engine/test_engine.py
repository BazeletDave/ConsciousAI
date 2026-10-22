import unittest, threading
from engine import GovernanceEngine, Capability, Action, sign_capability

class GovernanceTests(unittest.TestCase):
    def setUp(self):
        self.key=b"test-key"
        self.engine=GovernanceEngine(self.key, hourly_cap="100",burst=100,refill_per_second=100)
        self.now=100000.
        self.claims=dict(token_id="t1",agent_id="a",asset_pair="EUR/USD",max_single="70",
            max_hourly="90",not_before=99900.,expires_at=101000.)
    def cap(self,**changes):
        claims={**self.claims,**changes}
        return Capability(**claims,signature=sign_capability(claims,self.key))
    def act(self,ident,amount="20",agent="a",pair="EUR/USD"):
        return Action(ident,agent,pair,amount)
    def evaluate(self,action,cap=None,now=None):
        return self.engine.evaluate(action,cap or self.cap(),now=self.now if now is None else now,tick=1000.)
    def test_valid_and_integrity(self):
        self.assertEqual(self.evaluate(self.act("a"))["status"],"AUTHORIZED_SIMULATION")
        self.assertTrue(self.engine.ledger.verify())
        self.engine.ledger.records[0]["amount"]="999"
        self.assertFalse(self.engine.ledger.verify())
    def test_forgery_and_scope(self):
        forged=self.cap()
        forged=Capability(**{**forged.__dict__,"signature":"bad"})
        self.assertEqual(self.evaluate(self.act("1"),forged)["status"],"REJECTED_AUTHORITY")
        self.assertEqual(self.evaluate(self.act("2",agent="other"))["status"],"REJECTED_AUTHORITY")
        self.assertEqual(self.evaluate(self.act("3",pair="GBP/USD"))["status"],"REJECTED_AUTHORITY")
    def test_invalid_amount_and_duplicate(self):
        for i,amount in enumerate(["-1","NaN","Infinity","0","0.001"]):
            self.assertEqual(self.evaluate(self.act(str(i),amount))["status"],"REJECTED_INPUT")
        self.evaluate(self.act("unique"))
        self.assertEqual(self.evaluate(self.act("unique"))["status"],"REJECTED_DUPLICATE")
    def test_expiry_revocation(self):
        self.assertEqual(self.evaluate(self.act("1"),now=101001)["status"],"REJECTED_AUTHORITY")
        self.engine.revoke("t1")
        self.assertEqual(self.evaluate(self.act("2"),now=101002)["status"],"REJECTED_AUTHORITY")
    def test_limits(self):
        self.assertEqual(self.evaluate(self.act("1","70"))["status"],"AUTHORIZED_SIMULATION")
        self.assertEqual(self.evaluate(self.act("2","30"))["status"],"REJECTED_LIMIT")
    def test_concurrent_atomic(self):
        results=[]
        def run(i):
            results.append(self.evaluate(self.act(str(i),"60"))["status"])
        threads=[threading.Thread(target=run,args=(i,)) for i in range(10)]
        for t in threads:t.start()
        for t in threads:t.join()
        self.assertEqual(results.count("AUTHORIZED_SIMULATION"),1)
        self.assertTrue(self.engine.ledger.verify())
    def test_breaker_requires_operator(self):
        e=GovernanceEngine(self.key,burst=1,refill_per_second=0.001)
        cap=self.cap()
        e.evaluate(self.act("1"),cap,now=self.now,tick=1000)
        self.assertEqual(e.evaluate(self.act("2"),cap,now=self.now,tick=1000)["status"],"REJECTED_CIRCUIT")
        with self.assertRaises(PermissionError):e.reset()
        e.reset(operator_approved=True)
        self.assertFalse(e.tripped)

if __name__=="__main__":unittest.main()
