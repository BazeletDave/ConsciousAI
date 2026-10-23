# Reproducible instruments | GRI Uber institutional research

**Version 1.0 | 23 October 2026 | Research only**

[Full journal manuscript](../2026-10-23-uber-global-agentic-management-journal-manuscript.md)

## Data collection and quality control
The following are **blank instruments**, not a dataset or evidence of completed experiments.

### Ridehail offer panel schema (CSV header)
```csv
observation_id,platform,market,offer_timestamp_utc,accepted,expected_pickup_miles,expected_occupied_miles,expected_minutes,actual_online_minutes,actual_engaged_minutes,gross_payout_usd,tip_usd,bonus_usd,operating_cost_usd,contract_version,source_hash,verification_status
```
Do not enter invented values. Keep passenger, driver and trip identifiers out of public data.

### Enterprise task evaluation schema (CSV header)
```csv
task_id,team_code,risk_tier,assignment_method,ai_access,baseline_difficulty,model_version,policy_version,tool_scope,employee_minutes,reviewer_minutes,quality_score,error_count,incident_severity,total_cost_usd,completed,appealed,reversed,source_hash
```

### Decision rights coding schema (CSV header)
```csv
episode_id,case_id,rule_source,propose_formal,propose_effective,approve_formal,approve_effective,execute_formal,execute_effective,observe_formal,observe_effective,veto_formal,veto_effective,reverse_formal,reverse_effective,contest_formal,contest_effective,coder_id,adjudication_status
```
Values: 0 absent; 1 formally documented; 2 demonstrated in practice; NA unknown. Formal and effective values are distinct dimensions. This scale is proposed, not validated.

## Testable arithmetic example
For the published Chicago screenshot transcription only, passenger charges 32.27 and 40.81; estimated Lyft fees 1.99 and 21.03. The estimated fee shares are approximately 6.17% and 51.53%, respectively. They are **not** final realized margins.

## Quality gates
1. Reject duplicate observation IDs.
2. Reject negative miles, durations and monetary amounts unless a signed adjustment field is explicitly specified.
3. Preserve unknown values as null, never zero by default.
4. Check UTC timestamps and chronological consistency.
5. Keep displayed offer rates separate from realized net earnings.
6. Require source URI or privacy cleared source hash for every observation.
7. Report missingness and exclusions by variable and cohort.
8. For agent actions, deny execution without explicit authorization, policy version and human approval where required.
9. Do not compute a causal treatment effect without an identified assignment mechanism and documented assumptions.
10. Publish versioned code, data dictionary, results and uncertainty only after ethics and source rights review.

## Python standard library validation example
```python
import csv
from decimal import Decimal, InvalidOperation

REQUIRED = ("observation_id", "platform", "accepted", "verification_status")
NUMERIC = ("expected_pickup_miles", "expected_occupied_miles", "expected_minutes",
           "actual_online_minutes", "actual_engaged_minutes", "gross_payout_usd",
           "tip_usd", "bonus_usd", "operating_cost_usd")

def validate(path):
    errors, seen = [], set()
    with open(path, newline="", encoding="utf-8") as handle:
        for rowno, row in enumerate(csv.DictReader(handle), start=2):
            for field in REQUIRED:
                if not row.get(field):
                    errors.append((rowno, field, "missing"))
            key = row.get("observation_id")
            if key in seen:
                errors.append((rowno, "observation_id", "duplicate"))
            if key:
                seen.add(key)
            if row.get("accepted") not in ("true", "false", "TRUE", "FALSE", "1", "0"):
                errors.append((rowno, "accepted", "invalid boolean"))
            for field in NUMERIC:
                value = row.get(field)
                if value in ("", None):
                    continue
                try:
                    number = Decimal(value)
                    if not number.is_finite() or number < 0:
                        errors.append((rowno, field, "invalid nonnegative number"))
                except InvalidOperation:
                    errors.append((rowno, field, "invalid decimal"))
    return errors

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        raise SystemExit("Usage: python validate.py panel.csv")
    issues = validate(sys.argv[1])
    for issue in issues:
        print(*issue, sep=": ")
    raise SystemExit(1 if issues else 0)
```

**Boundary:** This is a transparent illustrative validator, not a full audit engine or deployed production control. It does not validate provenance hashes, consent, causal identification or semantic consistency between fields.
