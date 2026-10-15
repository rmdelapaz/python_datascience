# --- lab bootstrap: find labs_paths.py (the same three lines open every lab; see labs/README.md) ---
import pathlib, sys
sys.path[:0] = [str(p) for p in pathlib.Path(globals().get("__file__", "lab.py")).resolve().parents if (p / "labs_paths.py").is_file()]
from labs_paths import DATA

# %% [markdown]
# # Lab 1.1-B · A what-if that must not touch the real data (STARTER)
# A manager asks: "What would week 1 have looked like if Bend had sold 10 more units
# every day?" You will answer on a COPY, and prove the real numbers did not change.
# Along the way you will meet a view that changes the original, and an integer array
# that quietly drops a decimal.
#
# Expected when you finish: the real Bend total (868) printed three times, unchanged;
# a what-if Bend total of 938; True/False answers from np.shares_memory; and the
# line that shows 97.6 stored as 97.

# %% Load the units column and shape week 1 (done for you). Column 4 is `units`.
import numpy as np

units = np.genfromtxt(DATA / "daily_sales.csv", delimiter=",", skip_header=1, usecols=4)
week1 = units[:28].reshape(7, 4).astype(np.int64)     # rows = Mon..Sun, columns = Asheville, Bend, Boise, Flagstaff
print(week1)
print("Bend, real total:", week1[:, 1].sum())

# %% Step 1: predict first. Is a column slice a view or a copy?
bend = week1[:, 1]
# TODO 1: print np.shares_memory(week1, bend). Write your prediction here first: ______
print("TODO 1: does `bend` share memory with `week1`?")

# %% Step 2: make an independent copy of the whole table for the what-if
# TODO 2: what_if = ...        (one method call on week1)
what_if = None

# %% Step 3: add 10 units to Bend's column in the copy only
if what_if is None:
    print("TODO 2-4: `what_if` is still None")
else:
    # TODO 3: what_if[:, 1] = what_if[:, 1] + 10
    print("Bend, what-if total:", what_if[:, 1].sum())
    print("Bend, real total:   ", week1[:, 1].sum())
    # TODO 4: print np.shares_memory(week1, what_if)

# %% Step 5: the integer trap
# The manager changes her mind: "Use the regional Monday average for Bend on Monday instead: 97.6."
trap = week1[:, 1].copy()
# TODO 5: store 97.6 in trap[0], print trap[0] and trap.dtype. What happened to the .6?
#         Then fix it: make `fixed` a float64 copy with .astype(np.float64) and store 97.6 there.
print("TODO 5: store 97.6 in an int64 array and see what you get")
print("Bend, real total (still):", week1[:, 1].sum())
