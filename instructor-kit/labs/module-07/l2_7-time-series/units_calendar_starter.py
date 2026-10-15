# --- lab bootstrap: find labs_paths.py (the same three lines open every lab; see labs/README.md) ---
import pathlib, sys
sys.path[:0] = [str(p) for p in pathlib.Path(globals().get("__file__", "lab.py")).resolve().parents if (p / "labs_paths.py").is_file()]
from labs_paths import DATA

# %% [markdown]
# # Lab 2.7-A · An honest weekly calendar (STARTER)
# Bend's manager wants unit sales by week, with no misleading weeks in the table.
# Questions: Which of Bend's weekly totals are built from fewer than 7 days?
#            What was Bend's best COMPLETE week?
#            What does the week-over-week change look like around the incomplete week?
#
# Expected when you finish:
#   - 4 dates on which every store was closed, and a count of missing days per store
#   - a short table of Bend's incomplete weeks (2 rows)
#   - one line naming the best complete week and its units
#   - 4 week-over-week changes for August 2024, two of them created by the gap

# %% Load with real dates and go wide: one row per day, one column per store (done for you)
import pandas as pd

daily = pd.read_csv(DATA / "daily_sales.csv", parse_dates=["date"])
units = daily.pivot(index="date", columns="store", values="units")
print("rows:", len(units), "| index type:", type(units.index).__name__)

# %% Step 1: compare with the full calendar
# TODO 1: build `calendar` with pd.date_range from the first to the last date, one entry per day.
#         Then `closed_days` = the calendar dates that are NOT in units.index (use .difference).
calendar = None
closed_days = None

if closed_days is None:
    print("TODO 1 not done yet: `closed_days` is still None.")
else:
    print("days in the calendar:", len(calendar))
    print("closed on:", [str(d.date()) for d in closed_days])

# %% Step 2: one row for every calendar day
# TODO 2: give `units` a row for every day with .asfreq("D") and store it in `full`.
#         Print full.isna().sum() to see how many days each store is missing.
full = None

if full is None:
    print("TODO 2 not done yet: `full` is still None.")
else:
    print(full.isna().sum().to_string())

# %% Step 3: decide what each gap means
# A closed store sold 0 units: that is a fact. An export that failed is unknown: leave it NaN.
# TODO 3: set the closed days to 0 for every store:  full.loc[closed_days] = 0
#         Then print full.isna().sum() again. Only the unknown days should be left.

# %% Step 4: weekly totals for Bend, with the day count beside each total
# TODO 4: weekly = full["Bend"].resample("W").agg(["sum", "count"])
#         incomplete = the rows of `weekly` where count is less than 7
weekly = None
incomplete = None

if weekly is None:
    print("TODO 4 not done yet: `weekly` is still None.")
else:
    print(incomplete)

# %% Step 5: the best complete week, and the change around the gap
# TODO 5: keep only the weeks with count == 7, then use .idxmax() and .max() on their "sum".
# TODO 6: print weekly["sum"].diff() for the weeks ending 2024-08-04 to 2024-08-25.
#         Which two of those four changes would you NOT report as real?
if weekly is not None:
    print("TODO 5 and 6: write your code here.")
