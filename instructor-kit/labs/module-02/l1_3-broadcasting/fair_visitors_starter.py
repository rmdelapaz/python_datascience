# --- lab bootstrap: find labs_paths.py (the same three lines open every lab; see labs/README.md) ---
import pathlib, sys
sys.path[:0] = [str(p) for p in pathlib.Path(globals().get("__file__", "lab.py")).resolve().parents if (p / "labs_paths.py").is_file()]
from labs_paths import DATA

# %% [markdown]
# # Lab 1.3-A · A fair comparison of foot traffic (STARTER)
# Boise always has the most visitors, so raw counts only say "Boise is bigger". Divide each
# store by its OWN average (a table and a row) and you can ask a better question:
# which day was the busiest FOR EACH STORE, and how busy was it compared with normal?
# Then divide each day by its OWN total (a table and a column) for each store's share.
#
# Before every operation, write the two shapes one above the other and predict the result.
#
# Expected when you finish: four store averages, a ratio table of shape (224, 4), each
# store's busiest day as a ratio and a date, a share table whose rows add up to 1, the
# average share per store, and Boise's largest and smallest share of a day.

# %% Build the table (done for you): 224 days x 4 stores, visitors. No values are missing.
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
# TODO 1: store_mean = table.mean(axis=...)      -> shape (4,)
store_mean = None
print("store averages:", store_mean)

# %% Step 2: table and row.  Shapes: (224, 4) and (4,)  ->  predict: ________
# TODO 2: ratio = table / store_mean
ratio = None

if ratio is None:
    print("TODO 2-3: `ratio` is still None")
else:
    print("ratio shape:", ratio.shape)
    # %% Step 3: each store's busiest day, relative to its own normal
    # TODO 3: print ratio.max(axis=0).round(2) and day[ratio.argmax(axis=0)]
    print("TODO 3: busiest day per store")

# %% Step 4: table and column.  Shapes: (224, 4) and (224, 1)  ->  predict: ________
# TODO 4: day_total = table.sum(axis=1, keepdims=True); share = table / day_total
#         (try it once WITHOUT keepdims=True and read the error message from the right)
share = None

if share is None:
    print("TODO 4-5: `share` is still None")
else:
    print("rows add up to:", share.sum(axis=1)[:3])
    # %% Step 5: read the share table
    # TODO 5: print share.mean(axis=0).round(3); then Boise's (column 2) largest and smallest
    #         share and the dates they happened on (max / argmax, min / argmin)
    print("TODO 5: average share per store; Boise's extremes")
