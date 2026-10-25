"""GRI independent research prototype. Deterministic action authorization, not a semantic LLM guardrail."""
from dataclasses import dataclass
from hashlib import sha256
import json
import re

@dataclass(frozen=True)
class Policy:
    agent_id: str
    allowed_intents: tuple[str, ...]
    allowed_tools: tuple[str, ...]
    allowed_resources: tuple[str, ...]
    max_amount: float = 0.0
    require_approval: bool = True

    @property
    def digest(self):
        return sha256(json.dumps(self.__dict__, sort_keys=True).encode()).hexdigest()

@dataclass(frozen=True)
class Action:
    agent_id: str
    intent: str
    tool: str
    resource: str
    amount: float = 0.0
    approved: bool = False

def screen_intent(policy: Policy, intent: str) -> bool:
    normalize = lambda s: re.sub(r'\s+', ' ', s.strip().lower())
    return normalize(intent) in {normalize(x) for x in policy.allowed_intents}

def authorize(policy: Policy, action: Action) -> tuple[bool, str]:
    """Fail closed; this function never executes a tool."""
    if action.agent_id != policy.agent_id:
        return False, 'agent_mismatch'
    if not screen_intent(policy, action.intent):
        return False, 'intent_out_of_scope'
    if action.tool not in policy.allowed_tools:
        return False, 'tool_not_allowed'
    if action.resource not in policy.allowed_resources:
        return False, 'resource_not_allowed'
    if action.amount < 0 or action.amount > policy.max_amount:
        return False, 'amount_out_of_bounds'
    if policy.require_approval and not action.approved:
        return False, 'human_approval_required'
    return True, 'authorized'

def evaluate(policy, labeled_actions):
    """BLOCK is positive. Ground truth supplied independently by test author."""
    tp = fp = tn = fn = 0
    for action, should_block in labeled_actions:
        allowed, _ = authorize(policy, action)
        blocked = not allowed
        if blocked and should_block: tp += 1
        elif blocked and not should_block: fp += 1
        elif not blocked and should_block: fn += 1
        else: tn += 1
    n = tp + tn + fp + fn
    return {'n': n, 'tp': tp, 'tn': tn, 'fp': fp, 'fn': fn,
            'accuracy': (tp + tn) / n if n else None,
            'false_approved_rate': fn / (fn + tp) if fn + tp else None,
            'false_blocked_rate': fp / (fp + tn) if fp + tn else None}
