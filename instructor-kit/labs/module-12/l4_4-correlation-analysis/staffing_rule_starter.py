# --- lab bootstrap: find labs_paths.py (the same three lines open every lab; see labs/README.md) ---
import pathlib, sys
sys.path[:0] = [str(p) for p in pathlib.Path(globals().get("__file__", "lab.py")).resolve().parents if (p / "labs_paths.py").is_file()]
from labs_paths import DATA

# %% [markdown]
# # Lab 4.4-B · Recover the staffing rule (STARTER)
# Managers schedule staff in advance from the traffic they expect. Can a regression line
# recover their rule of thumb from the data? Fit it, read every number in the units of the
# data, use it carefully, and see why the same data gives a different line the other way round.
#
# Expected when you finish: a slope of about 1.6 staff per 100 visitors with r about 0.93; a
# prediction for a 400-visitor day with its typical miss; four store slopes that are almost
# identical; a reversed line that is NOT 1 / slope; and three sentences on what the line does
# not say.

# %% Load the store-days (done for you)
import numpy as np
import pandas as pd
from scipy import stats

daily = pd.read_csv(DATA / "daily_sales.csv", parse_dates=["date"])
x, y = daily["visitors"], daily["staff_on_duty"]
print("store-days:", len(daily), "| visitors", x.min(), "to", x.max(), "| staff", y.min(), "to", y.max())

# %% Step 1: the line, staff predicted from visitors
# TODO 1: fit = stats.linregress(x, y)   (predictor first). Print the slope (also per 100
#         visitors), the intercept, r and r squared. Say the slope in words, with its units.
fit = None

# %% Step 2: use it, with its typical miss
# TODO 2: predict staff for a 400-visitor day, and print the SD of the residuals
#         (actual minus predicted): "give or take" for a single day.

# %% Step 3: one rule for every store?
# TODO 3: fit the same line separately for each store (groupby("store")) and print each slope
#         per 100 visitors and each intercept. One rule, or four?

# %% Step 4: the other way round
# Predict first: if staff = 0.84 + 0.0159 x visitors, is the line for visitors from staff
# simply visitors = (staff - 0.84) / 0.0159?  ______
# TODO 4: fit stats.linregress(y, x). Compare its slope with 1 / fit.slope, and compare r.

# %% Step 5: what the line does not say
# TODO 5: three sentences: what the slope describes, why it is not "staff bring visitors",
#         and which predictions it cannot make.
if fit is None:
    print("TODO 1-5 not done yet: `fit` is still None.")
