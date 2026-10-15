# --- lab bootstrap: find labs_paths.py (the same three lines open every lab; see labs/README.md) ---
import pathlib, sys
sys.path[:0] = [str(p) for p in pathlib.Path(globals().get("__file__", "lab.py")).resolve().parents if (p / "labs_paths.py").is_file()]
from labs_paths import DATA
# %% [markdown]
# # Lab 2.3-A · The repair bench, second tent (STARTER)
# The Asheville store manager kept a hand-typed log of May 2025 (asheville_may_log.csv,
# next to this file). It has the same KINDS of damage as orders_messy.csv, but you have
# not been walked through this one. Audit it, write your own repair list, fix it in the
# lesson's order (structure, text, numbers, dates, missing values) and score the result.
#
# Expected when you finish: 31 rows with the columns
#   date, store, visitors, transactions, units, revenue, staff_on_duty, promo_day
# and the scorecard line "cells compared: 217 | still blank: 2 | wrong: 0".
# Stretch (TODO 6): use the TOTAL row to recover one of the two blanks honestly.

# %% Tools (done for you)
import pathlib

import pandas as pd

pd.set_option("display.width", 150)
pd.set_option("display.max_columns", 20)
LOG = pathlib.Path(globals().get("__file__", "lab.py")).resolve().parent / "asheville_may_log.csv"


def audit(df):
    """One row per column: its dtype, how many values are missing, how many are distinct."""
    return pd.DataFrame({"dtype": df.dtypes.astype(str), "missing": df.isna().sum(), "distinct": df.nunique()})


def score(clean):
    """Compare a cleaned log with the same 31 days of daily_sales.csv, cell by cell."""
    key = pd.read_csv(DATA / "daily_sales.csv", parse_dates=["date"])
    key = key[(key["store"] == "Asheville") & key["date"].between("2025-05-01", "2025-05-31")].set_index("date")
    need = ["date"] + key.columns.tolist()
    if clean.columns.tolist() != need or len(clean) != len(key) or clean["date"].isna().any():
        print("not ready to score: need 31 rows, no missing dates, and exactly these columns:", need)
        return
    mine = clean.set_index("date")
    blank = wrong = 0
    for col in key.columns:
        is_blank = mine[col].isna() & key[col].notna()
        match = (mine[col] == key[col]).fillna(False)
        blank += is_blank.sum()
        wrong += (~match & ~is_blank).sum()
    print(f"cells compared: {key.size} | still blank: {blank} | wrong: {wrong}")


# %% Step 0: audit before you touch anything (done for you: READ it)
raw = pd.read_csv(LOG)
print(raw.columns.tolist())
print(audit(raw))
print("rows:", len(raw), "| exact duplicate rows:", raw.duplicated().sum())
print(raw.tail(2))
# Write your repair list here before you fix anything:
#   1.
#   2.
#   3.

# %% Step 1: structure
# TODO 1: on a copy called `clean`: tidy the headers (.str.strip().str.lower()), then rename
#         them to the eight names in the header of this file (rename(columns={...})).
#         Save the number in the TOTAL row in `stated_total` (as a float), then drop that
#         row and the exact duplicates, and reset the index. You should have 31 rows.
clean = raw.copy()
stated_total = None

# %% Step 2: text
# TODO 2: print clean["store"].value_counts() first. Then strip, title-case, and fix the
#         one misspelling with .replace({...}).
#         promo_day is written yes / Yes / Y / YES / no / No / N: make it lowercase, keep the
#         first letter (.str[0]) and turn it into 1 and 0 with .map({"y": 1, "n": 0}).

# %% Step 3: numbers
# TODO 3: revenue: remove "$" and ",", then pd.to_numeric(..., errors="coerce").
#         Which value became NaN that was not empty? Print it BEFORE you convert.
#         Then look at revenue / transactions with .describe(): one day is about 100 times
#         too large. Divide only that row by 100 with a single .loc assignment.
#         visitors, transactions, units, staff_on_duty: whole numbers -> .astype("Int64").

# %% Step 4: dates
# TODO 4: three formats: 2025-05-01, 05/03/2025 and "May 5, 2025".
#         Parse once per format with errors="coerce" and combine with .fillna().

# %% Step 5: verify
# TODO 5: add three assert lines (31 rows, one store name, revenue between 0 and 20000
#         ignoring missing values), then let the scorecard run.
score(clean)

# %% Step 6 (stretch): a blank you CAN repair
# TODO 6: the TOTAL row is the sum of all 31 days. stated_total minus the sum of the
#         revenue you have is the one missing day. Fill it with .loc and score again.
