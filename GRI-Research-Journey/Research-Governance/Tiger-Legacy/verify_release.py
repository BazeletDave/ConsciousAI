"""Reproduce Tiger Legacy release evidence in a complete checked-out repository.

No client data, network calls, deployment or mutation. Requires Python >=3.11.
Run from anywhere: python GRI-Research-Journey/Research-Governance/Tiger-Legacy/verify_release.py
"""
import hashlib
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
GOV = ROOT / "GRI-Research-Journey" / "Research-Governance"
DASH = GOV / "ConsciousAI-Research-Systems"
LAB = GOV / "Tiger-Legacy" / "version_one"

def run_tests(folder, args):
    result = subprocess.run([sys.executable, "-m", "unittest", "discover", *args, "-v"],
                            cwd=folder, text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    print(result.stdout, flush=True)
    if result.returncode:
        raise RuntimeError("test failure: " + str(folder))
    return result.stdout

def main():
    if not DASH.is_dir() or not LAB.is_dir():
        raise RuntimeError("complete GRI repository checkout required")
    manifest = json.loads((DASH / "tiger_legacy_trust_manifest.json").read_text())
    raw = (DASH / "tiger_legacy_synthetic_snapshot.json").read_bytes()
    observed = hashlib.sha256(raw).hexdigest()
    if observed != manifest["snapshot_sha256"]:
        raise RuntimeError("snapshot digest differs from repository manifest")
    sys.path.insert(0, str(DASH))
    from tiger_legacy_bridge import snapshot
    summary = snapshot(DASH)
    assert summary["production_security"] == "unmeasured"
    assert summary["operational_actions_authorized"] == 0
    assert summary["model_promoted"] is False
    print("Pinned synthetic snapshot digest:", observed)
    print("Verification classification:", summary["integrity_status"])
    print("Executing full dashboard suite, including original Tiger Assurance HTTP regression")
    run_tests(DASH, ["-p", "test_*.py"])
    print("Executing full Tiger Legacy suite")
    run_tests(LAB, ["-s", "tests", "-p", "test_*.py"])
    print("PASS: complete repository-level Tiger Legacy release evidence reproduced")
    print("NOTE: This script does not verify GitHub attestation signatures; use GitHub CLI attestation verify.")

if __name__ == "__main__":
    main()
