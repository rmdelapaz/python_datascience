# --- lab bootstrap: find labs_paths.py (the same three lines open every lab; see labs/README.md) ---
import pathlib, sys
sys.path[:0] = [str(p) for p in pathlib.Path(globals().get("__file__", "lab.py")).resolve().parents if (p / "labs_paths.py").is_file()]
from labs_paths import DATA

# %% [markdown]
# # Lab 1.2-B · Eight weeks of transactions, along each axis (SOLUTION)
# Reference answers. Hand out only after the lab.

# %% Build the table. Columns: Asheville, Bend, Boise, Flagstaff.
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
total = table.sum()
store_total = table.sum(axis=0)        # axis 0 (the 56 days) disappears: 4 values
day_total = table.sum(axis=1)          # axis 1 (the 4 stores) disappears: 56 values
print("total:", total)
print("per store:", store_total)
print("per day, first five:", day_total[:5])
print("shapes:", store_total.shape, day_total.shape)

# %% Step 2: positions, then look them up in a parallel array
best_row = table.argmax(axis=0)        # for each store, the row of its busiest day
print("each store's busiest day:", day[best_row])
print("transactions that day:   ", table.max(axis=0))

# %% Step 3: the three busiest days overall
order = np.argsort(day_total)          # positions, smallest total first
top3 = order[::-1][:3]
print("three busiest days:", day[top3], day_total[top3])

# %% Step 4: who won each day?
winner = table.argmax(axis=1)          # for each day, the column of the busiest store
cols, counts = np.unique(winner, return_counts=True)
for col, count in zip(cols, counts):
    print(f"{store_names[col]:<10} won {count:>2} of 56 days")
