# --- lab bootstrap: find labs_paths.py (the same three lines open every lab; see labs/README.md) ---
import pathlib, sys
sys.path[:0] = [str(p) for p in pathlib.Path(globals().get("__file__", "lab.py")).resolve().parents if (p / "labs_paths.py").is_file()]
from labs_paths import DATA

# %% [markdown]
# # Lab 4.5-A · Are returned orders bigger? (SOLUTION)
# Customer service believes "people send back the big orders". Compare the order totals of
# returned and completed orders: state the hypotheses, run a Welch t-test, get the confidence
# interval and the effect size, confirm with a permutation test, then challenge the result.

# %% Load the orders
import numpy as np
import pandas as pd
from scipy import stats

orders = pd.read_csv(DATA / "orders.csv", parse_dates=["order_date"])
returned = orders.loc[orders["status"] == "returned", "order_total"]
completed = orders.loc[orders["status"] == "completed", "order_total"]

# H0: returned and completed orders have the same mean order total.
# H1: the means differ (two-sided). alpha = 0.05. Welch t-test.

# %% Step 1: look before you test
for name, g in [("returned", returned), ("completed", completed)]:
    print(f"{name:<9} n {len(g):5d}  mean {g.mean():7.2f}  median {g.median():7.2f}  "
          f"SD {g.std():6.2f}  skew {g.skew():4.1f}")

# %% Step 2: Welch t-test with its confidence interval
res = stats.ttest_ind(returned, completed, equal_var=False)
ci = res.confidence_interval()
print(f"difference {returned.mean() - completed.mean():.2f}, 95% CI {ci.low:.2f} to {ci.high:.2f}")
print(f"t = {res.statistic:.2f}, df = {res.df:.0f}, p = {res.pvalue:.1e}")

# %% Step 3: effect size
def cohens_d(x, y):
    nx, ny = len(x), len(y)
    pooled = ((nx - 1) * np.var(x, ddof=1) + (ny - 1) * np.var(y, ddof=1)) / (nx + ny - 2)
    return (np.mean(x) - np.mean(y)) / np.sqrt(pooled)

print(f"Cohen's d = {cohens_d(returned, completed):.2f}")

# %% Step 4: a second opinion that needs no normal theory
def mean_diff(x, y):
    return np.mean(x) - np.mean(y)

perm = stats.permutation_test((returned, completed), mean_diff, n_resamples=9_999,
                              rng=np.random.default_rng(42))
print(f"permutation p-value = {perm.pvalue:.4f}  (9,999 shuffles: 0.0002 is the smallest possible)")

# %% Step 5: challenge it. Returns are mostly online; are online orders simply bigger?
print(orders.groupby("channel")["order_total"].mean().round(2).to_string())
online = orders[orders["channel"] == "online"]
r_on = online.loc[online["status"] == "returned", "order_total"]
c_on = online.loc[online["status"] == "completed", "order_total"]
res_on = stats.ttest_ind(r_on, c_on, equal_var=False)
ci_on = res_on.confidence_interval()
print(f"online only: difference {r_on.mean() - c_on.mean():.2f}, "
      f"95% CI {ci_on.low:.2f} to {ci_on.high:.2f}")
print(f"             p = {res_on.pvalue:.1e}, d = {cohens_d(r_on, c_on):.2f}")

# %% Step 6: the report
print("Returned orders average about $25 more than completed ones (95% CI $15 to $36;")
print("Welch p = 1.1e-06; permutation test agrees). The effect is small (d = 0.14):")
print("the two groups overlap almost completely. Within online orders alone the gap")
print("is about $24, so it is not only a channel difference. Observational data.")
