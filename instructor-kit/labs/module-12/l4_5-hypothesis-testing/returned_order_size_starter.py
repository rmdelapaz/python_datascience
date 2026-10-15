# --- lab bootstrap: find labs_paths.py (the same three lines open every lab; see labs/README.md) ---
import pathlib, sys
sys.path[:0] = [str(p) for p in pathlib.Path(globals().get("__file__", "lab.py")).resolve().parents if (p / "labs_paths.py").is_file()]
from labs_paths import DATA

# %% [markdown]
# # Lab 4.5-A · Are returned orders bigger? (STARTER)
# Customer service believes "people send back the big orders". Compare the order totals of
# returned and completed orders: state the hypotheses, run a Welch t-test, get the confidence
# interval and the effect size, confirm with a permutation test, then challenge the result.
#
# Expected when you finish: a difference of about $25 with a 95% CI that excludes 0, a very
# small p-value, a SMALL Cohen's d, a permutation p-value that agrees, the same comparison
# within online orders only, and a report that says both "real" and "small".

# %% Load the orders (done for you)
import numpy as np
import pandas as pd
from scipy import stats

orders = pd.read_csv(DATA / "orders.csv", parse_dates=["order_date"])
returned = orders.loc[orders["status"] == "returned", "order_total"]
completed = orders.loc[orders["status"] == "completed", "order_total"]

# TODO 0: BEFORE any test, write the null and alternative hypotheses and alpha here:
# H0: ______
# H1: ______

# %% Step 1: look before you test
# TODO 1: for each group print n, mean, median, SD and skew. Are the groups very different
#         in size? Is the data skewed? Is the sample large enough for the CLT to help?

# %% Step 2: Welch t-test with its confidence interval
# TODO 2: res = stats.ttest_ind(returned, completed, equal_var=False)   (equal_var=False!)
#         ci = res.confidence_interval(); print the difference, the CI, t, df and p.
res = None

# %% Step 3: effect size
def cohens_d(x, y):
    """Difference in means divided by the pooled standard deviation."""
    nx, ny = len(x), len(y)
    pooled = ((nx - 1) * np.var(x, ddof=1) + (ny - 1) * np.var(y, ddof=1)) / (nx + ny - 2)
    return (np.mean(x) - np.mean(y)) / np.sqrt(pooled)

# TODO 3: print Cohen's d. Small, medium or large (0.2, 0.5, 0.8)?

# %% Step 4: a second opinion that needs no normal theory
# TODO 4: stats.permutation_test((returned, completed), mean_diff, n_resamples=9_999,
#         rng=np.random.default_rng(42)) with a mean_diff(x, y) function you write.
#         (It takes a few seconds.) Does it agree with Step 2?

# %% Step 5: challenge it
# TODO 5: returns are mostly online orders. Print the mean order total by channel, then repeat
#         Step 2 and Step 3 for online orders only. Does the gap survive?

# %% Step 6: the report
# TODO 6: print a report with: what was compared (and n), the difference with its CI, the
#         test and p-value, the effect size in words, and one caveat.
if res is None:
    print("TODO 1-6 not done yet: `res` is still None.")
