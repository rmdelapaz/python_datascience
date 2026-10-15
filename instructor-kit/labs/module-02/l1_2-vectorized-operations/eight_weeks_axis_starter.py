# --- lab bootstrap: find labs_paths.py (the same three lines open every lab; see labs/README.md) ---
import pathlib, sys
sys.path[:0] = [str(p) for p in pathlib.Path(globals().get("__file__", "lab.py")).resolve().parents if (p / "labs_paths.py").is_file()]
from labs_paths import DATA

# %% [markdown]
# # Lab 1.2-B · Eight weeks of transactions, along each axis (STARTER)
# A table of 56 days (rows) by 4 stores (columns). Every question below is one aggregation
# with the right axis. Before each one, say what shape the answer should have:
# "one number per store" is 4 values, "one number per day" is 56.
#
# Expected when you finish: the grand total, four store totals, the first five day totals,
# each store's busiest day (a date), the three busiest days across all stores (dates and
# totals), and how many of the 56 days each store "won".

# %% Build the table (done for you). Columns: Asheville, Bend, Boise, Flagstaff.
import numpy as np


def load(col, dtype=float):
    """Read one column of daily_sales.csv into an array (the helper from Lesson 1.2)."""
    return np.genfromtxt(DATA / "daily_sales.csv", delimiter=",", skip_header=1, usecols=col, dtype=dtype)

dates = load(0, dtype="datetime64[D]")
transactions = load(3)

table = transactions[:224].reshape(56, 4)        # 56 days x 4 stores (January and February 2024)
day = dates[:224].reshape(56, 4)[:, 0]           # one date per row
store_names = np.array(["Asheville", "Bend", "Boise", "Flagstaff"])
print(table.shape, day[0], "to", day[-1])

# %% Step 1: everything, per store, per day
# TODO 1: total (one number), store_total (shape (4,)), day_total (shape (56,))
total = None
store_total = None
day_total = None
print("total:", total)
print("per store:", store_total)
print("per day, first five:", None if day_total is None else day_total[:5])

# %% Step 2: positions, then look them up in a parallel array
# TODO 2: best_row = table.argmax(axis=...)  -> the ROW of each store's busiest day (4 positions)
#         then print day[best_row] to turn positions into dates
best_row = None
print("each store's busiest day:", "TODO 2" if best_row is None else day[best_row])

# %% Step 3: the three busiest days overall
# TODO 3: order = np.argsort(day_total); top3 = the last three positions, largest first
#         print day[top3] and day_total[top3]
print("TODO 3: three busiest days")

# %% Step 4: who won each day?
# TODO 4: winner = table.argmax(axis=...)  -> the COLUMN of the busiest store on each day (56 positions)
#         tally with np.unique(winner, return_counts=True) and print store name + count
print("TODO 4: days won by each store")
