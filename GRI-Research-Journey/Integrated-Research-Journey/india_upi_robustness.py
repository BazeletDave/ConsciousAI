"""GRI reproducible aggregate robustness tests; not causal inference.
NPCI UPI April-September 2026 volume in millions.
https://www.npci.org.in/product/upi/product-statistics
"""
import itertools, json
import numpy as np
from scipy.stats import linregress
v=np.array([22346.80,23201.93,22716.07,23658.35,24508.96,24068.38])
x=np.arange(6); y=np.log(v); fit=linregress(x,y)
loo=[100*np.expm1(linregress(np.delete(x,i),np.delete(y,i)).slope) for i in x]
permuted=[linregress(x,p).slope for p in itertools.permutations(y)]
changes=100*np.diff(v)/v[:-1]
print(json.dumps({"n":6,"sum_billion":round(float(v.sum()/1000),5),
"endpoint_growth_pct":round(float(100*(v[-1]/v[0]-1)),4),
"monthly_compound_trend_pct":round(float(100*np.expm1(fit.slope)),4),
"r_squared":round(float(fit.rvalue**2),5),
"leave_one_out_monthly_pct":[round(float(z),4) for z in loo],
"permutation_p_exchangeable_null":round(float(np.mean(np.abs(permuted)>=abs(fit.slope)-1e-12)),6),
"monthly_growth_pct":[round(float(z),4) for z in changes]},indent=2))
