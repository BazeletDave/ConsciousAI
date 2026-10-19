"""GRI schema conformance smoke test. Requires jsonschema (pip install jsonschema)."""
import json
from pathlib import Path
from jsonschema import Draft202012Validator, FormatChecker

base = Path(__file__).resolve().parent
schema = json.loads((base / "GRI-Evidence-Ledger-Schema-v0.1.json").read_text())
Draft202012Validator.check_schema(schema)
validator = Draft202012Validator(schema, format_checker=FormatChecker())
good = json.loads((base / "example-evidence-valid.json").read_text())
bad = json.loads((base / "example-evidence-invalid.json").read_text())
assert not list(validator.iter_errors(good)), "Expected valid synthetic record"
assert list(validator.iter_errors(bad)), "Expected invalid synthetic record"
print("PASS: schema loads; valid synthetic record accepted; invalid record rejected")
