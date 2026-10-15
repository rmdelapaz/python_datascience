# --- lab bootstrap: find labs_paths.py (the same three lines open every lab; see labs/README.md) ---
import pathlib, sys
sys.path[:0] = [str(p) for p in pathlib.Path(globals().get("__file__", "lab.py")).resolve().parents if (p / "labs_paths.py").is_file()]
from labs_paths import DATA

# %% [markdown]
# # Lab 1.3-B · A grid of targets, and a grid nobody asked for (STARTER)
# Part 1: Pinecrest wants next year's daily revenue target for each store under three
# growth scenarios. Four stores x three scenarios = twelve numbers: a column meeting a row.
# Part 2: a forecast check that goes quietly wrong because of one shape.
#
# Expected when you finish: four shape predictions checked with np.broadcast_shapes,
# a (4, 3) table of targets, how many targets pass $7,500 (in total and per store),
# then four forecast errors whose average size is 209.9 (not 1753.02).

# %% Load (done for you)
import numpy as np


def load(col, dtype=float):
    """Read one column of daily_sales.csv into an array (the helper from Lesson 1.2)."""
    return np.genfromtxt(DATA / "daily_sales.csv", delimiter=",", skip_header=1, usecols=col, dtype=dtype)

stores = load(1, dtype=str)
revenue = load(5)
store_names = np.unique(stores)                                    # Asheville, Bend, Boise, Flagstaff
current = np.array([np.nanmean(revenue[stores == name]) for name in store_names])   # a loop over 4 stores is fine
growth = np.array([0.03, 0.05, 0.10])                              # three scenarios
print(store_names)
print(current.round(2), current.shape, growth.shape)

# %% Step 1: predict, then check. Write your prediction before you run each line.
# TODO 1: uncomment one at a time. One of them raises an error: which, and why?
# print(np.broadcast_shapes((4,), (3,)))        # my prediction: ________
# print(np.broadcast_shapes((4, 1), (3,)))      # my prediction: ________
# print(np.broadcast_shapes((224, 4), (4,)))    # my prediction: ________
# print(np.broadcast_shapes((4,), (4, 1)))      # my prediction: ________
print("TODO 1: four shape predictions")

# %% Step 2: column meets row
# TODO 2: targets = current as a COLUMN (shape (4, 1)) times (1 + growth)
#         use current[:, np.newaxis] or current.reshape(-1, 1)
targets = None

if targets is None:
    print("TODO 2-3: `targets` is still None")
else:
    print(targets.shape)
    print(targets.round(0))
    # %% Step 3: a mask on the grid
    # TODO 3: how many of the twelve targets are above 7500? And how many per store (axis=1)?
    print("TODO 3: targets above $7,500")

# %% Step 4: the accidental grid
actual = current                                                   # shape (4,)
forecast = np.array([[5900.0], [6800.0], [10400.0], [6700.0]])     # came from another program as a COLUMN
errors = actual - forecast
print("errors shape:", errors.shape)                               # four stores should give four errors!
print("average size of an error:", np.abs(errors).mean().round(2))
# TODO 4: fix the line `errors = ...` so that there are four errors (forecast.ravel() flattens),
#         then print the four errors and their average size again.
