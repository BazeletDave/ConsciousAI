"""GRI governance PostgreSQL API: research simulation only. No external execution.
Apply migrations/001_initial_gri_governance_schema.sql to an empty test database.
Signed capability format: JSON object with claims {agent_id, asset_pair,
max_single_amount, max_hourly_volume, valid_from, valid_until, nonce}.
The Ed25519 issuer signs RFC8785 canonical bytes of claims. capability_digest
is SHA256 of those exact canonical bytes. Issuer key must be pre-registered.
"""
from __future__ import annotations

from datetime import datetime, timezone, timedelta
from decimal import Decimal, InvalidOperation
from hashlib import sha256
import json
import os
from typing import Any

import rfc8785
from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PublicKey
from fastapi import Depends, FastAPI, Header, HTTPException
from pydantic import BaseModel, Field
from sqlalchemy import create_engine, text
from sqlalchemy.orm import Session, sessionmaker

POLICY_VERSION = "v2.1.0-research"
ZERO = "0" * 64
DATABASE_URL = os.environ.get("DATABASE_URL")
if not DATABASE_URL:
    raise RuntimeError("DATABASE_URL must be configured explicitly")
engine = create_engine(DATABASE_URL, pool_pre_ping=True)
SessionLocal = sessionmaker(bind=engine, expire_on_commit=False)
app = FastAPI(title="GRI Governance Research Simulation", version=POLICY_VERSION)

def canonical(value: Any) -> bytes:
    return rfc8785.dumps(value)

def digest(value: Any) -> str:
    return sha256(canonical(value)).hexdigest()

def parse_amount(value: str) -> Decimal:
    try:
        d = Decimal(value)
    except (InvalidOperation, ValueError, TypeError):
        raise ValueError("Invalid amount")
    if not d.is_finite() or d <= 0 or d.as_tuple().exponent < -4 or d >= Decimal("100000000000000"):
        raise ValueError("Amount must be positive, finite and have at most four decimal places")
    return d

def utc(value: str) -> datetime:
    d = datetime.fromisoformat(value.replace("Z", "+00:00"))
    if d.tzinfo is None:
        raise ValueError("Timezone required")
    return d.astimezone(timezone.utc)

class GovernanceRequest(BaseModel):
    action_id: str = Field(min_length=1, max_length=128)
    agent_id: str = Field(min_length=1, max_length=128)
    asset_pair: str = Field(min_length=1, max_length=64)
    amount: str

class GovernanceResponse(BaseModel):
    action_id: str
    decision_status: str
    rejection_reason: str | None
    sequence_index: int
    record_hash: str
    policy_version: str = POLICY_VERSION

def get_db():
    with SessionLocal() as db:
        yield db

def authorize(db: Session, capability: dict, issuer_key_id: str, signature_hex: str, req: GovernanceRequest, now: datetime):
    claims = capability
    required = {"agent_id","asset_pair","max_single_amount","max_hourly_volume","valid_from","valid_until","nonce"}
    if not isinstance(claims, dict) or set(claims) != required or any(not isinstance(claims[k], str) for k in required):
        raise HTTPException(401, "Invalid capability claims")
    issuer = db.execute(text("SELECT * FROM governance_issuer_keys WHERE key_id=:k"), {"k":issuer_key_id}).mappings().first()
    if issuer is None or issuer["revoked"] or not issuer["valid_from"] <= now < issuer["valid_until"]:
        raise HTTPException(401, "Untrusted or inactive issuer")
    encoded = canonical(claims)
    try:
        Ed25519PublicKey.from_public_bytes(bytes.fromhex(issuer["public_key_hex"])).verify(bytes.fromhex(signature_hex), encoded)
    except (ValueError, InvalidSignature):
        raise HTTPException(401, "Invalid capability signature")
    cap_digest = sha256(encoded).hexdigest()
    registered = db.execute(text("""SELECT * FROM agent_capabilities
        WHERE capability_digest=:digest AND issuer_key_id=:issuer AND agent_id=:agent"""),
        {"digest":cap_digest,"issuer":issuer_key_id,"agent":req.agent_id}).mappings().first()
    if registered is None or registered["revoked"]:
        raise HTTPException(403, "Capability not registered or revoked")
    if claims["agent_id"] != req.agent_id or claims["asset_pair"] != registered["allowed_asset_pair"]:
        raise HTTPException(403, "Capability identity or scope mismatch")
    try:
        if not (utc(claims["valid_from"]) <= now < utc(claims["valid_until"])):
            raise HTTPException(403, "Capability expired or not yet active")
        if not (registered["valid_from"] <= now < registered["valid_until"]):
            raise HTTPException(403, "Registered capability inactive")
        if parse_amount(claims["max_single_amount"]) != registered["max_single_amount"] or parse_amount(claims["max_hourly_volume"]) != registered["max_hourly_volume"]:
            raise HTTPException(403, "Capability limits mismatch")
    except ValueError:
        raise HTTPException(401, "Invalid capability validity or limits")
    return registered, cap_digest

@app.post("/api/v1/governance/evaluate", response_model=GovernanceResponse)
def evaluate(
    request: GovernanceRequest,
    x_idempotency_key: str = Header(min_length=1, max_length=255, alias="X-Idempotency-Key"),
    x_issuer_key_id: str = Header(alias="X-Issuer-Key-ID"),
    x_capability_signature: str = Header(alias="X-Capability-Signature"),
    x_capability_claims: str = Header(alias="X-Capability-Claims"),
    db: Session = Depends(get_db),
):
    try:
        claims = json.loads(x_capability_claims)
    except (ValueError, TypeError):
        raise HTTPException(401, "Malformed capability claims")
    try:
        amount = parse_amount(request.amount)
    except ValueError as e:
        raise HTTPException(422, str(e))
    # RFC8785 normalizes request data. Amount is a decimal string, not float.
    request_hash = digest(request.model_dump())
    try:
        with db.begin():
            # One existing global lock serializes all authorization decisions,
            # idempotency checks, rolling-volume reservations and chain appends.
            head = db.execute(text("SELECT * FROM evidence_chain_heads WHERE chain_id='primary' FOR UPDATE")).mappings().one()
            now = datetime.now(timezone.utc)
            cap, cap_digest = authorize(db, claims, x_issuer_key_id, x_capability_signature, request, now)
            existing = db.execute(text("""SELECT * FROM idempotency_records
                WHERE agent_id=:agent AND idempotency_key=:key"""),
                {"agent":request.agent_id,"key":x_idempotency_key}).mappings().first()
            if existing:
                if existing["request_hash"] != request_hash:
                    raise HTTPException(409, "Idempotency key reused with different request")
                return GovernanceResponse(**existing["response_payload"])
            breaker = db.execute(text("SELECT is_open, tripped_reason FROM circuit_breaker_states WHERE system_id='primary'")).mappings().one()
            reason = None
            if breaker["is_open"]:
                reason = "Circuit breaker open"
            elif request.asset_pair != cap["allowed_asset_pair"]:
                reason = "Asset pair not authorized"
            elif amount > cap["max_single_amount"]:
                reason = "Single action limit exceeded"
            else:
                # This global lock also serializes other agents; intentionally
                # conservative for the research prototype.
                rolling = db.execute(text("""SELECT COALESCE(SUM(amount),0) FROM authorization_reservations
                    WHERE agent_id=:agent AND created_at > :start"""),
                    {"agent":request.agent_id,"start":now-timedelta(hours=1)}).scalar_one()
                if rolling + amount > cap["max_hourly_volume"]:
                    reason = "Rolling 60-minute limit exceeded"
            approved = reason is None
            if approved:
                db.execute(text("""INSERT INTO authorization_reservations
                    (action_id,agent_id,capability_id,amount,created_at)
                    VALUES (:action,:agent,:cap,:amount,:now)"""),
                    {"action":request.action_id,"agent":request.agent_id,"cap":cap["id"],"amount":amount,"now":now})
            index = head["last_index"] + 1
            event = {
                "chain_id":"primary","sequence_index":index,
                "timestamp_utc":now.isoformat(),
                "action_id":request.action_id,"agent_id":request.agent_id,
                "capability_digest":cap_digest,"policy_version":POLICY_VERSION,
                "input_payload_hash":request_hash,
                "decision_status":"AUTHORIZED_SIMULATION" if approved else "REJECTED",
                "rejection_reason":reason,
                "amount":format(amount, ".4f"),"previous_record_hash":head["last_hash"]
            }
            record_hash = digest(event)
            db.execute(text("""INSERT INTO evidence_records
                (chain_id,sequence_index,timestamp_utc,action_id,agent_id,capability_digest,
                policy_version,input_payload_hash,decision_status,rejection_reason,
                amount,previous_record_hash,record_hash)
                VALUES ('primary',:index,:now,:action,:agent,:cap,:policy,:input,:decision,
                :reason,:amount,:prev,:hash)"""),{
                "index":index,"now":now,"action":request.action_id,"agent":request.agent_id,
                "cap":cap_digest,"policy":POLICY_VERSION,"input":request_hash,
                "decision":event["decision_status"],"reason":reason,"amount":amount,
                "prev":head["last_hash"],"hash":record_hash
            })
            db.execute(text("""UPDATE evidence_chain_heads SET last_index=:index,last_hash=:hash
                WHERE chain_id='primary'"""),{"index":index,"hash":record_hash})
            response = GovernanceResponse(action_id=request.action_id,
                decision_status=event["decision_status"],rejection_reason=reason,
                sequence_index=index,record_hash=record_hash)
            db.execute(text("""INSERT INTO idempotency_records
                (agent_id,idempotency_key,request_hash,response_payload)
                VALUES (:agent,:key,:hash,CAST(:payload AS jsonb))"""),{
                "agent":request.agent_id,"key":x_idempotency_key,
                "hash":request_hash,"payload":response.model_dump_json()
            })
        return response
    except HTTPException:
        raise
    # SQLAlchemy context manager rolls back on all errors. Never return approval
    # on a failed transaction. Unexpected errors propagate for operator review.
