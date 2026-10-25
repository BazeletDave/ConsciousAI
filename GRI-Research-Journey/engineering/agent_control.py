"""Pure decision engine: no tools, network, credentials, or action execution."""
import hashlib
import json

def authorize(capability, request):
    if not isinstance(capability, dict) or not isinstance(request, dict):
        raise ValueError("capability and request must be objects")
    agent = request.get("agent_id")
    action = request.get("action")
    allowed = capability.get("allowed_actions")
    if not isinstance(agent, str) or not agent or not isinstance(action, str) or not action:
        raise ValueError("agent_id and action required")
    if not isinstance(allowed, list) or any(not isinstance(v, str) for v in allowed):
        raise ValueError("allowed_actions must be strings")
    matched = capability.get("agent_id") == agent and action in allowed
    approval = request.get("human_approval") is True
    restricted = action in {"deploy", "publish", "retrain", "change_policy", "modify_production"}
    decision = "ALLOW_RESEARCH_SIMULATION" if matched and (not restricted or approval) else "DENY"
    payload = {"agent_id": agent, "action": action, "decision": decision,
               "human_approval_present": approval, "restricted": restricted}
    return {**payload, "audit_digest": hashlib.sha256(json.dumps(payload, sort_keys=True).encode()).hexdigest(),
            "execution_performed": False, "notice": "Human approval boolean is a test fixture, not authenticated approval."}
