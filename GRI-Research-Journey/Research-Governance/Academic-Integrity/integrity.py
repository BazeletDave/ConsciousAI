"""Research-only academic integrity governance; telemetry alone never proves misconduct."""
from dataclasses import dataclass
from enum import Enum
from typing import Optional

class FlagLevel(str, Enum):
    NO_INTERVENTION = "NO_INTERVENTION"
    LOG_FOR_REVIEW = "LOG_FOR_REVIEW"
    INSUFFICIENT_EVIDENCE = "INSUFFICIENT_EVIDENCE"
    ISSUE_INTEGRITY_WARNING = "ISSUE_INTEGRITY_WARNING"
    FLAG_FOR_PROCTOR = "FLAG_FOR_PROCTOR"

class AIPolicy(str, Enum):
    PERMITTED = "PERMITTED"
    PERMITTED_WITH_DISCLOSURE = "PERMITTED_WITH_DISCLOSURE"
    RESTRICTED = "RESTRICTED"
    PROHIBITED = "PROHIBITED"
    UNSPECIFIED = "UNSPECIFIED"

@dataclass(frozen=True)
class ExamTelemetryEvent:
    session_active: bool
    window_focused: bool
    tab_switches_count: int
    pasted_external_content: bool
    clipboard_character_count: int
    event_confidence: float

@dataclass(frozen=True)
class AssessmentPolicy:
    assessment_id: str
    ai_policy: AIPolicy = AIPolicy.UNSPECIFIED
    paste_allowed: Optional[bool] = None
    external_resources_allowed: Optional[bool] = None
    policy_version: str = "research-1"
    student_notice_provided: bool = False

@dataclass(frozen=True)
class GovernanceDecision:
    level: FlagLevel
    rationale: str
    policy_version: str
    misconduct_determined: bool = False
    adverse_action_authorized: bool = False

def evaluate_academic_integrity(event: ExamTelemetryEvent,
                                policy: AssessmentPolicy) -> GovernanceDecision:
    """Evaluates telemetry as *ambiguous evidence* subject to explicit policy.

    No result determines cheating, assigns guilt or authorizes sanctions.
    """
    if event.tab_switches_count < 0 or event.clipboard_character_count < 0:
        raise ValueError("event counts cannot be negative")
    if not 0 <= event.event_confidence <= 1:
        raise ValueError("event confidence must be between 0 and 1")
    def result(level, rationale):
        return GovernanceDecision(level, rationale, policy.policy_version)
    if not event.session_active:
        return result(FlagLevel.NO_INTERVENTION, "Assessment session inactive")
    if not policy.student_notice_provided:
        return result(FlagLevel.INSUFFICIENT_EVIDENCE, "Monitoring notice not confirmed")
    if event.event_confidence < 0.85:
        return result(FlagLevel.INSUFFICIENT_EVIDENCE, "Telemetry quality below research threshold")
    activity = (event.pasted_external_content or event.tab_switches_count > 0
                or not event.window_focused)
    if not activity:
        return result(FlagLevel.NO_INTERVENTION, "No relevant telemetry event")
    if (policy.paste_allowed is None or policy.external_resources_allowed is None
            or policy.ai_policy == AIPolicy.UNSPECIFIED):
        return result(FlagLevel.INSUFFICIENT_EVIDENCE, "Assessment permissions are incomplete")
    if (event.pasted_external_content and not policy.paste_allowed):
        return result(FlagLevel.LOG_FOR_REVIEW,
                      "Observed paste conflicts with documented assessment rule; context unknown")
    if (event.tab_switches_count > 0 or not event.window_focused) and not policy.external_resources_allowed:
        return result(FlagLevel.LOG_FOR_REVIEW,
                      "Focus/visibility event under restricted-resource rule; cause unknown")
    return result(FlagLevel.NO_INTERVENTION, "Observed activity not prohibited by stated assessment rules")
