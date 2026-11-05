# Issue 13 | Preregistered evaluation protocol

Grand Research Institute | Existing Mobility Intelligence research | 5 November 2026

## Scope and sequence

This is a preregistration-style **protocol specification**, not a registered external study and not a completed prospective evaluation. The offline implementation is in `mobility_evaluation.py`. Use only synthetic or independently authorized and consented records, with the governance gates of issues #11 and #12 observed. No platform API, automated dispatch, or automated acceptance is authorized.

## Primary endpoint

Per eligible scenario, net contribution = gross receipts minus paid and unpaid mileage costs and tolls. Report net contribution in currency units and compare constrained selection against a gross-only feasible rules baseline and the no-drive alternative. An illustrative offline comparison cannot establish causal benefit.

## Safety and feasibility endpoints

Report each of: (1) return deadline adherence, (2) minimum sleep opportunity before next commitment, (3) protected class and other schedule block adherence, (4) maximum duty time, and (5) number of infeasible options selected. The prespecified safety target is **zero** infeasible selections. If all options violate hard constraints or have nonpositive uncertainty-adjusted net, select no drive. Never trade safety for projected gross.

## Forecast endpoints

Chronological training, calibration and untouched holdout partitions are mandatory. Report holdout mean absolute error, last-value rules baseline MAE, nominal and observed interval coverage, and the fraction of holdout observations outside the training range. No shuffled splits. Refit or recalibrate only with data strictly preceding the evaluation horizon. Record sample counts and partition boundaries.

The implemented interval uses the empirical quantile of calibration residuals against a frozen training mean. This is a simple retrospective residual interval, **not a proven calibrated probabilistic forecast** under temporal drift. The out-of-distribution range flag is a minimal diagnostic, not a comprehensive distribution-shift test. Report interval failures and abstain from claims of valid uncertainty when exchangeability is unsupported.

## Reproducibility and stopping conditions

Run `python -m unittest test_mobility_evaluation -v` from this directory. Preserve source commit SHA, Python version, test output, synthetic fixtures, exact chronological split and any exclusions. Do not publish performance claims until authorized prospective evaluation and independent reproduction are available. Stop before any real participant data are introduced without separate ethics, consent, security and retention authorization.
