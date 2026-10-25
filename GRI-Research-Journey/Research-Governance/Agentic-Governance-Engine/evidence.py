"""Research evidence bundles: portable verification, not independently anchored.
No raw credentials or tokens are recorded.
"""
from dataclasses import dataclass, asdict
from datetime import datetime, timezone
from hashlib import sha256
import hmac, json, threading

ZERO = "0" * 64

def canonical(value):
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False,
                      allow_nan=False).encode("utf-8")

def digest(value):
    return sha256(canonical(value)).hexdigest()

@dataclass(frozen=True)
class Proof:
    record_index: int
    timestamp_utc: str
    action_id: str
    agent_id: str
    policy_version: str
    input_payload_hash: str
    decision_status: str
    rejection_reason: str | None
    previous_record_hash: str
    proof_hash: str

def verify_export(bundle: dict, *, trusted_checkpoint: dict | None = None) -> bool:
    """Validate all records and a supplied trusted head/size; checkpoint trust is external."""
    try:
        records = bundle["records"]
        expected_head = bundle["head"]
        expected_count = bundle["count"]
        if type(expected_count) is not int or expected_count != len(records):
            return False
        previous = ZERO
        for index, record in enumerate(records):
            if type(record["record_index"]) is not int or record["record_index"] != index:
                return False
            if record["previous_record_hash"] != previous:
                return False
            if not isinstance(record["input_payload_hash"],str) or len(record["input_payload_hash"]) != 64:
                return False
            state = {k:v for k,v in record.items() if k != "proof_hash"}
            computed = digest(state)
            if not hmac.compare_digest(computed, record["proof_hash"]):
                return False
            previous = computed
        if not hmac.compare_digest(previous, expected_head):
            return False
        if trusted_checkpoint is not None:
            if trusted_checkpoint.get("head") != expected_head or trusted_checkpoint.get("count") != expected_count:
                return False
        return True
    except (KeyError, TypeError, ValueError, OverflowError):
        return False

class EvidenceRecorder:
    def __init__(self, policy_version="v2.0.1"):
        self.policy_version = policy_version
        self.records = []
        self.head = ZERO
        self.lock = threading.RLock()

    def generate_proof(self, action_id, agent_id, input_payload, decision_status,
                       rejection_reason=None):
        with self.lock:
            state = {
                "record_index": len(self.records),
                "timestamp_utc": datetime.now(timezone.utc).isoformat(),
                "action_id": action_id,
                "agent_id": agent_id,
                "policy_version": self.policy_version,
                "input_payload_hash": digest(input_payload),
                "decision_status": decision_status,
                "rejection_reason": rejection_reason,
                "previous_record_hash": self.head,
            }
            proof = Proof(**state, proof_hash=digest(state))
            self.records.append(proof)
            self.head = proof.proof_hash
            return proof

    def export(self):
        with self.lock:
            return {"schema_version":"gri-evidence-v1","count":len(self.records),
                    "head":self.head,"records":[asdict(r) for r in self.records]}

    def verify(self, trusted_checkpoint=None):
        return verify_export(self.export(), trusted_checkpoint=trusted_checkpoint)
