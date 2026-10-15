# --- lab bootstrap: find labs_paths.py (the same three lines open every lab; see labs/README.md) ---
import pathlib, sys
sys.path[:0] = [str(p) for p in pathlib.Path(globals().get("__file__", "lab.py")).resolve().parents if (p / "labs_paths.py").is_file()]
from labs_paths import DATA

# %% [markdown]
# # Handout 1.1 · Three silent traps (find the bug)
# This script runs WITHOUT an error message and prints three wrong answers.
# That is the hard kind of bug. For each block: predict the right answer on paper,
# run it, then find the one line to change. Printing .dtype is the fastest clue.
#
# Correct answers:
#     Block 1: average price 48.5
#     Block 2: total stock 260
#     Block 3: Monday is still 148 (and the what-if Monday is 0)

# %% Block 1: the prices print with quotes around them, and prices.mean() raises an error
import numpy as np

prices = np.array([24.50, 39.00, "82.00", 48.50])
print("dtype:", prices.dtype)
print("average price:", prices[:2])          # should be: print("average price:", prices.mean())

# %% Block 2: adding two stock counts gives a negative number
on_shelf = np.array([100, 60], dtype=np.int8)
in_back = np.array([60, 40], dtype=np.int8)
total = on_shelf + in_back
print("total stock:", total.sum())

# %% Block 3: a what-if overwrote the real data
boise_week = np.array([148, 152, 90, 110, 131, 190, 160])
what_if = boise_week[:3]
what_if[0] = 0
print("Monday is still:", boise_week[0])
