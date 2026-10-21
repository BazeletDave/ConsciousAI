#!/usr/bin/env python3
"""PHP ledger validation: structural, semantic and optional external checks.

Never asserts independent audit certification. All external checks fail closed.
"""
import argparse
import json
import re
import subprocess
from pathlib import Path
from urllib.parse import urlparse
from php_evidence_verifier import validate_ledger

try:
    from jsonschema import Draft202012Validator, FormatChecker
except ImportError:
    Draft202012Validator = FormatChecker = None

SHA=re.compile(r"^[0-9a-f]{40}$")
DIGEST=re.compile(r"^sha256:[0-9a-f]{64}$")
REPO="https://github.com/php/php-src.git"

def schema_errors(data, schema):
    if Draft202012Validator is None:
        return ["Missing required dependency: jsonschema"]
    Draft202012Validator.check_schema(schema)
    return [f"{list(e.absolute_path)}: {e.message}"
            for e in Draft202012Validator(schema,format_checker=FormatChecker()).iter_errors(data)]

def verify_upstream_commit(commit, repo_dir):
    """Only a full local upstream clone with fetched object can establish existence.
    A commit's existence alone does not establish that it fixes a CVE.
    """
    if not isinstance(commit,str) or not SHA.fullmatch(commit):
        return False,"Invalid commit SHA"
    if repo_dir is None:
        return False,"No independently provisioned upstream checkout"
    try:
        def run(args):
            return subprocess.run(args,capture_output=True,text=True,timeout=15,check=False)
        origin=run(["git","-C",str(repo_dir),"remote","get-url","origin"])
        if origin.returncode or origin.stdout.strip() not in (REPO,"git@github.com:php/php-src.git"):
            return False,"Checkout origin is not canonical php-src"
        obj=run(["git","-C",str(repo_dir),"cat-file","-t",commit])
        if obj.returncode or obj.stdout.strip()!="commit":
            return False,"Commit object unavailable or not a commit"
        return True,"Commit object present in supplied php-src checkout; CVE association unverified"
    except (OSError,subprocess.TimeoutExpired) as exc:
        return False,f"Git verification unavailable: {type(exc).__name__}"

def verify_cosign(image_ref,digest,key_path):
    """Verify an exact digest-bound image using an explicitly provided trust key."""
    if not isinstance(digest,str) or not DIGEST.fullmatch(digest):
        return False,"Invalid image digest"
    if not isinstance(image_ref,str) or not image_ref or "@" in image_ref:
        return False,"Expected registry image reference without digest"
    if key_path is None:
        return False,"No trusted Cosign public key supplied"
    if not Path(key_path).is_file():
        return False,"Cosign public key not found"
    try:
        result=subprocess.run(["cosign","verify","--key",str(key_path),f"{image_ref}@{digest}"],
                              capture_output=True,text=True,timeout=30,check=False)
        if result.returncode!=0:
            return False,"Cosign returned nonzero status"
        return True,"Cosign signature verified for supplied key and digest; deployment not attested"
    except (OSError,subprocess.TimeoutExpired) as exc:
        return False,f"Cosign verification unavailable: {type(exc).__name__}"

def verify(data,schema,repo_dir=None,cosign_key=None,external=False):
    errors=schema_errors(data,schema)
    if errors: return errors
    errors=validate_ledger(data)
    if external:
        for asset in data["assets"]:
            aid=asset["asset_id"]
            ok,msg=verify_upstream_commit(asset["source_verification"]["upstream_commit_hash"],repo_dir)
            if not ok: errors.append(f"{aid}: upstream: {msg}")
            image=asset["image_integrity"]
            ok,msg=verify_cosign(image["registry_uri"],image["image_digest_sha256"],cosign_key)
            if not ok: errors.append(f"{aid}: image: {msg}")
    return errors

def main():
    p=argparse.ArgumentParser()
    p.add_argument("ledger",type=Path)
    p.add_argument("--schema",type=Path,default=Path(__file__).with_name("php_evidence_ledger.schema.json"))
    p.add_argument("--external",action="store_true",help="Require local Git and Cosign verification")
    p.add_argument("--php-src-checkout",type=Path)
    p.add_argument("--cosign-key",type=Path)
    a=p.parse_args()
    data=json.loads(a.ledger.read_text(encoding="utf-8"))
    schema=json.loads(a.schema.read_text(encoding="utf-8"))
    errors=verify(data,schema,a.php_src_checkout,a.cosign_key,a.external)
    print(json.dumps({"status":"FAIL" if errors else "CONSISTENCY_CHECKS_PASS_NOT_CERTIFIED","errors":errors},indent=2))
    raise SystemExit(bool(errors))

if __name__=="__main__":
    main()
