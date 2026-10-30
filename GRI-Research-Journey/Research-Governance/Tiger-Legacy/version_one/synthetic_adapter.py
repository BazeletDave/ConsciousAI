"""Generic synthetic adapter boundary. Never treats caller metadata as trusted identity."""
from synthetic_identity import authorized_read

class SyntheticAdapter:
    def __init__(self, lab, identity, allowed_purposes):
        if not isinstance(allowed_purposes, (tuple, frozenset, list, set)) or not allowed_purposes:
            raise ValueError("purposes required")
        if any(not isinstance(p, str) or not p for p in allowed_purposes):
            raise ValueError("invalid purpose")
        self._lab = lab
        self._identity = identity
        self._purposes = frozenset(allowed_purposes)

    def read(self, token, resource, purpose, now):
        if not isinstance(resource, str) or not resource:
            raise PermissionError("invalid resource")
        if purpose not in self._purposes:
            raise PermissionError("purpose not enabled")
        return authorized_read(self._lab, self._identity, token, resource, purpose, now)
