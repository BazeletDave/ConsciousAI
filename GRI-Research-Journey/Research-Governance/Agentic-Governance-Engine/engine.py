"""GRI Agentic Governance Engine v2. Research-only deterministic enforcement core.
No network execution, real trading, credential handling, or production authorization.
"""
from __future__ import annotations
from dataclasses import dataclass
from decimal import Decimal, InvalidOperation
from collections import deque
from datetime import datetime, timezone
import hashlib, hmac, json, math, threading, time, uuid

def canonical(obj):
    return json.dumps(obj, sort_keys=True, separators=(",", ":"), allow_nan=False)

def money(value):
    try:
        amount = Decimal(str(value))
    except (InvalidOperation, ValueError):
        raise ValueError("Invalid monetary value")
    if not amount.is_finite() or amount <= 0 or amount.as_tuple().exponent < -2:
        raise ValueError("Amount must be positive, finite and have at most two decimals")
    return amount

@dataclass(frozen=True)
class Capability:
    token_id: str
    agent_id: str
    asset_pair: str
    max_single: str
    max_hourly: str
    not_before: float
    expires_at: float
    signature: str

    def claims(self):
        return {k: getattr(self,k) for k in (
            "token_id","agent_id","asset_pair","max_single","max_hourly",
            "not_before","expires_at")}

def sign_capability(claims, key):
    """HMAC signing for local laboratory simulation only. Use managed asymmetric keys in production."""
    return hmac.new(key, canonical(claims).encode(), hashlib.sha256).hexdigest()

@dataclass(frozen=True)
class Action:
    action_id: str
    agent_id: str
    asset_pair: str
    amount: str

class Ledger:
    """Append-only in-memory hash chain. NOT a Merkle tree or durable tamperproof storage."""
    def __init__(self):
        self.records = []
        self.head = "0" * 64

    def append(self, event):
        record = {"index": len(self.records), "previous_hash": self.head, **event}
        digest = hashlib.sha256(canonical(record).encode()).hexdigest()
        record["hash"] = digest
        self.records.append(record)
        self.head = digest
        return record

    def verify(self):
        prev = "0" * 64
        for idx, item in enumerate(self.records):
            data = {k:v for k,v in item.items() if k != "hash"}
            if data["index"] != idx or data["previous_hash"] != prev:
                return False
            digest = hashlib.sha256(canonical(data).encode()).hexdigest()
            if not hmac.compare_digest(digest, item["hash"]):
                return False
            prev = digest
        return prev == self.head

class GovernanceEngine:
    """All policy decisions and volume reservations are serialized under one lock."""
    def __init__(self, signing_key, hourly_cap="200000", burst=5, refill_per_second=5):
        if not signing_key or burst <= 0 or refill_per_second <= 0:
            raise ValueError("Invalid configuration")
        self.key = signing_key
        self.hourly_cap = money(hourly_cap)
        self.burst = float(burst)
        self.refill = float(refill_per_second)
        self.tokens = float(burst)
        self.last_tick = time.monotonic()
        self.lock = threading.RLock()
        self.ledger = Ledger()
        self.window = deque()
        self.token_windows = {}
        self.seen = set()
        self.revoked = set()
        self.tripped = False

    def _log(self, action, status, reason, now):
        self.ledger.append({"timestamp":datetime.fromtimestamp(now,timezone.utc).isoformat(),
            "action_id":action.action_id,"agent_id":action.agent_id,
            "asset_pair":action.asset_pair,"amount":str(action.amount),
            "status":status,"reason":reason})
        return {"status":status,"reason":reason,"ledger_hash":self.ledger.head}

    def evaluate(self, action, capability, *, now=None, tick=None):
        with self.lock:
            now = time.time() if now is None else float(now)
            tick = time.monotonic() if tick is None else float(tick)
            if not math.isfinite(now) or not math.isfinite(tick):
                raise ValueError("Invalid clock")
            if action.action_id in self.seen:
                return self._log(action,"REJECTED_DUPLICATE","Duplicate action ID",now)
            self.seen.add(action.action_id)
            if self.tripped:
                return self._log(action,"REJECTED_CIRCUIT","Circuit open",now)
            if not isinstance(capability, Capability):
                return self._log(action,"REJECTED_AUTHORITY","Missing capability",now)
            expected = sign_capability(capability.claims(),self.key)
            if not hmac.compare_digest(expected, capability.signature):
                return self._log(action,"REJECTED_AUTHORITY","Invalid signature",now)
            if capability.token_id in self.revoked:
                return self._log(action,"REJECTED_AUTHORITY","Revoked token",now)
            if not capability.not_before <= now < capability.expires_at:
                return self._log(action,"REJECTED_AUTHORITY","Capability outside validity window",now)
            if action.agent_id != capability.agent_id or action.asset_pair != capability.asset_pair:
                return self._log(action,"REJECTED_AUTHORITY","Agent or asset mismatch",now)
            try:
                amount = money(action.amount)
                single = money(capability.max_single)
                token_cap = money(capability.max_hourly)
            except ValueError:
                return self._log(action,"REJECTED_INPUT","Invalid amount or token limits",now)
            if amount > single:
                return self._log(action,"REJECTED_LIMIT","Single action cap exceeded",now)
            elapsed = max(0.0,tick-self.last_tick)
            self.tokens = min(self.burst,self.tokens+elapsed*self.refill)
            self.last_tick = max(self.last_tick,tick)
            if self.tokens < 1:
                self.tripped = True
                return self._log(action,"REJECTED_CIRCUIT","Velocity breaker activated",now)
            while self.window and now-self.window[0][0] >= 3600:
                self.window.popleft()
            token_window = self.token_windows.setdefault(capability.token_id,deque())
            while token_window and now-token_window[0][0] >= 3600:
                token_window.popleft()
            global_total = sum((a for _,a in self.window),Decimal("0"))
            token_total = sum((a for _,a in token_window),Decimal("0"))
            if global_total+amount > self.hourly_cap or token_total+amount > token_cap:
                return self._log(action,"REJECTED_LIMIT","Rolling hour limit exceeded",now)
            self.tokens -= 1
            self.window.append((now,amount))
            token_window.append((now,amount))
            return self._log(action,"AUTHORIZED_SIMULATION","Capacity reserved; no external execution",now)

    def revoke(self, token_id):
        with self.lock:
            self.revoked.add(token_id)

    def reset(self, operator_approved=False):
        with self.lock:
            if not operator_approved:
                raise PermissionError("Explicit operator approval required")
            self.tripped=False
            self.tokens=self.burst
            self.last_tick=time.monotonic()

    def snapshot(self):
        with self.lock:
            return {"circuit_open":self.tripped,"ledger_valid":self.ledger.verify(),
                "ledger_head":self.ledger.head,"events":len(self.ledger.records),
                "records":list(self.ledger.records)}
