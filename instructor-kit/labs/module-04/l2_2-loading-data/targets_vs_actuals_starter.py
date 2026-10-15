# --- lab bootstrap: find labs_paths.py (the same three lines open every lab; see labs/README.md) ---
import pathlib, sys
sys.path[:0] = [str(p) for p in pathlib.Path(globals().get("__file__", "lab.py")).resolve().parents if (p / "labs_paths.py").is_file()]
from labs_paths import DATA, OUTPUT
# %% [markdown]
# # Lab 2.2-C · Did the stores hit their targets? (STARTER)
# Question: which of the four stores beat its 2025 revenue target, and by how much?
# Both halves of the answer are in sales_2025.xlsx, on two sheets that need different options.
#
# Expected when you finish: the two sheet names, a 12-row monthly table with real column
# names (no "Unnamed"), a four-row result table sorted from best to worst, and a
# one-sheet workbook in your output folder that reads back with the same shape.

# %% Find the sheets (done for you)
import pandas as pd

BOOK = DATA / "sales_2025.xlsx"
print(pd.ExcelFile(BOOK).sheet_names)
print(pd.read_excel(BOOK, header=None, nrows=5).iloc[:, :3])     # the top of the first sheet, as it is

# %% Step 1: load each sheet with its own options
# TODO 1: monthly = pd.read_excel(BOOK, sheet_name="Monthly Sales", header=...)
#         (which row, counting from 0, holds Month, Boise, Bend, ...?)
#         targets = pd.read_excel(BOOK, sheet_name="Targets")
#         Print both shapes and monthly.columns.tolist().
monthly = None
targets = None

# %% Step 2: one row per store
# TODO 2: for each store name, compute
#           actual = monthly[store].sum()
#           target = targets.loc[targets["store"] == store, "target_revenue"].sum()
#         and append {"store": store, "actual": actual, "target": target} to `rows`.
#         Then result = pd.DataFrame(rows), add a column pct_of_target
#         (actual / target * 100, rounded to 1 decimal) and sort by it, largest first.
rows = []
result = None

# %% Step 3: hand it to a colleague
# TODO 3: result.to_excel(OUTPUT / "targets_vs_actuals.xlsx", sheet_name="2025", index=False)
#         Read it back with pd.read_excel and print its shape and columns.
if monthly is None or result is None:
    print("TODO 1-3 not done yet: `monthly` or `result` is still None.")
