"""Offline agent action simulator. No real tools, credentials, or network."""
from dataclasses import dataclass
from hashlib import sha256
import json
from guardrail import Policy, Action, authorize

@dataclass(frozen=True)
class Attempt:
    case_id: str
    action: Action
    expected_allow: bool
    family: str

class Simulator:
    def __init__(self, policy: Policy, enforce: bool = True):
        self.policy = policy
        self.enforce = enforce
        self.state = {}
        self.audit = []
        self._last_hash = '0' * 64

    def run(self, attempt: Attempt) -> dict:
        permitted, reason = authorize(self.policy, attempt.action)
        executed = permitted or not self.enforce
        if executed:
            self.state.setdefault(attempt.action.resource, []).append({
                'case_id': attempt.case_id, 'tool': attempt.action.tool,
                'amount': attempt.action.amount})
        entry = {'sequence': len(self.audit), 'case_id': attempt.case_id,
                 'family': attempt.family, 'expected_allow': attempt.expected_allow,
                 'decision_allow': permitted, 'decision_reason': reason,
                 'tool_executed': executed, 'resource': attempt.action.resource,
                 'policy_digest': self.policy.digest, 'previous_hash': self._last_hash}
        digest = sha256(json.dumps(entry, sort_keys=True, separators=(',', ':'),
                                   allow_nan=False).encode()).hexdigest()
        entry['entry_hash'] = digest
        self.audit.append(entry)
        self._last_hash = digest
        return dict(entry)

def verify_chain(audit: list[dict]) -> bool:
    previous = '0' * 64
    for index, record in enumerate(audit):
        item = dict(record)
        digest = item.pop('entry_hash', None)
        if item.get('sequence') != index or item.get('previous_hash') != previous:
            return False
        if sha256(json.dumps(item, sort_keys=True, separators=(',', ':'),
                             allow_nan=False).encode()).hexdigest() != digest:
            return False
        previous = digest
    return True

def run_experiment(attempts: list[Attempt], policy: Policy, enforce: bool = True) -> dict:
    sim = Simulator(policy, enforce)
    events = [sim.run(a) for a in attempts]
    bad = [e for e in events if not e['expected_allow']]
    legitimate = [e for e in events if e['expected_allow']]
    escapes = sum(e['tool_executed'] for e in bad)
    blocked_legitimate = sum(not e['tool_executed'] for e in legitimate)
    return {'mode': 'enforced' if enforce else 'monitor_only',
            'attempts': len(events), 'unauthorized_attempts': len(bad),
            'unauthorized_executions': escapes,
            'unauthorized_execution_rate': escapes / len(bad) if bad else None,
            'legitimate_attempts': len(legitimate),
            'legitimate_block_rate': blocked_legitimate / len(legitimate) if legitimate else None,
            'audit_chain_valid': verify_chain(events),
            'audit': events, 'state': sim.state,
            'limitations': ['Synthetic deterministic simulator, not real agent/tool execution',
                            'Hash chaining requires a separately trusted anchor',
                            'No signed identity, concurrent replay, semantic classification or latency benchmark']}

if __name__ == '__main__':
    from measurable_eval import POLICY, fixtures
    import argparse
    from pathlib import Path
    parser = argparse.ArgumentParser()
    parser.add_argument('--out', default='simulation_results.json')
    args = parser.parse_args()
    attempts = [Attempt(row['id'], Action(**row['action']), row['expected_allow'], row['family']) for row in fixtures()]
    report = {'enforced': run_experiment(attempts, POLICY, True),
              'monitor_only': run_experiment(attempts, POLICY, False)}
    Path(args.out).write_text(json.dumps(report, indent=2, allow_nan=False)+'\n', encoding='utf-8')
    print(json.dumps({mode: {k:v for k,v in result.items() if k not in ('audit','state','limitations')}
                      for mode,result in report.items()}, indent=2))
