"""Conservative GRI policy preflight for future autonomous workflows.

Not legal advice. All callers MUST invoke this before performing external actions.
No network calls, self-authorization, or persistence.
"""
from __future__ import annotations

AUTOMATIC = frozenset({"read_approved_public_source", "deduplicate", "internal_draft",
                       "calculate_internal_metrics", "internal_evidence_check"})
HUMAN = frozenset({"add_source", "publish", "train_model", "promote_model",
                   "modify_policy", "change_permissions", "send_external_alert",
                   "share_personal_data", "security_action"})
DENIED = frozenset({"bypass_access_controls", "intrusive_scan_without_authorization",
                    "collect_restricted_data", "impersonate_agency",
                    "autonomous_third_party_remediation", "self_authorize"})
def authorize(action, *, source_approved=False, human_approval=False,
              contains_personal_data=False, externally_visible=False):
    if not isinstance(action, str) or action not in AUTOMATIC | HUMAN | DENIED:
        return {"allowed": False, "decision": "deny_unknown_action"}
    if action in DENIED:
        return {"allowed": False, "decision": "deny_prohibited"}
    if action in HUMAN:
        # Approval must be verified out of band; caller-supplied booleans are NOT sufficient.
        return {"allowed": False, "decision": "requires_external_human_approval_workflow"}
    if contains_personal_data or externally_visible:
        return {"allowed": False, "decision": "requires_external_human_approval_workflow"}
    if action == "read_approved_public_source" and not source_approved:
        return {"allowed": False, "decision": "deny_source_not_approved"}
    return {"allowed": True, "decision": "bounded_internal_operation_only"}
