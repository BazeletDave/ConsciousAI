"""Research-only authorization reference: HMAC-signed, scoped, expiring, one-use grants.
Do not expose signing keys to agents. In-memory replay store is not multi-process safe.
"""
from dataclasses import dataclass
from hashlib import sha256
import hmac
import json
import math
import secrets
import time

@dataclass(frozen=True)
class Grant:
    principal: str
    agent_id: str
    policy_digest: str
    intent: str
    tool: str
    resource: str
    amount: float
    expires_at: int
    nonce: str

def canonical(grant):
    return json.dumps(grant.__dict__, sort_keys=True, separators=(',', ':'), allow_nan=False).encode()

def issue_grant(key, *, principal, agent_id, policy_digest, intent, tool, resource, amount, ttl_seconds=60, now=None):
    if not isinstance(key, bytes) or len(key) < 32: raise ValueError('key must be >=32 bytes')
    if not principal or not agent_id or not policy_digest: raise ValueError('missing identity or policy')
    if not isinstance(ttl_seconds, int) or not 1 <= ttl_seconds <= 300: raise ValueError('invalid ttl')
    if not isinstance(amount, (int,float)) or not math.isfinite(amount) or amount < 0: raise ValueError('invalid amount')
    issued_at = int(time.time() if now is None else now)
    grant = Grant(principal, agent_id, policy_digest, intent, tool, resource, float(amount), issued_at + ttl_seconds, secrets.token_hex(16))
    signature = hmac.new(key, canonical(grant), sha256).hexdigest()
    return grant, signature

class ReplayStore:
    """Demo-only single-process replay protection; production needs atomic shared storage."""
    def __init__(self): self.used = set()
    def consume(self, nonce):
        if nonce in self.used: return False
        self.used.add(nonce)
        return True

def verify_and_authorize(key, grant, signature, action, policy, principal, replay_store, now=None):
    from guardrail import authorize
    if not isinstance(key, bytes) or len(key) < 32: return False, 'invalid_key'
    if not isinstance(grant, Grant) or not isinstance(signature, str): return False, 'invalid_grant'
    if not isinstance(replay_store, ReplayStore): return False, 'invalid_replay_store'
    expected = hmac.new(key, canonical(grant), sha256).hexdigest()
    if not hmac.compare_digest(expected, signature): return False, 'invalid_signature'
    if int(time.time() if now is None else now) >= grant.expires_at: return False, 'expired'
    if not principal or grant.principal != principal: return False, 'principal_mismatch'
    if grant.policy_digest != policy.digest: return False, 'stale_policy'
    fields = ('agent_id', 'intent', 'tool', 'resource', 'amount')
    if any(getattr(grant, f) != getattr(action, f) for f in fields): return False, 'scope_mismatch'
    if not math.isfinite(action.amount): return False, 'invalid_amount'
    from dataclasses import replace
    ok, reason = authorize(policy, replace(action, approved=True))
    if not ok: return False, reason
    if not replay_store.consume(grant.nonce): return False, 'replay'
    return True, 'authorized'
