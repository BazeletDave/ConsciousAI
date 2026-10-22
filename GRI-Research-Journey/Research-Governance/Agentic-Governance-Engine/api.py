"""Local simulation API. Bind to loopback; no real money or external systems."""
import os
from dataclasses import asdict
from fastapi import FastAPI, Header, HTTPException
from pydantic import BaseModel, Field
from engine import GovernanceEngine, Capability, Action, sign_capability
import time, uuid

app=FastAPI(title="GRI Agentic Governance Research API",version="2.0.0")
key=os.environ.get("GRI_SIM_SIGNING_KEY","local-research-only-not-production").encode()
engine=GovernanceEngine(key)

class ActionRequest(BaseModel):
    action_id: str = Field(min_length=1,max_length=128)
    agent_id: str = Field(min_length=1,max_length=128)
    asset_pair: str = Field(min_length=1,max_length=32)
    amount: str
    capability: dict

@app.get("/health")
def health():
    return {"service":"research-simulation","mode":"no-external-execution"}

@app.get("/state")
def state():
    return engine.snapshot()

@app.post("/simulate")
def simulate(req:ActionRequest):
    try:
        cap=Capability(**req.capability)
        return engine.evaluate(Action(req.action_id,req.agent_id,req.asset_pair,req.amount),cap)
    except (ValueError,TypeError) as exc:
        raise HTTPException(422,str(exc))

@app.get("/demo-capability")
def demo_capability():
    """Local-only convenience; never expose capability issuance like this in production."""
    now=time.time()
    claims={"token_id":str(uuid.uuid4()),"agent_id":"Agent-88","asset_pair":"EUR/USD",
        "max_single":"50000","max_hourly":"200000","not_before":now-1,"expires_at":now+3600}
    return {**claims,"signature":sign_capability(claims,key)}

@app.post("/reset")
def reset(x_operator_approval: str|None=Header(default=None)):
    if x_operator_approval != "research-demo-acknowledged":
        raise HTTPException(403,"Explicit demo operator acknowledgment required")
    engine.reset(operator_approved=True)
    return {"status":"reset","mode":"research-simulation"}
