# --- lab bootstrap: find labs_paths.py (the same three lines open every lab; see labs/README.md) ---
import pathlib, sys
sys.path[:0] = [str(p) for p in pathlib.Path(globals().get("__file__", "lab.py")).resolve().parents if (p / "labs_paths.py").is_file()]
from labs_paths import DATA

# %% [markdown]
# # Lab 1.1-A · A week of transactions (SOLUTION)
# Reference answers. Hand out only after the lab.

# %% Load one column. Column 3 is `transactions`.
import numpy as np

transactions = np.genfromtxt(DATA / "daily_sales.csv", delimiter=",", skip_header=1, usecols=3)
print("first eight values:", transactions[:8])

# %% Step 1: four facts every array knows about itself
print("shape:", transactions.shape, "| dtype:", transactions.dtype,
      "| ndim:", transactions.ndim, "| size:", transactions.size)

# %% Step 2: is anything missing?
missing = np.isnan(transactions).sum()
print("missing values:", missing)       # 0: only the revenue column has gaps

# %% Step 3: slice out the second week and give it a shape
week2 = transactions[28:56].reshape(7, 4)       # 7 days x 4 stores, a view of the same memory
print(week2)
print("shares memory with the full column:", np.shares_memory(week2, transactions))

# %% Step 4: rows, columns and one cell
print("Saturday, every store:", week2[5])
print("Bend, every day:      ", week2[:, 1])
print("Boise on Saturday:    ", week2[5, 2])

# %% Step 5: the busiest store-day
print("busiest store-day:", week2.max())

# %% Step 6: a smaller dtype
small = week2.astype(np.int16)                  # astype always builds a new array
print("float64:", week2.nbytes, "bytes | int16:", small.nbytes, "bytes")
print("same values:", np.array_equal(week2, small))
print("still a view of the column?", np.shares_memory(small, transactions))
