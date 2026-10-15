# --- lab bootstrap: find labs_paths.py (the same three lines open every lab; see labs/README.md) ---
import pathlib, sys
sys.path[:0] = [str(p) for p in pathlib.Path(globals().get("__file__", "lab.py")).resolve().parents if (p / "labs_paths.py").is_file()]
from labs_paths import DATA
# %% [markdown]
# # Lab 2.2-A · Brief the interpreter (STARTER)
# Question: the till system exported one week of store sales in its own dialect
# (till_export_week08.txt, next to this file). Load it so that every column has the
# right dtype, then prove the load is right by matching it against daily_sales.csv.
#
# Expected when you finish: dtypes with a datetime64 date and a float64 revenue,
# 28 rows, exactly 1 missing revenue (which store, which day?), and "totals match: True".

# %% Look at the raw text first (done for you)
import pathlib

import numpy as np
import pandas as pd

EXPORT = pathlib.Path(globals().get("__file__", "lab.py")).resolve().parent / "till_export_week08.txt"
with open(EXPORT, encoding="utf-8") as f:
    for _ in range(6):
        print(f.readline().rstrip())

# %% Step 1: read it with no options and see what goes wrong
naive = pd.read_csv(EXPORT)
print(naive.shape, naive.columns.tolist())

# %% Step 2: brief the reader
# TODO 1: write the read_csv call. Decide each option from the six lines printed above:
#   sep=...          what separates the values?
#   skiprows=...     how many lines of notes sit above the header?
#   decimal=..., thousands=...   how is 3.536,91 written?
#   na_values=[...]  how does this file say "missing"?
#   parse_dates=["date"], date_format=...   17.02.2025 is day.month.year: "%d.%m.%Y"
week = None

# %% Step 3: check the translation
# TODO 2: print week.dtypes and week.shape, then the row(s) where revenue is missing.

# %% Step 4: prove it against the clean file
# TODO 3: load daily_sales.csv with parse_dates=["date"], keep the rows whose date is
#         .between("2025-02-17", "2025-02-23"), and compare the two revenue totals with
#         np.isclose(a, b). Also compare the visitors totals with ==.
if week is None:
    print("TODO 1-3 not done yet: `week` is still None.")
