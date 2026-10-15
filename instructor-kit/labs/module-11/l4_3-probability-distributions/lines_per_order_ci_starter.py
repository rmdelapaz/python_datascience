# --- lab bootstrap: find labs_paths.py (the same three lines open every lab; see labs/README.md) ---
import pathlib, sys
sys.path[:0] = [str(p) for p in pathlib.Path(globals().get("__file__", "lab.py")).resolve().parents if (p / "labs_paths.py").is_file()]
from labs_paths import DATA

# %% [markdown]
# # Lab 4.3-B · How many product lines does an order have? (STARTER)
# The warehouse plans picking time from the number of product lines on an order. An intern
# hand-checks 150 randomly chosen orders. How well does that sample pin down the mean for all
# orders? Build the standard error and a 95% confidence interval from one sample, then use the
# full data (which the intern never sees) to check whether the "95%" is honest.
#
# Expected when you finish: a sample mean close to (not equal to) the true mean; a standard
# error computed two ways that match; an interval about a third of a line wide; a share of
# individual orders "inside" the interval that is nowhere near 95%; coverage close to 95% over
# 5,000 repeats; and an interval about half as wide when the sample is four times as large.

# %% Load the order lines and count them per order (done for you)
import numpy as np
import pandas as pd
from scipy import stats

rng = np.random.default_rng(2025)          # ONE generator, created once
items = pd.read_csv(DATA / "order_items.csv")
lines = items.groupby("order_id").size()                 # the "population": every order
population = lines.to_numpy()
print("orders:", len(population), "| mean lines:", round(population.mean(), 3),
      "| SD:", round(population.std(), 3), "| skew:", round(stats.skew(population), 2))

# %% Step 1: the intern's one sample of 150 orders (done for you)
sample = rng.choice(population, size=150, replace=False)

# TODO 1: compute x_bar (the sample mean) and s (the sample SD, ddof=1) and print them.
x_bar, s = None, None

# %% Step 2: the standard error, two ways
# TODO 2: se = s / sqrt(n). Check it against stats.sem(sample).
se = None

# %% Step 3: a 95% confidence interval for the mean (t version)
# TODO 3: low, high = stats.t.interval(0.95, df=len(sample) - 1, loc=x_bar, scale=se)
#         Print the interval, and whether it contains population.mean().
low, high = None, None

# %% Step 4: SD or SE? The interval is about the MEAN, not about orders
# Write your prediction first: what share of individual orders have a line count
# between `low` and `high`?  about 95%, or far fewer? ________
# TODO 4: compute that share from `population`.

# %% Step 5: is "95%" honest? Repeat the whole study 5,000 times
# TODO 5: many = rng.choice(population, size=(5_000, 150)); one mean and one SE per row
#         (axis=1, ddof=1); build 5,000 intervals; print the share that contain population.mean().

# %% Step 6: what does four times the work buy?
# TODO 6: repeat for n = 600 (2,000 samples is plenty) and compare the median interval width
#         with n = 150. By what factor did it shrink, and why?
if x_bar is None:
    print("TODO 1-6 not done yet: `x_bar` is still None.")
