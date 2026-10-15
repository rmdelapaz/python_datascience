# --- lab bootstrap: find labs_paths.py (the same three lines open every lab; see labs/README.md) ---
import pathlib, sys
sys.path[:0] = [str(p) for p in pathlib.Path(globals().get("__file__", "lab.py")).resolve().parents if (p / "labs_paths.py").is_file()]
from labs_paths import DATA

# %% [markdown]
# # Lab 4.3-B · How many product lines does an order have? (SOLUTION)
# The warehouse plans picking time from the number of product lines on an order. An intern
# hand-checks 150 randomly chosen orders. How well does that sample pin down the mean for all
# orders? Build the standard error and a 95% confidence interval from one sample, then use the
# full data (which the intern never sees) to check whether the "95%" is honest.

# %% Load the order lines and count them per order
import numpy as np
import pandas as pd
from scipy import stats

rng = np.random.default_rng(2025)
items = pd.read_csv(DATA / "order_items.csv")
lines = items.groupby("order_id").size()                 # the "population": every order
population = lines.to_numpy()
print("orders:", len(population), "| mean lines:", round(population.mean(), 3),
      "| SD:", round(population.std(), 3), "| skew:", round(stats.skew(population), 2))

# %% Step 1: the intern's one sample of 150 orders
sample = rng.choice(population, size=150, replace=False)
x_bar = sample.mean()
s = sample.std(ddof=1)
print("sample mean:", round(x_bar, 3), "| sample SD:", round(s, 3))

# %% Step 2: the standard error, two ways
se = s / np.sqrt(len(sample))
print("SE by hand:", round(se, 4), "| scipy.stats.sem:", round(stats.sem(sample), 4))

# %% Step 3: a 95% confidence interval for the mean (t version)
low, high = stats.t.interval(0.95, df=len(sample) - 1, loc=x_bar, scale=se)
print(f"95% CI: {low:.3f} to {high:.3f}")
print("contains the true mean?", bool(low <= population.mean() <= high))

# %% Step 4: SD or SE? The interval is about the MEAN, not about orders
inside = ((population >= low) & (population <= high)).mean()
print(f"share of individual orders inside the interval: {inside:.1%}")
print("(only the orders with exactly 2 lines; the interval describes the mean, not orders)")

# %% Step 5: is "95%" honest? Repeat the whole study 5,000 times
n = 150
many = rng.choice(population, size=(5_000, n))
means = many.mean(axis=1)
ses = many.std(axis=1, ddof=1) / np.sqrt(n)
t_mult = stats.t.ppf(0.975, df=n - 1)
covered = (means - t_mult * ses <= population.mean()) & (population.mean() <= means + t_mult * ses)
print(f"intervals that contain the true mean: {covered.mean():.1%} of 5,000")
print("SD of the 5,000 sample means:", round(means.std(), 4),
      "| sigma / sqrt(n):", round(population.std() / np.sqrt(n), 4))

# %% Step 6: what does four times the work buy?
for size in (150, 600):
    draws = rng.choice(population, size=(2_000, size))
    width = 2 * stats.t.ppf(0.975, df=size - 1) * draws.std(axis=1, ddof=1) / np.sqrt(size)
    print(f"n = {size}: median width of the 95% CI = {np.median(width):.3f} lines")
