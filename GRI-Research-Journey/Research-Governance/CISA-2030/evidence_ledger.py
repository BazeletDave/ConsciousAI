"""Local authenticated, append-only CISA2030 evidence ledger. No HTTP, network or production hooks."""
import hashlib
import hmac
import json
import sqlite3
from datetime import datetime, timezone
from pathlib import Path

def canonical(value):
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True).encode()

def digest(value):
    return hashlib.sha256(canonical(value)).hexdigest()

def utc_now():
    return datetime.now(timezone.utc).isoformat()

class EvidenceLedger:
    def __init__(self, db_path, keys):
        """keys: {principal_id: (role, secret_bytes)}; caller must supply secrets securely."""
        if not keys or any(role not in ("collector", "reviewer", "auditor") or not isinstance(secret, bytes) or len(secret) < 32
                           for role, secret in keys.values()):
            raise ValueError("invalid role/key configuration")
        self.keys = keys
        self.db = sqlite3.connect(str(db_path))
        self.db.execute("PRAGMA foreign_keys=ON")
        self.db.executescript("""
            CREATE TABLE IF NOT EXISTS events(
              sequence INTEGER PRIMARY KEY AUTOINCREMENT,
              event_type TEXT NOT NULL,
              principal TEXT NOT NULL,
              event_json TEXT NOT NULL,
              previous_hash TEXT NOT NULL,
              event_hash TEXT NOT NULL UNIQUE,
              signature TEXT NOT NULL
            );
            CREATE TRIGGER IF NOT EXISTS no_event_update BEFORE UPDATE ON events BEGIN SELECT RAISE(ABORT,'append only'); END;
            CREATE TRIGGER IF NOT EXISTS no_event_delete BEFORE DELETE ON events BEGIN SELECT RAISE(ABORT,'append only'); END;
        """)

    def _authorize(self, principal, role):
        entry = self.keys.get(principal)
        if entry is None or entry[0] != role:
            raise PermissionError("unauthorized role")
        return entry[1]

    def _append(self, event_type, principal, role, payload):
        secret = self._authorize(principal, role)
        self.db.execute("BEGIN IMMEDIATE")
        try:
            previous = self.db.execute("SELECT event_hash FROM events ORDER BY sequence DESC LIMIT 1").fetchone()
            previous_hash = previous[0] if previous else "0" * 64
            event = {"type": event_type, "principal": principal, "payload": payload, "timestamp": utc_now()}
            event_hash = digest({"previous_hash": previous_hash, "event": event})
            signature = hmac.new(secret, event_hash.encode(), hashlib.sha256).hexdigest()
            self.db.execute("INSERT INTO events(event_type,principal,event_json,previous_hash,event_hash,signature) VALUES(?,?,?,?,?,?)",
                            (event_type, principal, canonical(event).decode(), previous_hash, event_hash, signature))
            self.db.commit()
            return event_hash
        except Exception:
            self.db.rollback()
            raise

    def collect(self, principal, record, artifact_bytes):
        self._authorize(principal, "collector")
        if not isinstance(artifact_bytes, bytes) or not artifact_bytes or len(artifact_bytes) > 10_000_000:
            raise ValueError("artifact must be 1 to 10 MB of bytes")
        if not isinstance(record, dict) or record.get("scenario_type") == "synthetic":
            raise ValueError("only authorized nonsynthetic records")
        if record.get("consent_or_authority") is None or not str(record["consent_or_authority"]).strip():
            raise ValueError("authority required")
        if record.get("source_sha256") != hashlib.sha256(artifact_bytes).hexdigest():
            raise ValueError("artifact digest mismatch")
        if not isinstance(record.get("record_id"), str) or not record["record_id"]:
            raise ValueError("record_id required")
        for event in self.events():
            if event["type"] == "collect" and event["payload"]["record"]["record_id"] == record["record_id"]:
                raise ValueError("duplicate record")
        return self._append("collect", principal, "collector", {"record": record, "artifact_sha256": record["source_sha256"]})

    def review(self, principal, record_id, decision, rationale):
        self._authorize(principal, "reviewer")
        if decision not in ("approve", "reject") or not isinstance(rationale, str) or not rationale.strip():
            raise ValueError("decision and rationale required")
        events = self.events()
        collected = [e for e in events if e["type"] == "collect" and e["payload"]["record"]["record_id"] == record_id]
        if len(collected) != 1:
            raise ValueError("unknown record")
        if collected[0]["principal"] == principal:
            raise PermissionError("self-review forbidden")
        if any(e["type"] == "review" and e["payload"]["record_id"] == record_id for e in events):
            raise ValueError("already reviewed; use a new correction event in future version")
        return self._append("review", principal, "reviewer", {"record_id": record_id, "decision": decision, "rationale": rationale})

    def events(self):
        return [json.loads(row[0]) for row in self.db.execute("SELECT event_json FROM events ORDER BY sequence")]

    def verify(self):
        previous = "0" * 64
        count = 0
        for principal, raw, previous_hash, event_hash, signature in self.db.execute(
                "SELECT principal,event_json,previous_hash,event_hash,signature FROM events ORDER BY sequence"):
            event = json.loads(raw)
            if previous_hash != previous or event["principal"] != principal or canonical(event).decode() != raw:
                return {"valid": False, "events": count}
            expected = digest({"previous_hash": previous, "event": event})
            key = self.keys.get(principal)
            if expected != event_hash or key is None or not hmac.compare_digest(
                    hmac.new(key[1], event_hash.encode(), hashlib.sha256).hexdigest(), signature):
                return {"valid": False, "events": count}
            previous = event_hash
            count += 1
        return {"valid": True, "events": count, "head_sha256": previous}

    def approved_records(self, principal):
        self._authorize(principal, "auditor")
        if not self.verify()["valid"]:
            raise ValueError("ledger integrity failure")
        events = self.events()
        approved = {e["payload"]["record_id"] for e in events if e["type"] == "review" and e["payload"]["decision"] == "approve"}
        return [e["payload"]["record"] for e in events if e["type"] == "collect" and e["payload"]["record"]["record_id"] in approved]

    def close(self):
        self.db.close()
