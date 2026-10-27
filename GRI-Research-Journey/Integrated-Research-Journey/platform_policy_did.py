"""Synthetic platform policy Difference in Differences model.
Research contribution: David Grand, Grand Research Institute.
Run: python platform_policy_did.py
Dependencies: numpy, pandas, statsmodels (see requirements-platform-did.txt).
"""
import numpy as np
import pandas as pd
import statsmodels.api as sm
import statsmodels.formula.api as smf

# Synthetic Panel Data: Tracking reach before and after a platform policy shift
# Treatment = Accounts affected by strict automated flagging
# Post = Time period after platform algorithmic policy update
# Design note: observations are independently sampled group/period cells;
# account identifiers and repeated observations are not generated here.

np.random.seed(101)
n_samples = 1000

df_causal = pd.DataFrame({
    'candidate_group': np.random.choice([0, 1], size=n_samples), # 1 = Targeted Group, 0 = Control
    'post_policy_change': np.random.choice([0, 1], size=n_samples), # 1 = After update, 0 = Before
    'baseline_engagement': np.random.normal(50, 10, size=n_samples),
})

# Simulate outcome: Interaction term (DiD effect) represents algorithmic suppression or boost
# True causal effect of algorithmic change = -8.5 unit drop in reach
df_causal['reach'] = (
    df_causal['baseline_engagement']
    + 5 * df_causal['candidate_group']
    - 3 * df_causal['post_policy_change']
    - 8.5 * (df_causal['candidate_group'] * df_causal['post_policy_change'])
    + np.random.normal(0, 3, size=n_samples)
)

# Fit OLS Difference-in-Differences Model
model = smf.ols('reach ~ candidate_group * post_policy_change', data=df_causal).fit()

print(model.summary().tables[1])
