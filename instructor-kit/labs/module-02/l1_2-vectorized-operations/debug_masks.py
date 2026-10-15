# --- lab bootstrap: find labs_paths.py (the same three lines open every lab; see labs/README.md) ---
import pathlib, sys
sys.path[:0] = [str(p) for p in pathlib.Path(globals().get("__file__", "lab.py")).resolve().parents if (p / "labs_paths.py").is_file()]
from labs_paths import DATA

# %% [markdown]
# # Handout 1.2 · Four mask bugs (find the bug)
# Blocks 1 and 2 stop with an error: read the LAST line of the traceback, fix, run again.
# Blocks 3 and 4 run and print a wrong answer, which is worse.
#
# Correct answers:
#     Block 1: 15 Boise store-days above $20,000
#     Block 2: 15 again (the same question, written the other way round)
#     Block 3: 6 store-days are in neither group
#     Block 4: revenue[0] is still 5017.07, and 101 values in `capped` equal 15000

# %%
import numpy as np


def load(col, dtype=float):
    """Read one column of daily_sales.csv into an array (the helper from Lesson 1.2)."""
    return np.genfromtxt(DATA / "daily_sales.csv", delimiter=",", skip_header=1, usecols=col, dtype=dtype)

stores = load(1, dtype=str)
revenue = load(5)

# %% Block 1
big_boise = (stores == "Boise") and (revenue > 20000)
print("Block 1:", big_boise.sum(), "Boise store-days above $20,000")

# %% Block 2
big_boise = revenue > 20000 & stores == "Boise"
print("Block 2:", big_boise.sum())

# %% Block 3: "every store-day is either above $7,000 or it is not"... so this should print 0
above = revenue > 7000
not_above = revenue <= 7000
print("Block 3:", revenue.size - above.sum() - not_above.sum(), "store-days are in neither group")
# Explain the number you get. Then count that group directly with ONE NumPy function.

# %% Block 4: cap a COPY at $15,000 and leave the real data alone
capped = revenue
capped[capped > 15000] = 15000
print("Block 4: revenue[0] is still", revenue[0], "and", (capped == 15000).sum(), "values in `capped` equal 15000")
print("         largest real revenue:", np.nanmax(revenue), " <- should be 27677.1")
