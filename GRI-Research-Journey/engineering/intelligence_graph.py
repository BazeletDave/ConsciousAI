"""Typed, provenance-aware research graph. No autonomous inference promotion."""
import hashlib
import json

NODE_TYPES = {"institution", "policy", "ai_system", "research_case", "evidence", "actor"}
EDGE_TYPES = {"documents", "governs", "relates_to", "affects", "cites"}

class IntelligenceGraph:
    def __init__(self):
        self.nodes = {}
        self.edges = {}

    def add_node(self, node_id, kind, label):
        if not all(isinstance(v, str) and v.strip() for v in (node_id, kind, label)):
            raise ValueError("invalid node")
        if kind not in NODE_TYPES:
            raise ValueError("unsupported node type")
        record = {"id": node_id, "kind": kind, "label": label}
        if node_id in self.nodes and self.nodes[node_id] != record:
            raise ValueError("conflicting node")
        self.nodes[node_id] = record
        return record

    def add_edge(self, source, target, relation, evidence_digest, *, inferred=False):
        if source not in self.nodes or target not in self.nodes:
            raise ValueError("edge endpoints must exist")
        if relation not in EDGE_TYPES:
            raise ValueError("unsupported relationship")
        if not isinstance(evidence_digest, str) or len(evidence_digest) != 64 or any(c not in "0123456789abcdef" for c in evidence_digest):
            raise ValueError("evidence digest must be sha256 hex")
        if type(inferred) is not bool:
            raise ValueError("inferred must be boolean")
        payload = {"source": source, "target": target, "relation": relation,
                   "evidence_digest": evidence_digest, "inferred": inferred,
                   "verified": False}
        edge_id = hashlib.sha256(json.dumps(payload, sort_keys=True).encode()).hexdigest()
        self.edges[edge_id] = payload
        return {"edge_id": edge_id, **payload}

    def snapshot(self):
        return {"nodes": [self.nodes[k] for k in sorted(self.nodes)],
                "edges": [{"id": k, **self.edges[k]} for k in sorted(self.edges)],
                "publication_authorized": False}
