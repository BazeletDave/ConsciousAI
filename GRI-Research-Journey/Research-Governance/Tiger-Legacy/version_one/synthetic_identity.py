"""Offline synthetic identity boundary for Tiger Legacy. NOT a production IdP."""
import base64
import hashlib
import hmac
import json
import time
from tiger_legacy import canonical

def _b64(data):
    return base64.urlsafe_b64encode(data).rstrip(b"=").decode("ascii")

def _unb64(data):
    if not isinstance(data, str) or len(data) > 8192:
        raise ValueError("invalid token encoding")
    return base64.b64decode(data + "=" * (-len(data) % 4), altchars=b"-_", validate=True)

class SyntheticIdentity:
    """Test-only HMAC issuer and verifier. Keys must be held outside the repository."""
    def __init__(self, key, issuer="gri.synthetic.identity", audience="tiger-legacy-lab"):
        if not isinstance(key, bytes) or len(key) < 32:
            raise ValueError("minimum 32 byte synthetic signing key")
        self._key = key
        self.issuer = issuer
        self.audience = audience

    def issue(self, tenant, subject, issued_at, expires_at):
        if not all(isinstance(x, str) and x for x in (tenant, subject)):
            raise ValueError("invalid identity")
        if type(issued_at) is not int or type(expires_at) is not int or not issued_at < expires_at:
            raise ValueError("invalid lifetime")
        claims = {"iss": self.issuer, "aud": self.audience, "tenant": tenant,
                  "sub": subject, "iat": issued_at, "exp": expires_at}
        payload = _b64(canonical(claims))
        signature = _b64(hmac.new(self._key, payload.encode(), hashlib.sha256).digest())
        return payload + "." + signature

    def verify(self, token, now=None):
        if not isinstance(token, str) or token.count(".") != 1:
            return None
        try:
            payload, signature = token.split(".")
            if not hmac.compare_digest(
                hmac.new(self._key, payload.encode(), hashlib.sha256).digest(),
                _unb64(signature)):
                return None
            claims = json.loads(_unb64(payload))
            moment = int(time.time()) if now is None else now
            if type(moment) is not int or not isinstance(claims, dict):
                return None
            if set(claims) != {"iss", "aud", "tenant", "sub", "iat", "exp"}:
                return None
            if claims["iss"] != self.issuer or claims["aud"] != self.audience:
                return None
            if not all(isinstance(claims[k], str) and claims[k] for k in ("tenant", "sub")):
                return None
            if type(claims["iat"]) is not int or type(claims["exp"]) is not int:
                return None
            if not claims["iat"] <= moment < claims["exp"]:
                return None
            return {"tenant": claims["tenant"], "principal": claims["sub"]}
        except (ValueError, TypeError, UnicodeError, OverflowError):
            return None

def authorized_read(lab, identity, token, resource, purpose, now):
    """Fail closed. Never accept caller-supplied principal or tenant as authority."""
    principal = identity.verify(token, now=now)
    if principal is None:
        raise PermissionError("identity verification failed")
    return lab.read(principal["tenant"], resource, principal["principal"], purpose, now)
