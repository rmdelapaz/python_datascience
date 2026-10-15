# --- lab bootstrap: find labs_paths.py (the same three lines open every lab; see labs/README.md) ---
import pathlib, sys
sys.path[:0] = [str(p) for p in pathlib.Path(globals().get("__file__", "lab.py")).resolve().parents if (p / "labs_paths.py").is_file()]
from labs_paths import DATA

# %% [markdown]
# # Handout 1.3 · Three shape bugs (find the bug)
# Block 1 raises an error. Blocks 2 and 3 run and print wrong answers.
# For each block: write the two shapes one above the other, right-aligned, BEFORE you fix it.
#
# Correct answers:
#     Block 1: every row of `centered` adds up to 0 (prints [0. 0. 0. 0. 0. 0. 0.])
#     Block 2: 7 gaps, and the largest gap is 6131.55
#     Block 3: [0. 0. 0. 0.]

# %% A week of revenue: 7 days x 4 stores
import numpy as np


def load(col, dtype=float):
    """Read one column of daily_sales.csv into an array (the helper from Lesson 1.2)."""
    return np.genfromtxt(DATA / "daily_sales.csv", delimiter=",", skip_header=1, usecols=col, dtype=dtype)

revenue = load(5)
week1 = revenue[:28].reshape(7, 4)

# %% Block 1: subtract each DAY's average from that day's row
centered = week1 - week1.mean(axis=1)
print("Block 1:", np.abs(centered.sum(axis=1)).round(2))

# %% Block 2: for each day, the gap between the best store and the worst store (7 numbers)
best = week1.max(axis=1)                       # shape (7,)
worst = week1.min(axis=1, keepdims=True)       # shape (7, 1)
gap = best - worst
print("Block 2:", gap.size, "gaps, and the largest gap is", gap.max().round(2))

# %% Block 3: the same centering as Block 1, on the first four days only
square = week1[:4]                             # 4 days x 4 stores
centered4 = square - square.mean(axis=1)
print("Block 3:", np.abs(centered4.sum(axis=1)).round(2))
# No error this time. Why not? What did NumPy subtract from what?
