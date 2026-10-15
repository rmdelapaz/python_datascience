# --- lab bootstrap: find labs_paths.py (the same three lines open every lab; see labs/README.md) ---
import pathlib, sys
sys.path[:0] = [str(p) for p in pathlib.Path(globals().get("__file__", "lab.py")).resolve().parents if (p / "labs_paths.py").is_file()]
from labs_paths import DATA

# %% [markdown]
# # Lab 4.3-A · A normal model for walk-in conversion (STARTER)
# Each store-day, some share of the people who walk in buy something:
# conversion = transactions / visitors. Store managers want to know what a "bad day" and a
# "great day" look like. Fit a normal model, check it against the data, then use the four
# methods (cdf, sf, ppf, rvs) to answer their questions.
#
# Expected when you finish: a mean near 0.235 and a skew near 0; three "within k SD" lines
# where the data and the model agree to within about one percentage point; four model-against-
# data lines; a simulated year; and one sentence for the managers.

# %% Load the data and build the column (done for you)
import numpy as np
import pandas as pd
from scipy import stats

rng = np.random.default_rng(11)          # ONE generator, created once, used for every draw
daily = pd.read_csv(DATA / "daily_sales.csv", parse_dates=["date"])
conversion = daily["transactions"] / daily["visitors"]
print("store-days:", len(conversion), "| missing:", conversion.isna().sum())

# %% Step 1: describe before you model
# TODO 1: compute mu (the mean) and sigma (the SD) of `conversion`, and print them with the skew.
#         Is a bell curve a reasonable shape to try?
mu, sigma = None, None

# %% Step 2: freeze a normal distribution with the data's own mean and SD
# TODO 2: model = stats.norm(loc=..., scale=...)     (scale is the SD, not the variance)
model = None

# %% Step 3: check the model. Does the 68-95-99.7 rule hold?
# TODO 3: for k in (1, 2, 3) print the share of the DATA within k SDs of the mean, and the
#         share the MODEL puts there (a difference of two cdf values).

# %% Step 4: the managers' questions, model against data
# Write the method you will use next to each question BEFORE you code it:
#   P(conversion below 20%)        method: ______
#   P(conversion above 27%)        method: ______
#   the 5th percentile (a bad day) method: ______
# TODO 4: answer each one with the model, and print the same quantity from the data beside it.

# %% Step 5: simulate a year of store-days and count the bad ones
# TODO 5: year = model.rvs(size=365, random_state=rng); count the days below 0.20 and compare
#         with what the model expects (365 * model.cdf(0.20)).

# %% Step 6: one sentence for the managers
# TODO 6: print a sentence built from your variables: the typical conversion, and what counts
#         as a bad day and a great day.
if model is None:
    print("TODO 1-6 not done yet: `model` is still None.")
