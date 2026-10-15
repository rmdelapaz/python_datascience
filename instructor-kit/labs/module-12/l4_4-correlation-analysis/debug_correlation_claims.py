# --- lab bootstrap: find labs_paths.py (the same three lines open every lab; see labs/README.md) ---
import pathlib, sys
sys.path[:0] = [str(p) for p in pathlib.Path(globals().get("__file__", "lab.py")).resolve().parents if (p / "labs_paths.py").is_file()]
from labs_paths import DATA

# %% [markdown]
# # Lab 4.4 · Find the bugs: four correlation claims that are wrong (DEBUG HANDOUT)
# Every line runs. Every claim printed below is wrong or overstated. For each one, say what
# is wrong and rewrite the claim (or the code) so it is true.
# There is no solution file: the lesson's Common Mistakes and the r-is-not-a-slope warning
# are the answer.

# %%
import numpy as np
import pandas as pd

daily = pd.read_csv(DATA / "daily_sales.csv", parse_dates=["date"])

# %% Claim 1: "Visitors and revenue are unrelated: the correlation is missing"
print("Claim 1: r =", np.corrcoef(daily["visitors"], daily["revenue"])[0, 1])

# %% Claim 2: "r = 0.94, so each extra visitor brings in 94 cents"
r = daily["visitors"].corr(daily["revenue"])
print(f"Claim 2: r = {r:.2f}, so each extra visitor brings in {r * 100:.0f} cents")

# %% Claim 3: "Staff and transactions: r = 0.90, so staffing explains 90% of transactions"
r_st = daily["staff_on_duty"].corr(daily["transactions"])
print(f"Claim 3: r = {r_st:.2f}, so staffing explains {r_st:.0%} of the variation in transactions")

# %% Claim 4: "u and u squared have no relationship at all: look at r"
u = pd.Series(np.arange(-5, 6))
print("Claim 4: r between u and u squared =", u.corr(u ** 2), "so the two are unrelated")
