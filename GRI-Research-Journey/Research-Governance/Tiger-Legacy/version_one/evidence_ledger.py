"""Synthetic-only durable SQLite evidence ledger. External checkpoint custody required."""
import hashlib
import hmac
import json
import sqlite3
from pathlib import Path
from tiger_legacy import canonical

GENESIS = "0" * 64

class EvidenceLedger:
    def __init__(self, path, key):
        if not isinstance(key, bytes) or len(key) < 32:
            raise ValueError("research HMAC key must be >=32 bytes")
        self.path = str(path)
        self.key = key
        with self._db() as db:
            db.execute("""CREATE TABLE IF NOT EXISTS events (
                seq INTEGER PRIMARY KEY, event_id TEXT NOT NULL UNIQUE,
                payload TEXT NOT NULL, previous TEXT NOT NULL,
                digest TEXT NOT NULL, mac TEXT NOT NULL)""")
            db.execute("""CREATE TRIGGER IF NOT EXISTS prevent_event_update
                BEFORE UPDATE ON events BEGIN SELECT RAISE(ABORT, 'immutable evidence'); END""")
            db.execute("""CREATE TRIGGER IF NOT EXISTS prevent_event_delete
                BEFORE DELETE ON events BEGIN SELECT RAISE(ABORT, 'immutable evidence'); END""")

    def _db(self):
        db = sqlite3.connect(self.path, timeout=5, isolation_level=None)
        db.execute("PRAGMA busy_timeout=5000")
        db.execute("PRAGMA synchronous=FULL")
        return db

    def append(self, event_id, payload):
        if not isinstance(event_id, str) or not event_id or not isinstance(payload, dict):
            raise ValueError("invalid event")
        encoded = canonical(payload).decode("utf-8")
        with self._db() as db:
            db.execute("BEGIN IMMEDIATE")
            row = db.execute("SELECT seq,digest FROM events ORDER BY seq DESC LIMIT 1").fetchone()
            seq = row[0] + 1 if row else 0
            previous = row[1] if row else GENESIS
            record = {"seq": seq, "event_id": event_id, "payload": json.loads(encoded), "previous": previous}
            digest = hashlib.sha256(canonical(record)).hexdigest()
            mac = hmac.new(self.key, digest.encode(), hashlib.sha256).hexdigest()
            db.execute("INSERT INTO events VALUES (?,?,?,?,?,?)", (seq,event_id,encoded,previous,digest,mac))
        return digest

    def rows(self):
        with self._db() as db:
            return db.execute("SELECT seq,event_id,payload,previous,digest,mac FROM events ORDER BY seq").fetchall()

    def verify(self, checkpoint=None):
        previous = GENESIS
        rows = self.rows()
        for index, (seq, event_id, payload, link, digest, mac) in enumerate(rows):
            if seq != index or link != previous:
                return False
            try:
                record = {"seq": seq, "event_id": event_id, "payload": json.loads(payload), "previous": link}
                expected = hashlib.sha256(canonical(record)).hexdigest()
            except (ValueError, TypeError):
                return False
            if not hmac.compare_digest(digest, expected):
                return False
            if not hmac.compare_digest(mac, hmac.new(self.key, digest.encode(), hashlib.sha256).hexdigest()):
                return False
            previous = digest
        if checkpoint is not None:
            if not isinstance(checkpoint, dict) or checkpoint.get("count") != len(rows) or checkpoint.get("head") != previous:
                return False
        return True

    def checkpoint(self):
        if not self.verify():
            raise ValueError("ledger integrity invalid")
        rows = self.rows()
        return {"schema": "gri.tiger_legacy.ledger_checkpoint.v1", "count": len(rows),
                "head": rows[-1][4] if rows else GENESIS,
                "custody": "export_only_external_custodian_not_implemented"}

    def backup(self, destination):
        if Path(destination).resolve() == Path(self.path).resolve():
            raise ValueError("backup destination must differ")
        with self._db() as src, sqlite3.connect(destination) as dst:
            src.backup(dst)
        return str(destination)
