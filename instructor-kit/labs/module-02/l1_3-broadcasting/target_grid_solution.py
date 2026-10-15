# --- lab bootstrap: find labs_paths.py (the same three lines open every lab; see labs/README.md) ---
import pathlib, sys
sys.path[:0] = [str(p) for p in pathlib.Path(globals().get("__file__", "lab.py")).resolve().parents if (p / "labs_paths.py").is_file()]
from labs_paths import DATA

# %% [markdown]
# # Lab 1.3-B · A grid of targets, and a grid nobody asked for (SOLUTION)
# Reference answers. Hand out only after the lab.

# %% Load
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

# %% Step 1: predict, then check
try:
    print(np.broadcast_shapes((4,), (3,)))
except ValueError as err:
    print("(4,) with (3,): fails:", err)                           # 4 meets 3, neither is 1
print("(4, 1) with (3,):   ", np.broadcast_shapes((4, 1), (3,)))    # 1 meets 3, 4 meets a missing axis
print("(224, 4) with (4,): ", np.broadcast_shapes((224, 4), (4,)))  # a table and a row
print("(4,) with (4, 1):   ", np.broadcast_shapes((4,), (4, 1)))    # a row and a column: a 4 x 4 grid

# %% Step 2: column meets row
targets = current[:, np.newaxis] * (1 + growth)                    # (4, 1) with (3,) -> (4, 3)
print(targets.shape)
print(targets.round(0))

# %% Step 3: a mask on the grid
above = targets > 7500
print("targets above $7,500:", above.sum(), "of", above.size)
print("per store:", above.sum(axis=1))                             # axis 1 (scenarios) disappears: one count per store

# %% Step 4: the accidental grid
actual = current                                                   # shape (4,)
forecast = np.array([[5900.0], [6800.0], [10400.0], [6700.0]])     # came from another program as a COLUMN
wrong = actual - forecast                                          # (4,) with (4, 1) -> (4, 4): every actual minus every forecast
print("wrong shape:", wrong.shape, "| average size:", np.abs(wrong).mean().round(2))

errors = actual - forecast.ravel()                                 # (4,) with (4,) -> (4,)
print("errors shape:", errors.shape)
print("errors:", errors.round(2))
print("average size of an error:", np.abs(errors).mean().round(2))
