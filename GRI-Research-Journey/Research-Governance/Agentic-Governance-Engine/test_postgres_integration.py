"""PostgreSQL integration and adversarial tests; requires isolated migrated database."""
import json
import os
import uuid
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timedelta, timezone
from decimal import Decimal
from hashlib import sha256

import pytest
import rfc8785
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey
from fastapi.testclient import TestClient
from sqlalchemy import text

from app.main import SessionLocal, app

def ts(dt):
    return dt.isoformat()

@pytest.fixture(autouse=True)
def clean_db():
    with SessionLocal.begin() as db:
        db.execute(text("""TRUNCATE TABLE evidence_checkpoints, idempotency_records,
          evidence_records, authorization_reservations, agent_capabilities,
          governance_issuer_keys, agent_locks RESTART IDENTITY CASCADE"""))
        db.execute(text("UPDATE evidence_chain_heads SET last_index=0,last_hash=repeat('0',64)"))
        db.execute(text("UPDATE circuit_breaker_states SET is_open=false,tripped_reason=NULL"))
    yield

@pytest.fixture
def credential():
    key = Ed25519PrivateKey.generate()
    now = datetime.now(timezone.utc)
    claims = {
        "agent_id":"agent-test","asset_pair":"EUR/USD",
        "max_single_amount":"30000.0000","max_hourly_volume":"200000.0000",
        "valid_from":ts(now-timedelta(minutes=5)),
        "valid_until":ts(now+timedelta(hours=2)),"nonce":str(uuid.uuid4())
    }
    encoded = rfc8785.dumps(claims)
    cap_hash = sha256(encoded).hexdigest()
    pub = key.public_key().public_bytes(encoding=serialization.Encoding.Raw,
                                        format=serialization.PublicFormat.Raw).hex()
    with SessionLocal.begin() as db:
        db.execute(text("""INSERT INTO governance_issuer_keys
          (key_id,public_key_hex,valid_from,valid_until)
          VALUES ('issuer-test',:pub,:start,:end)"""),
          {"pub":pub,"start":now-timedelta(hours=1),"end":now+timedelta(days=1)})
        db.execute(text("""INSERT INTO agent_capabilities
          (agent_id,issuer_key_id,capability_digest,allowed_asset_pair,
          max_single_amount,max_hourly_volume,valid_from,valid_until)
          VALUES ('agent-test','issuer-test',:digest,'EUR/USD',30000,200000,:start,:end)"""),
          {"digest":cap_hash,"start":now-timedelta(minutes=5),"end":now+timedelta(hours=2)})
    return claims,key

def send(claims,key,amount="30000.0000",pair="EUR/USD",idem=None,action=None):
    headers={
      "X-Issuer-Key-ID":"issuer-test",
      "X-Capability-Claims":json.dumps(claims,separators=(",",":")),
      "X-Capability-Signature":key.sign(rfc8785.dumps(claims)).hex(),
      "X-Idempotency-Key":idem or str(uuid.uuid4())
    }
    body={"action_id":action or str(uuid.uuid4()),"agent_id":"agent-test",
          "asset_pair":pair,"amount":amount}
    with TestClient(app) as client:
        return client.post("/api/v1/governance/evaluate",headers=headers,json=body)

def counts():
    with SessionLocal() as db:
        return (
          db.execute(text("SELECT COUNT(*) FROM authorization_reservations")).scalar_one(),
          db.execute(text("SELECT COUNT(*) FROM evidence_records")).scalar_one(),
          db.execute(text("SELECT COUNT(*) FROM idempotency_records")).scalar_one()
        )

def test_trusted_and_untrusted_signatures(credential):
    claims,key=credential
    assert send(claims,key).json()["decision_status"]=="AUTHORIZED_SIMULATION"
    attacker=Ed25519PrivateKey.generate()
    assert send(claims,attacker).status_code==401
    with SessionLocal.begin() as db:
        db.execute(text("UPDATE agent_capabilities SET revoked=true"))
    assert send(claims,key).status_code==403

def test_scope_single_limit_and_idempotency_conflict(credential):
    claims,key=credential
    assert send(claims,key,pair="BTC/USD").json()["decision_status"]=="REJECTED"
    assert send(claims,key,amount="30000.0001").json()["decision_status"]=="REJECTED"
    idem=str(uuid.uuid4()); action=str(uuid.uuid4())
    first=send(claims,key,idem=idem,action=action)
    assert first.status_code==200
    second=send(claims,key,idem=idem,action=action)
    assert second.json()==first.json()
    assert send(claims,key,idem=idem,action=str(uuid.uuid4())).status_code==409

def test_parallel_rolling_limit(credential):
    claims,key=credential
    with ThreadPoolExecutor(max_workers=10) as pool:
        results=list(pool.map(lambda _:send(claims,key),range(10)))
    assert all(r.status_code==200 for r in results), [r.text for r in results]
    approved=[r for r in results if r.json()["decision_status"]=="AUTHORIZED_SIMULATION"]
    assert len(approved)==6
    assert len(results)-len(approved)==4
    with SessionLocal() as db:
        total=db.execute(text("SELECT COALESCE(SUM(amount),0) FROM authorization_reservations")).scalar_one()
        assert total==Decimal("180000.0000")
        head=db.execute(text("SELECT last_index FROM evidence_chain_heads WHERE chain_id='primary'")).scalar_one()
        assert head==10
    assert counts()==(6,10,10)

def test_circuit_breaker_and_invalid_amount(credential):
    claims,key=credential
    with SessionLocal.begin() as db:
        db.execute(text("UPDATE circuit_breaker_states SET is_open=true,tripped_reason='test'"))
    assert send(claims,key).json()["decision_status"]=="REJECTED"
    assert send(claims,key,amount="NaN").status_code==422
    assert send(claims,key,amount="0.00001").status_code==422

def test_database_failure_rolls_back(credential):
    claims,key=credential
    # Trigger a real DB constraint failure after reservation and evidence writes
    # by making idempotency inserts fail, before transaction commit.
    with SessionLocal.begin() as db:
        db.execute(text("""ALTER TABLE idempotency_records
            ADD CONSTRAINT test_block_insert CHECK (false) NOT VALID"""))
    try:
        with pytest.raises(Exception):
            send(claims,key)
        assert counts()==(0,0,0)
        with SessionLocal() as db:
            assert db.execute(text("SELECT last_index FROM evidence_chain_heads")).scalar_one()==0
    finally:
        with SessionLocal.begin() as db:
            db.execute(text("ALTER TABLE idempotency_records DROP CONSTRAINT test_block_insert"))
