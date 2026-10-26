"""Encrypt/decrypt GRI restricted backup exports with AES-256-GCM.

Requires cryptography. Supply a 32-byte key as 64 hex characters through
GRI_BACKUP_KEY_HEX; store in a secret manager, never source control.
Ciphertext must be copied to an independently administered storage destination.
"""
import argparse
import hashlib
import json
import os
from pathlib import Path
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

MAGIC=b"GRIENC1"
MAX_BYTES=100_000_000

def key_from_env():
    raw=os.environ.get("GRI_BACKUP_KEY_HEX","")
    if len(raw)!=64:
        raise ValueError("missing 256-bit backup key")
    try: key=bytes.fromhex(raw)
    except ValueError: raise ValueError("invalid backup key") from None
    return key

def encrypt(source, destination, key):
    source,destination=Path(source),Path(destination)
    if source.resolve()==destination.resolve() or destination.exists():
        raise ValueError("destination must be new and distinct")
    if len(key)!=32: raise ValueError("AES-256 key required")
    if source.stat().st_size>MAX_BYTES: raise ValueError("backup exceeds staging limit")
    data=source.read_bytes()
    nonce=os.urandom(12)
    ciphertext=MAGIC+nonce+AESGCM(key).encrypt(nonce,data,MAGIC)
    with destination.open("xb") as f:
        os.chmod(destination,0o600)
        f.write(ciphertext)
    return {"encrypted_bytes":len(ciphertext),"sha256":hashlib.sha256(ciphertext).hexdigest()}

def decrypt(source,destination,key):
    source,destination=Path(source),Path(destination)
    if destination.exists() or source.resolve()==destination.resolve():
        raise ValueError("destination must be new and distinct")
    data=source.read_bytes()
    if not data.startswith(MAGIC) or len(data)>MAX_BYTES+128:
        raise ValueError("invalid encrypted backup")
    plain=AESGCM(key).decrypt(data[len(MAGIC):len(MAGIC)+12],data[len(MAGIC)+12:],MAGIC)
    with destination.open("xb") as f:
        os.chmod(destination,0o600)
        f.write(plain)
    return {"restored_bytes":len(plain),"sha256":hashlib.sha256(plain).hexdigest()}

if __name__=="__main__":
    p=argparse.ArgumentParser()
    p.add_argument("action",choices=["encrypt","decrypt"])
    p.add_argument("--source",required=True,type=Path)
    p.add_argument("--destination",required=True,type=Path)
    a=p.parse_args()
    print(json.dumps((encrypt if a.action=="encrypt" else decrypt)(a.source,a.destination,key_from_env()),indent=2))
