# --- lab bootstrap: find labs_paths.py (the same three lines open every lab; see labs/README.md) ---
import pathlib, sys
sys.path[:0] = [str(p) for p in pathlib.Path(globals().get("__file__", "lab.py")).resolve().parents if (p / "labs_paths.py").is_file()]
from labs_paths import DATA

# %% [markdown]
# # Lab 1.1-B · A what-if that must not touch the real data (SOLUTION)
# Reference answers. Hand out only after the lab.

# %% Load the units column and shape week 1. Column 4 is `units`.
import numpy as np

units = np.genfromtxt(DATA / "daily_sales.csv", delimiter=",", skip_header=1, usecols=4)
week1 = units[:28].reshape(7, 4).astype(np.int64)     # rows = Mon..Sun, columns = Asheville, Bend, Boise, Flagstaff
print(week1)
print("Bend, real total:", week1[:, 1].sum())

# %% Step 1: a column slice is a view
bend = week1[:, 1]
print("bend shares memory with week1:", np.shares_memory(week1, bend))     # True: writing to bend would change week1

# %% Step 2: an independent copy for the what-if
what_if = week1.copy()

# %% Step 3: add 10 units to Bend's column in the copy only
what_if[:, 1] = what_if[:, 1] + 10
print("Bend, what-if total:", what_if[:, 1].sum())      # 7 days x 10 more = 70 more
print("Bend, real total:   ", week1[:, 1].sum())

# %% Step 4: prove the two tables are separate
print("what_if shares memory with week1:", np.shares_memory(week1, what_if))

# %% Step 5: the integer trap
trap = week1[:, 1].copy()
trap[0] = 97.6                       # an int64 array keeps its dtype: the .6 is chopped, silently
print("stored 97.6, got:", trap[0], "| dtype:", trap.dtype)

fixed = week1[:, 1].astype(np.float64)      # astype returns a new float array
fixed[0] = 97.6
print("float version:", fixed[0], "| dtype:", fixed.dtype)
print("Bend, real total (still):", week1[:, 1].sum())
