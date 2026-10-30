"""GRI synthetic observation resilience comparison, no operational authority."""
import json

# Truth and readings are independently specified in the fixture, not independent sensors.
# (name, authorized, hazard, primary, secondary); None means no observation.
CASES = (
    ('normal', True, False, False, False),
    ('normal_missing_secondary', True, False, False, None),
    ('normal_disagreement', True, False, False, True),
    ('wrong_purpose', False, False, False, False),
    ('expired', False, False, False, False),
    ('revoked', False, False, False, False),
    ('cross_tenant', False, False, False, False),
    ('hazard_detected', True, True, True, True),
    ('hazard_primary_biased', True, True, False, True),
    ('hazard_correlated_bias', True, True, False, False),
    ('hazard_primary_missing', True, True, None, True),
    ('hazard_both_missing', True, True, None, None),
)

def run():
    rows = []
    for name, authorized, hazard, primary, secondary in CASES:
        single = authorized and primary is False
        dual = authorized and primary is False and secondary is False
        review = authorized and (primary is None or secondary is None or primary != secondary)
        rows.append(dict(case=name, authorized=authorized, hazard=hazard,
                         primary=primary, secondary=secondary, single=single,
                         dual=dual, simulated_review_referral=review))
    groups = {
        'unauthorized': [r for r in rows if not r['authorized']],
        'legitimate': [r for r in rows if r['authorized'] and not r['hazard']],
        'hidden_hazard': [r for r in rows if r['authorized'] and r['hazard']],
    }
    metrics = {group: {'denominator': len(items),
                       'single_allowed': sum(r['single'] for r in items),
                       'dual_allowed': sum(r['dual'] for r in items)}
               for group, items in groups.items()}
    return {'status': 'author_defined_synthetic_fixture_only',
            'metrics': metrics,
            'simulated_review_referrals': sum(r['simulated_review_referral'] for r in rows),
            'cases': rows}

if __name__ == '__main__':
    print(json.dumps(run(), sort_keys=True, indent=2))
