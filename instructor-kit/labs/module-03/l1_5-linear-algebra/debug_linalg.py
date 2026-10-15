# --- lab bootstrap: find labs_paths.py (the same three lines open every lab; see labs/README.md) ---
import pathlib, sys
sys.path[:0] = [str(p) for p in pathlib.Path(globals().get("__file__", "lab.py")).resolve().parents if (p / "labs_paths.py").is_file()]
from labs_paths import DATA

# %% [markdown]
# # Handout 1.5 · Four linear algebra bugs (find the bug)
# Block 1 runs and gives the wrong SHAPE. Block 2 raises an error. Blocks 3 and 4 run and
# give wrong NUMBERS. Print shapes before you change anything.
#
# Correct answers:
#     Block 1: three order totals: [756.35 348.95 356.3 ]
#     Block 2: revenue under each price list: [1461.6  1242.41]
#     Block 3: a slope near 21.39 (not nan)
#     Block 4: an intercept and a slope, about -238.85 and 21.39

# %%
import numpy as np


def load(col, dtype=float):
    """Read one column of daily_sales.csv into an array (the helper from Lesson 1.2)."""
    return np.genfromtxt(DATA / "daily_sales.csv", delimiter=",", skip_header=1, usecols=col, dtype=dtype)


orders = np.array([[2, 1, 3],
                   [1, 0, 2],
                   [0, 4, 1]])
prices = np.array([299.95, 82.95, 24.50])
price_lists = np.array([[299.95, 254.96],
                        [ 82.95,  70.51],
                        [ 24.50,  20.83]])

# %% Block 1: the total of each order
totals = orders * prices
print("Block 1:", totals.shape)
print(totals)

# %% Block 2: revenue under each price list, from the units sold of each product
units_sold = orders.sum(axis=0)                 # shape (3,)
print("Block 2:", price_lists @ units_sold)

# %% Block 3: Boise, revenue against visitors
stores = load(1, dtype=str)
visitors, revenue = load(2), load(5)
boise = stores == "Boise"
A = np.column_stack([np.ones(boise.sum()), visitors[boise]])
coef, *_ = np.linalg.lstsq(A, revenue[boise])
print("Block 3:", coef)

# %% Block 4: the same fit on the complete days. Where is the intercept?
keep = boise & ~np.isnan(revenue)
A = visitors[keep].reshape(-1, 1)
coef, *_ = np.linalg.lstsq(A, revenue[keep])
print("Block 4:", coef)
