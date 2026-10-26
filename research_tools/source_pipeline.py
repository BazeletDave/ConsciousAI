"""Offline, staging-only Reddit/YouTube export intake with persistent SQLite evidence ledger."""
import argparse, hashlib, ipaddress, json, sqlite3
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlsplit

PROVIDERS = {"reddit": ("reddit.com",), "youtube": ("youtube.com", "youtu.be")}

def allowed_url(value, provider):
    if not isinstance(value, str) or len(value) > 2048 or any(ord(c) < 32 for c in value):
        return False
    try:
        u = urlsplit(value)
        host = (u.hostname or "").lower().rstrip(".")
        try:
            ipaddress.ip_address(host)
            return False
        except ValueError:
            pass
        return (u.scheme == "https" and u.port in (None, 443) and not u.username
                and not u.password and not u.fragment and
                any(host == d or host.endswith("." + d) for d in PROVIDERS[provider]))
    except (ValueError, KeyError):
        return False

def normalize(provider, raw):
    if provider not in PROVIDERS or not isinstance(raw, dict):
        raise ValueError("unsupported provider or record")
    if raw.get("contains_personal_data") is not False:
        raise ValueError("privacy clearance missing")
    if raw.get("rights_basis") not in ("licensed", "public_metadata"):
        raise ValueError("rights not cleared")
    for key in ("url", "title", "summary", "observed_at"):
        if not isinstance(raw.get(key), str) or not raw[key].strip():
            raise ValueError("missing " + key)
    if len(raw["title"]) > 300 or len(raw["summary"]) > 2000:
        raise ValueError("oversized field")
    if not allowed_url(raw["url"], provider):
        raise ValueError("invalid source URL")
    try:
        date = datetime.fromisoformat(raw["observed_at"].replace("Z", "+00:00"))
        if date.tzinfo is None:
            raise ValueError()
    except ValueError:
        raise ValueError("invalid timestamp") from None
    return {k: raw[k] for k in ("url", "title", "summary", "observed_at", "rights_basis")} | {"source_type": provider}

def ingest(provider, items, database):
    db = sqlite3.connect(str(database))
    try:
        db.execute("PRAGMA busy_timeout=5000")
        db.execute("CREATE TABLE IF NOT EXISTS evidence (digest TEXT PRIMARY KEY, payload TEXT NOT NULL, status TEXT NOT NULL CHECK(status = 'HUMAN_REVIEW_REQUIRED'), inserted_at TEXT NOT NULL)")
        db.execute("CREATE TABLE IF NOT EXISTS events (id INTEGER PRIMARY KEY, digest TEXT, event TEXT NOT NULL, at TEXT NOT NULL)")
        counts = {"accepted": 0, "duplicate": 0, "rejected": 0, "errors": []}
        with db:
            for index, raw in enumerate(items):
                try:
                    record = normalize(provider, raw)
                    canonical = json.dumps(record, sort_keys=True, separators=(",", ":"), ensure_ascii=False)
                    digest = hashlib.sha256(canonical.encode()).hexdigest()
                    now = datetime.now(timezone.utc).isoformat()
                    candidate = dict(record, intake_id="GRI-" + digest[:16], digest=digest, evidence_class="UNVERIFIED_SOURCE_CANDIDATE", review_status="HUMAN_REVIEW_REQUIRED", training_eligible=False, publication_approved=False)
                    cursor = db.execute("INSERT OR IGNORE INTO evidence VALUES (?,?,?,?)", (digest, json.dumps(candidate, ensure_ascii=False), "HUMAN_REVIEW_REQUIRED", now))
                    if cursor.rowcount:
                        counts["accepted"] += 1
                        db.execute("INSERT INTO events(digest,event,at) VALUES (?,?,?)", (digest, "CANDIDATE_RECEIVED", now))
                    else:
                        counts["duplicate"] += 1
                except (ValueError, TypeError, KeyError) as exc:
                    counts["rejected"] += 1
                    counts["errors"].append({"index": index, "reason": str(exc)})
        return counts
    finally:
        db.close()

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--provider", required=True, choices=sorted(PROVIDERS))
    p.add_argument("--input", type=Path, required=True)
    p.add_argument("--db", type=Path, required=True)
    a = p.parse_args()
    if a.input.resolve() == a.db.resolve():
        p.error("input and database must differ")
    records = [json.loads(line) for line in a.input.read_text(encoding="utf-8").splitlines() if line.strip()]
    print(json.dumps(ingest(a.provider, records, a.db), indent=2))

if __name__ == "__main__":
    main()
