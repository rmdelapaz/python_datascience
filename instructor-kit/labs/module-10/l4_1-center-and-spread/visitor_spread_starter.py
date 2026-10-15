# --- lab bootstrap: find labs_paths.py (the same three lines open every lab; see labs/README.md) ---
import pathlib, sys
sys.path[:0] = [str(p) for p in pathlib.Path(globals().get("__file__", "lab.py")).resolve().parents if (p / "labs_paths.py").is_file()]
from labs_paths import DATA

# %% [markdown]
# # Lab 4.1-B · Which store has the steadiest foot traffic? (STARTER)
# Staffing is easy when every day looks alike and hard when days swing. Measure how much each
# store's daily visitor count varies, four ways, and see which measures survive a bad row.
#
# Expected when you finish: two hand-made variances for five days (one divides by n, one by
# n - 1) that match NumPy and pandas; a table with one row per store and the columns
# mean, median, range, sd, iqr; and a stress test where two measures barely move.

# %% Load the door-counter data (done for you)
import numpy as np
import pandas as pd

daily = pd.read_csv(DATA / "daily_sales.csv", parse_dates=["date"])
print("rows:", len(daily), "| visitors present:", daily["visitors"].count())

# %% Step 1: a variance by hand, on Bend's first five days
five = daily.loc[daily["store"] == "Bend", "visitors"].head(5).to_numpy()
print("five days:", five)
# TODO 1: compute the deviations from the mean, print their sum (what should it be?),
#         then the sum of squared deviations divided by n, and divided by n - 1.
deviations = None

# %% Step 2: match the libraries
# Write your prediction first: np.var(five) equals the "/ n" or the "/ (n - 1)" version? ______
# TODO 2: print np.var(five), pd.Series(five).var(), np.std(five), pd.Series(five).std()
#         and np.std(five, ddof=1). Which pairs agree?

# %% Step 3: four measures of spread for every store
def spread(values):
    """Return mean, median, range, sd (sample) and iqr of one column as a Series."""
    # TODO 3: fill in the five values. q1 and q3 come from values.quantile(0.25) and (0.75).
    return pd.Series({"mean": np.nan, "median": np.nan, "range": np.nan, "sd": np.nan, "iqr": np.nan})

table = daily.groupby("store")["visitors"].apply(spread).unstack().round(1)
print(table)
print("(All NaN until TODO 3 is done.)" if table.isna().all().all() else "")

# %% Step 4: steadiest in visitors, or steadiest for its size?
# TODO 4: add a column sd_over_mean = sd / mean. Which store has the smallest SD?
#         Which has the largest SD relative to its mean? Are they the answers you expected?

# %% Step 5: stress test. The door counter at Bend records 7950 instead of 795 on its busiest day
bend = daily.loc[daily["store"] == "Bend", "visitors"]
broken = bend.copy()
broken.loc[bend.idxmax()] = 7950
# TODO 5: for `bend` and for `broken`, print mean, median, range, SD and IQR.
#         Which measures moved a lot, and which barely moved?
