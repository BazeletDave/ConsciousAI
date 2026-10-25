"""Versioned, verifiable research evidence bridge. Offline; not a trusted audit service."""
from dataclasses import dataclass
from hashlib import sha256
import json
from typing import Mapping

from governance import Metrics, Policy, Request, assess


def canonical(value):
    return json.dumps(value, sort_keys=True, separators=(",", ":"), allow_nan=False)


def digest(value):
    return sha256(canonical(value).encode("utf-8")).hexdigest()


@dataclass(frozen=True)
class Evidence:
    source_id: str
    source_type: str
    classification: str
    provenance: str
    source_digest: str

    def __post_init__(self):
        if any(not isinstance(x, str) or not x.strip() for x in vars(self).values()):
            raise ValueError("complete evidence metadata required")
        if self.classification not in ("SYNTHETIC", "PUBLIC_SOURCE", "RESEARCH_OBSERVATION"):
            raise ValueError("unknown evidence classification")
        if len(self.source_digest) != 64 or any(c not in "0123456789abcdef" for c in self.source_digest):
            raise ValueError("source_digest must be lowercase SHA256")


class EvidenceLedger:
    def __init__(self):
        self._entries = []

    def append(self, req: Request, policy: Policy, evidence: Evidence, approved=False):
        if evidence.classification != "SYNTHETIC":
            raise ValueError("offline experiments require synthetic evidence")
        decision = assess(req, policy, approved)
        body = {
            "schema_version": "gri.evidence.v1",
            "sequence": len(self._entries),
            "previous_digest": self._entries[-1]["entry_digest"] if self._entries else "0" * 64,
            "evidence": vars(evidence),
            "decision": decision,
            "evidence_link": digest({"source_id": evidence.source_id, "source_digest": evidence.source_digest}),
        }
        entry = {**body, "entry_digest": digest(body)}
        self._entries.append(entry)
        return entry

    def export(self):
        return json.loads(canonical(self._entries))


def verify_chain(entries, expected_tip=None):
    previous = "0" * 64
    for i, entry in enumerate(entries):
        if not isinstance(entry, dict) or entry.get("sequence") != i or entry.get("previous_digest") != previous:
            return False
        body = {k: v for k, v in entry.items() if k != "entry_digest"}
        if digest(body) != entry.get("entry_digest"):
            return False
        ev = entry.get("evidence", {})
        if entry.get("evidence_link") != digest({"source_id": ev.get("source_id"), "source_digest": ev.get("source_digest")}):
            return False
        decision = entry.get("decision", {})
        decision_body = {k: v for k, v in decision.items() if k != "record_sha256"}
        if digest(decision_body) != decision.get("record_sha256"):
            return False
        previous = entry["entry_digest"]
    return expected_tip is None or previous == expected_tip
