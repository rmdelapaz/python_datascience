# --- lab bootstrap: find labs_paths.py (the same three lines open every lab; see labs/README.md) ---
import pathlib, sys
sys.path[:0] = [str(p) for p in pathlib.Path(globals().get("__file__", "lab.py")).resolve().parents if (p / "labs_paths.py").is_file()]
from labs_paths import DATA

# %% [markdown]
# # Lab 1.3-A · A fair comparison of foot traffic (SOLUTION)
# Reference answers. Hand out only after the lab.

# %% Build the table: 224 days x 4 stores, visitors. No values are missing.
import numpy as np


def load(col, dtype=float):
    """Read one column of daily_sales.csv into an array (the helper from Lesson 1.2)."""
    return np.genfromtxt(DATA / "daily_sales.csv", delimiter=",", skip_header=1, usecols=col, dtype=dtype)

dates = load(0, dtype="datetime64[D]")
visitors = load(2)

table = visitors[:896].reshape(224, 4)           # columns: Asheville, Bend, Boise, Flagstaff
day = dates[:896].reshape(224, 4)[:, 0]
print(table.shape, day[0], "to", day[-1])

# %% Step 1: a row of four store averages
store_mean = table.mean(axis=0)                  # shape (4,)
print("store averages:", store_mean.round(1))

# %% Step 2: table and row.  (224, 4) with (4,) -> (224, 4)
ratio = table / store_mean                       # the row is reused on every one of the 224 rows
print("ratio shape:", ratio.shape)
print(ratio[:2].round(2))

# %% Step 3: each store's busiest day, relative to its own normal
print("busiest day, times normal:", ratio.max(axis=0).round(2))
print("on:", day[ratio.argmax(axis=0)])
# All four stores peak on the same date: Saturday of the Memorial Day sale weekend.

# %% Step 4: table and column.  (224, 4) with (224, 1) -> (224, 4)
try:
    table / table.sum(axis=1)                    # (224, 4) with (224,): 4 meets 224, neither is 1
except ValueError as err:
    print("without keepdims:", err)

day_total = table.sum(axis=1, keepdims=True)     # shape (224, 1): a column
share = table / day_total
print("rows add up to:", share.sum(axis=1)[:3])

# %% Step 5: read the share table
print("average share per store:", share.mean(axis=0).round(3))
boise = share[:, 2]
print("Boise's largest share: ", boise.max().round(3), "on", day[boise.argmax()])
print("Boise's smallest share:", boise.min().round(3), "on", day[boise.argmin()])
