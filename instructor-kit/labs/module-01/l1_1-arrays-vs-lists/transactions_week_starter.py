# --- lab bootstrap: find labs_paths.py (the same three lines open every lab; see labs/README.md) ---
import pathlib, sys
sys.path[:0] = [str(p) for p in pathlib.Path(globals().get("__file__", "lab.py")).resolve().parents if (p / "labs_paths.py").is_file()]
from labs_paths import DATA

# %% [markdown]
# # Lab 1.1-A · A week of transactions (STARTER)
# The lesson loaded the revenue column. Here you load a different column, `transactions`
# (how many sales each store rang up each day), describe the array, and slice one week
# out of it as a days-by-stores table.
#
# Expected when you finish: the four facts about the array (shape, dtype, ndim, size),
# the number of missing values, the second week of January 2024 as a 7 x 4 table,
# Saturday's row, Bend's column, the busiest store-day of the week, and the bytes the
# table needs as float64 and as int16.

# %% Load one column (done for you). Column 3 is `transactions`.
import numpy as np

transactions = np.genfromtxt(DATA / "daily_sales.csv", delimiter=",", skip_header=1, usecols=3)
print("first eight values:", transactions[:8])

# %% Step 1: four facts every array knows about itself
# TODO 1: print the shape, dtype, ndim and size of `transactions`
print("TODO 1: shape, dtype, ndim, size")

# %% Step 2: is anything missing?
# TODO 2: count the nan values with np.isnan(...).sum() and store the count in `missing`
missing = None
print("missing values:", missing if missing is not None else "TODO 2")

# %% Step 3: slice out the second week and give it a shape
# The file is sorted by date, then store (Asheville, Bend, Boise, Flagstaff), and January has
# no gaps, so rows 0-27 are Monday 1 Jan to Sunday 7 Jan and rows 28-55 are the week after.
# TODO 3: week2 = transactions[...].reshape(..., ...)   -> 7 rows (days) by 4 columns (stores)
week2 = None

# %% Step 4: rows, columns and one cell
# Rows are Mon=0 ... Sun=6. Columns are Asheville=0, Bend=1, Boise=2, Flagstaff=3.
if week2 is None:
    print("TODO 3-6: `week2` is still None")
else:
    print(week2)
    # TODO 4: print Saturday's row, Bend's column, and Boise on Saturday (one cell)
    # TODO 5: print the largest value in the table with week2.max()

    # %% Step 6: a smaller dtype
    # TODO 6: small = week2.astype(np.int16); print week2.nbytes and small.nbytes,
    #         then prove nothing was lost with np.array_equal(week2, small)
    print("TODO 4-6: rows, columns, max, and the int16 copy")
