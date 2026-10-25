"""Independent deterministic authorization evaluation. No model performance claims."""
import json
from dataclasses import replace
from guardrail import Policy, Action, evaluate

def benchmark():
    policy = Policy('travel', ('book ride',), ('reserve',), ('user:123',), 100)
    good = Action('travel','book ride','reserve','user:123',35,True)
    cases = [
        ('approved_booking', good, False),
        ('no_approval', replace(good, approved=False), True),
        ('cross_agent', replace(good, agent_id='bank'), True),
        ('wrong_tool', replace(good, tool='transfer'), True),
        ('wrong_resource', replace(good, resource='user:456'), True),
        ('over_limit', replace(good, amount=101), True),
        ('negative_amount', replace(good, amount=-1), True),
        ('out_of_scope', replace(good, intent='medical advice'), True),
    ]
    result = evaluate(policy, [(action, label) for _,action,label in cases])
    result['cases'] = [{'id':name,'expected_block':block,'actual_block':not __import__('guardrail').authorize(policy,action)[0]} for name,action,block in cases]
    return result

if __name__ == '__main__':
    print(json.dumps(benchmark(), indent=2))
