"""Synthetic Monte Carlo extension: paired observation gates, correlated error.

No operational security claim. Uses seeded random fixtures independent of gate code.
"""
import argparse
import json
import random

def simulate(seed=20261030, n=10000, hazard_rate=0.20, unauthorized_rate=0.15,
             miss_rate=0.20, false_alarm_rate=0.05, shared_error=0.0):
    if not isinstance(n, int) or n < 1:
        raise ValueError("n must be positive")
    for value in (hazard_rate, unauthorized_rate, miss_rate, false_alarm_rate, shared_error):
        if not 0 <= value <= 1:
            raise ValueError("probabilities must be between zero and one")
    rng = random.Random(seed)
    counts = {name: {"unauthorized_allowed": 0, "hazards_allowed": 0,
                     "legitimate_allowed": 0, "holds": 0}
              for name in ("single", "dual")}
    denominators = {"unauthorized": 0, "hazard_authorized": 0, "legitimate_authorized": 0}
    for _ in range(n):
        authorized = rng.random() >= unauthorized_rate
        hazard = rng.random() < hazard_rate
        if not authorized:
            denominators["unauthorized"] += 1
        elif hazard:
            denominators["hazard_authorized"] += 1
        else:
            denominators["legitimate_authorized"] += 1
        # True denotes a hazard alarm. Shared-error is a mixture of common
        # failure and conditionally independent error draws, not a measured correlation.
        error1 = rng.random() < (miss_rate if hazard else false_alarm_rate)
        error2 = error1 if rng.random() < shared_error else (
            rng.random() < (miss_rate if hazard else false_alarm_rate))
        alarm1 = hazard != error1
        alarm2 = hazard != error2
        for policy, allowed in (("single", authorized and not alarm1),
                                ("dual", authorized and not alarm1 and not alarm2)):
            c = counts[policy]
            if not allowed:
                c["holds"] += 1
            if allowed and not authorized:
                c["unauthorized_allowed"] += 1
            elif allowed and hazard:
                c["hazards_allowed"] += 1
            elif allowed:
                c["legitimate_allowed"] += 1
    return {"status": "synthetic_simulation_only", "seed": seed, "n": n,
            "parameters": {"hazard_rate": hazard_rate, "unauthorized_rate": unauthorized_rate,
                           "miss_rate": miss_rate, "false_alarm_rate": false_alarm_rate,
                           "shared_error_mixture": shared_error},
            "denominators": denominators, "counts": counts,
            "additional_observation_attempts": n}

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--seed", type=int, default=20261030)
    parser.add_argument("--n", type=int, default=10000)
    parser.add_argument("--shared-error", type=float, default=0)
    args = parser.parse_args()
    print(json.dumps(simulate(seed=args.seed, n=args.n, shared_error=args.shared_error),
                     sort_keys=True, indent=2))
