"""Append-only SQLite evidence ledger with content integrity checks. Research only."""
import json
import sqlite3
from datetime import datetime, timezone
from evidence_pipeline import normalize

class EvidenceStore:
    def __init__(self, database_path):
        self.db = sqlite3.connect(database_path)
        self.db.execute("""CREATE TABLE IF NOT EXISTS evidence (
            sequence INTEGER PRIMARY KEY AUTOINCREMENT,
            digest TEXT NOT NULL UNIQUE,
            payload TEXT NOT NULL,
            ingested_at TEXT NOT NULL)""")
        self.db.commit()

    def append(self, record):
        item = normalize(record)
        payload = json.dumps(item, sort_keys=True, separators=(",", ":"))
        timestamp = datetime.now(timezone.utc).isoformat()
        with self.db:
            self.db.execute("INSERT OR IGNORE INTO evidence (digest,payload,ingested_at) VALUES (?,?,?)",
                            (item["evidence_digest"], payload, timestamp))
        return item["evidence_digest"]

    def get(self, digest):
        row = self.db.execute("SELECT payload FROM evidence WHERE digest=?", (digest,)).fetchone()
        if row is None:
            return None
        item = json.loads(row[0])
        expected = normalize({k: item[k] for k in ("source_id","source_url","claim","captured_at","jurisdiction","verification_status")})
        if expected["evidence_digest"] != digest or expected != item:
            raise ValueError("stored evidence integrity mismatch")
        return item

    def count(self):
        return self.db.execute("SELECT COUNT(*) FROM evidence").fetchone()[0]

    def close(self):
        self.db.close()
