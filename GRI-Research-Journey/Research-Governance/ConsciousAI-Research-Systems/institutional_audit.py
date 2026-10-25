"""Isolated GRI cryptographic audit research prototype. Not a production certification.
Restricted deterministic JSON encoding; not RFC 8785. No floats in signed evidence.
Requires cryptography; intentionally not imported by the live web service.
"""
import datetime as dt
import hashlib
import json
import os
import sqlite3
import tempfile
import unittest
from pathlib import Path
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.exceptions import InvalidSignature

GENESIS = "0" * 64

def canonical(obj):
    def check(v):
        if isinstance(v, float): raise ValueError("floats prohibited")
        if isinstance(v, dict):
            if not all(isinstance(k,str) for k in v): raise ValueError("non-string key")
            for x in v.values(): check(x)
        elif isinstance(v,list):
            for x in v: check(x)
        elif v is not None and not isinstance(v,(str,int,bool)):
            raise ValueError("unsupported value")
    check(obj)
    return json.dumps(obj,sort_keys=True,separators=(",",":"),ensure_ascii=False,allow_nan=False).encode()

class Signer:
    def __init__(self,key_id,private_key):
        self.key_id,self.private_key=key_id,private_key
    @classmethod
    def test_signer(cls):
        return cls("TEST-KEY",rsa.generate_private_key(public_exponent=65537,key_size=2048))
    def sign(self,raw):
        return self.private_key.sign(raw,padding.PSS(mgf=padding.MGF1(hashes.SHA256()),salt_length=padding.PSS.MAX_LENGTH),hashes.SHA256()).hex()

class Ledger:
    def __init__(self,path):
        self.path=str(path)
        with sqlite3.connect(self.path) as db:
            db.execute("PRAGMA journal_mode=WAL")
            db.execute("CREATE TABLE IF NOT EXISTS audit_ledger (block_index INTEGER PRIMARY KEY,timestamp_utc TEXT NOT NULL,key_id TEXT NOT NULL,canonical_payload BLOB NOT NULL,signature TEXT NOT NULL,previous_hash TEXT NOT NULL,current_hash TEXT NOT NULL)")
            db.execute("CREATE TRIGGER IF NOT EXISTS no_update BEFORE UPDATE ON audit_ledger BEGIN SELECT RAISE(FAIL,'audit updates forbidden'); END")
            db.execute("CREATE TRIGGER IF NOT EXISTS no_delete BEFORE DELETE ON audit_ledger BEGIN SELECT RAISE(FAIL,'audit deletes forbidden'); END")
    def append(self,signer,payload):
        with sqlite3.connect(self.path,timeout=30) as db:
            db.execute("BEGIN IMMEDIATE")
            row=db.execute("SELECT block_index,current_hash FROM audit_ledger ORDER BY block_index DESC LIMIT 1").fetchone()
            index,previous=(row[0]+1,row[1]) if row else (1,GENESIS)
            stamp=dt.datetime.now(dt.timezone.utc).isoformat()
            raw=canonical({"block_index":index,"previous_hash":previous,"key_id":signer.key_id,"timestamp_utc":stamp,"payload":payload,"schema_version":"gri-audit-v1"})
            sig=signer.sign(raw)
            digest=hashlib.sha256(raw+bytes.fromhex(sig)).hexdigest()
            db.execute("INSERT INTO audit_ledger VALUES (?,?,?,?,?,?,?)",(index,stamp,signer.key_id,raw,sig,previous,digest))
            return index,digest

def verify(path,trusted_keys,checkpoint=None):
    if not os.path.isfile(path): return False,"database missing"
    try:
        with sqlite3.connect("file:"+str(Path(path).resolve())+"?mode=ro",uri=True) as db:
            rows=db.execute("SELECT block_index,timestamp_utc,key_id,canonical_payload,signature,previous_hash,current_hash FROM audit_ledger ORDER BY block_index").fetchall()
    except sqlite3.Error as e: return False,str(e)
    if not rows: return False,"empty ledger"
    previous=GENESIS
    for expected,(index,stamp,kid,raw,sig,ph,ch) in enumerate(rows,1):
        if index!=expected or ph!=previous: return False,"chain continuity failure"
        try:
            envelope=json.loads(raw)
            if canonical(envelope)!=raw: return False,"noncanonical payload"
            if set(envelope)!={"block_index","previous_hash","key_id","timestamp_utc","payload","schema_version"}: return False,"invalid envelope schema"
            if envelope["schema_version"]!="gri-audit-v1" or (envelope["block_index"],envelope["previous_hash"],envelope["key_id"],envelope["timestamp_utc"])!=(index,ph,kid,stamp): return False,"envelope mismatch"
            if hashlib.sha256(raw+bytes.fromhex(sig)).hexdigest()!=ch: return False,"hash mismatch"
            key=trusted_keys.get(kid)
            if key is None: return False,"untrusted key"
            key.verify(bytes.fromhex(sig),raw,padding.PSS(mgf=padding.MGF1(hashes.SHA256()),salt_length=padding.PSS.MAX_LENGTH),hashes.SHA256())
        except (ValueError,TypeError,KeyError,UnicodeDecodeError,InvalidSignature): return False,"invalid signature or envelope"
        previous=ch
    if checkpoint is not None and checkpoint!=(len(rows),previous): return False,"checkpoint mismatch"
    return True,"verified "+str(len(rows))+" blocks"

class AuditTests(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory();self.addCleanup(self.temp.cleanup)
        self.path=os.path.join(self.temp.name,"audit.db")
        self.signer=Signer.test_signer()
        self.ledger=Ledger(self.path)
        self.keys={self.signer.key_id:self.signer.private_key.public_key()}
    def test_valid_and_reopen(self):
        self.ledger.append(self.signer,{"event":"synthetic"})
        Ledger(self.path).append(self.signer,{"event":"synthetic_2"})
        self.assertTrue(verify(self.path,self.keys)[0])
    def test_update_delete_protected(self):
        self.ledger.append(self.signer,{"event":"synthetic"})
        with sqlite3.connect(self.path) as db:
            with self.assertRaises(sqlite3.IntegrityError): db.execute("UPDATE audit_ledger SET key_id='X' WHERE block_index=1")
            with self.assertRaises(sqlite3.IntegrityError): db.execute("DELETE FROM audit_ledger WHERE block_index=1")
    def test_privileged_tamper_detected(self):
        self.ledger.append(self.signer,{"event":"synthetic"})
        with sqlite3.connect(self.path) as db:
            db.execute("DROP TRIGGER no_update")
            db.execute("UPDATE audit_ledger SET canonical_payload=? WHERE block_index=1",(canonical({"event":"altered"}),))
        self.assertFalse(verify(self.path,self.keys)[0])
    def test_truncation_checkpoint(self):
        self.ledger.append(self.signer,{"event":"synthetic"})
        _,tip=self.ledger.append(self.signer,{"event":"synthetic_2"})
        with sqlite3.connect(self.path) as db:
            db.execute("DROP TRIGGER no_delete")
            db.execute("DELETE FROM audit_ledger WHERE block_index=2")
        self.assertTrue(verify(self.path,self.keys)[0])
        self.assertFalse(verify(self.path,self.keys,(2,tip))[0])
    def test_untrusted_key_and_float_rejected(self):
        self.ledger.append(self.signer,{"event":"synthetic"})
        self.assertFalse(verify(self.path,{"TEST-KEY":Signer.test_signer().private_key.public_key()})[0])
        with self.assertRaises(ValueError): self.ledger.append(self.signer,{"accuracy":0.95})

if __name__=="__main__":
    unittest.main()
