"""Offline backup and integrity verification for GRI staging SQLite evidence.

No network, no cloud uploads, no credential access, no production mutation.
"""
import argparse
import hashlib
import json
import os
import sqlite3
from datetime import datetime, timezone
from pathlib import Path

def digest(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()

def backup(source, destination):
    source, destination = Path(source), Path(destination)
    if not source.is_file() or source.resolve() == destination.resolve():
        raise ValueError("source must exist and differ from destination")
    if destination.exists():
        raise FileExistsError("refusing to overwrite backup")
    destination.parent.mkdir(parents=True, exist_ok=True)
    with sqlite3.connect(f"file:{source.resolve()}?mode=ro", uri=True) as src:
        with sqlite3.connect(destination) as dst:
            src.backup(dst)
    try:
        with sqlite3.connect(f"file:{destination.resolve()}?mode=ro", uri=True) as check:
            result = check.execute("PRAGMA integrity_check").fetchone()[0]
            if result != "ok":
                raise ValueError("backup integrity failed")
        manifest = {"schema_version":"1.0","created_at":datetime.now(timezone.utc).isoformat(),
                    "source_name":source.name,"backup_name":destination.name,
                    "sha256":digest(destination),"integrity_check":"ok",
                    "notice":"Local staging backup only; independent offsite retention and restore drill required."}
        manifest_path = destination.with_name(destination.name + ".manifest.json")
        if manifest_path.exists():
            raise FileExistsError("manifest already exists")
        manifest_path.write_text(json.dumps(manifest,indent=2)+"\n",encoding="utf-8")
        os.chmod(destination, 0o600)
        os.chmod(manifest_path, 0o600)
        return manifest
    except Exception:
        destination.unlink(missing_ok=True)
        raise

def verify(destination):
    destination = Path(destination)
    manifest = json.loads(destination.with_name(destination.name + ".manifest.json").read_text(encoding="utf-8"))
    if manifest["backup_name"] != destination.name or digest(destination) != manifest["sha256"]:
        raise ValueError("backup hash mismatch")
    with sqlite3.connect(f"file:{destination.resolve()}?mode=ro",uri=True) as db:
        if db.execute("PRAGMA integrity_check").fetchone()[0] != "ok":
            raise ValueError("database integrity check failed")
    return True

if __name__ == "__main__":
    parser=argparse.ArgumentParser()
    parser.add_argument("action",choices=["backup","verify"])
    parser.add_argument("--source",type=Path)
    parser.add_argument("--destination",type=Path,required=True)
    args=parser.parse_args()
    if args.action=="backup":
        if args.source is None: parser.error("--source required for backup")
        print(json.dumps(backup(args.source,args.destination),indent=2))
    else:
        print(json.dumps({"verified":verify(args.destination)}))
