"""GRI Tiger Legacy Version One. Synthetic-only reference engine; not production security."""
import hashlib
import hmac
import json
from datetime import datetime, timezone

def canonical(obj):
    return json.dumps(obj, sort_keys=True, separators=(",", ":"), allow_nan=False).encode()

class TigerLegacy:
    def __init__(self, key):
        if not isinstance(key, bytes) or len(key) < 32:
            raise ValueError("synthetic test signing key must be at least 32 bytes")
        self._key = key
        self.resources = {}
        self.grants = {}
        self.events = []
        self.head = "0" * 64
        self.seen_ids = set()

    def _event(self, event_id, tenant, kind, details):
        if not event_id or event_id in self.seen_ids:
            raise ValueError("duplicate or missing event identifier")
        entry = {"sequence": len(self.events), "id": event_id, "tenant": tenant,
                 "kind": kind, "details": details, "previous": self.head}
        digest = hashlib.sha256(canonical(entry)).hexdigest()
        signature = hmac.new(self._key, digest.encode(), hashlib.sha256).hexdigest()
        entry.update(hash=digest, signature=signature)
        self.events.append(entry)
        self.seen_ids.add(event_id)
        self.head = digest
        return digest

    def add_resource(self, event_id, tenant, resource, owner, content):
        if not all(isinstance(x, str) and x for x in (tenant, resource, owner, content)):
            raise ValueError("invalid resource")
        key = (tenant, resource)
        if key in self.resources:
            raise ValueError("duplicate resource")
        self._event(event_id, tenant, "resource", {"resource": resource, "owner": owner,
                    "content_sha256": hashlib.sha256(content.encode()).hexdigest()})
        self.resources[key] = {"owner": owner, "content": content}

    def grant(self, event_id, tenant, resource, grantor, subject, purpose, expires):
        item = self.resources.get((tenant, resource))
        if item is None or item["owner"] != grantor:
            raise PermissionError("owner authorization required")
        if not subject or not purpose or not isinstance(expires, int):
            raise ValueError("invalid grant")
        key = (tenant, resource, subject, purpose)
        self._event(event_id, tenant, "grant", {"resource": resource, "subject": subject,
                    "purpose": purpose, "expires": expires})
        self.grants[key] = {"expires": expires, "revoked": False}

    def revoke(self, event_id, tenant, resource, grantor, subject, purpose):
        item = self.resources.get((tenant, resource))
        key = (tenant, resource, subject, purpose)
        if item is None or item["owner"] != grantor or key not in self.grants:
            raise PermissionError("owner and existing grant required")
        self._event(event_id, tenant, "revoke", {"resource": resource, "subject": subject, "purpose": purpose})
        self.grants[key]["revoked"] = True

    def authorize(self, tenant, resource, principal, purpose, now):
        if not all(isinstance(x, str) and x for x in (tenant, resource, principal, purpose)):
            return False
        if not isinstance(now, int):
            return False
        item = self.resources.get((tenant, resource))
        if item is None:
            return False
        if principal == item["owner"]:
            return True
        grant = self.grants.get((tenant, resource, principal, purpose))
        return bool(grant and not grant["revoked"] and now < grant["expires"])

    def read(self, tenant, resource, principal, purpose, now):
        if not self.authorize(tenant, resource, principal, purpose, now):
            raise PermissionError("access denied")
        return self.resources[(tenant, resource)]["content"]

    def verify(self):
        previous = "0" * 64
        ids = set()
        for index, entry in enumerate(self.events):
            data = {k: v for k, v in entry.items() if k not in ("hash", "signature")}
            if data["sequence"] != index or data["previous"] != previous or data["id"] in ids:
                return False
            digest = hashlib.sha256(canonical(data)).hexdigest()
            signature = hmac.new(self._key, digest.encode(), hashlib.sha256).hexdigest()
            if not hmac.compare_digest(digest, entry["hash"]) or not hmac.compare_digest(signature, entry["signature"]):
                return False
            previous = digest
            ids.add(data["id"])
        return previous == self.head and ids == self.seen_ids

    def summary(self):
        return {"synthetic_only": True, "tenant_count": len({t for t, _ in self.resources}),
                "resource_count": len(self.resources), "event_count": len(self.events),
                "evidence_verified": self.verify(), "production_security": "unmeasured"}
