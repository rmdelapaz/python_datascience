# --- lab bootstrap: find labs_paths.py (the same three lines open every lab; see labs/README.md) ---
import pathlib, sys
sys.path[:0] = [str(p) for p in pathlib.Path(globals().get("__file__", "lab.py")).resolve().parents if (p / "labs_paths.py").is_file()]
from labs_paths import DATA

# %% [markdown]
# # Lab 1.4-A · A mystery-shopper schedule nobody can argue with (SOLUTION)
# Head office wants to send a mystery shopper to Flagstaff on 12 days of 2025 and to run a
# pilot in 2 of the 4 stores. If a person picks the days and the stores, someone will say the
# choice was biased. So the generator picks, with a seed, and anyone can rerun it.
#
# Expected when you finish: the 2 pilot stores, 12 different Flagstaff dates in 2025 (sorted),
# how many of them fall on a weekend, proof that the same seed gives the same schedule,
# and a random 70/30 split of all 2,903 rows whose two groups have similar average visitors.
# With the seed 7 your output will match the solution exactly.

# %% Load (done for you)
import numpy as np


def load(col, dtype=float):
    """Read one column of daily_sales.csv into an array (the helper from Lesson 1.2)."""
    return np.genfromtxt(DATA / "daily_sales.csv", delimiter=",", skip_header=1, usecols=col, dtype=dtype)

dates = load(0, dtype="datetime64[D]")
stores = load(1, dtype=str)
visitors = load(2)
weekday = (dates - dates[0]).astype(int) % 7          # 0 = Monday ... 6 = Sunday
store_names = np.unique(stores)

flagstaff_2025 = np.flatnonzero((stores == "Flagstaff") & (dates >= np.datetime64("2025-01-01")))
print(flagstaff_2025.size, "Flagstaff rows in 2025; first row positions:", flagstaff_2025[:3])

# %% Step 1: ONE generator, created once, with a seed
rng = np.random.default_rng(7)

# %% Step 2: two different stores for the pilot
pilot = rng.choice(store_names, size=2, replace=False)
print("pilot stores:", pilot)

# %% Step 3: twelve different Flagstaff days
picks = rng.choice(flagstaff_2025, size=12, replace=False)       # row positions, no repeats
print("shopper dates:", np.sort(dates[picks]))
print("weekend days among them:", (weekday[picks] >= 5).sum(), "of 12")

# %% Step 4: is it reproducible?
again = np.random.default_rng(7)                                 # same seed: back to the first page
pilot_again = again.choice(store_names, size=2, replace=False)
picks_again = again.choice(flagstaff_2025, size=12, replace=False)
print("same schedule from the same seed:", np.array_equal(picks, picks_again))
# The draws must be repeated in the same order: the generator moves forward with every draw.

# %% Step 5: a random 70/30 split of every row
order = rng.permutation(visitors.size)                           # every row position, shuffled
cut = int(visitors.size * 0.7)
group_a, group_b = order[:cut], order[cut:]
print("group sizes:", group_a.size, group_b.size)
print("mean visitors:", visitors[group_a].mean().round(1), "and", visitors[group_b].mean().round(1),
      "| all rows:", visitors.mean().round(1))
# Similar, not identical: that gap is sampling variation.
