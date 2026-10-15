# --- lab bootstrap: find labs_paths.py (the same three lines open every lab; see labs/README.md) ---
import pathlib, sys
sys.path[:0] = [str(p) for p in pathlib.Path(globals().get("__file__", "lab.py")).resolve().parents if (p / "labs_paths.py").is_file()]
from labs_paths import DATA

# %% [markdown]
# # Lab 2.7-A · An honest weekly calendar (SOLUTION)
# Bend's manager wants unit sales by week, with no misleading weeks in the table.

# %% Load with real dates and go wide
import pandas as pd

daily = pd.read_csv(DATA / "daily_sales.csv", parse_dates=["date"])
units = daily.pivot(index="date", columns="store", values="units")
print("rows:", len(units), "| index type:", type(units.index).__name__)

# %% Step 1: compare with the full calendar
calendar = pd.date_range(units.index.min(), units.index.max(), freq="D")
closed_days = calendar.difference(units.index)
print("days in the calendar:", len(calendar))
print("closed on:", [str(d.date()) for d in closed_days])

# %% Step 2: one row for every calendar day
full = units.asfreq("D")
print("missing days per store after asfreq:")
print(full.isna().sum().to_string())

# %% Step 3: a closed day is a true 0; a failed export stays unknown
full.loc[closed_days] = 0
print("still unknown after zeroing the closed days:")
print(full.isna().sum().to_string())

# %% Step 4: weekly totals for Bend with the day count beside each total
weekly = full["Bend"].resample("W").agg(["sum", "count"])
incomplete = weekly[weekly["count"] < 7]
print("Bend weeks built from fewer than 7 days:")
print(incomplete)

# %% Step 5: best complete week, and the change around the gap
complete = weekly[weekly["count"] == 7]
best = complete["sum"].idxmax()
print(f"best complete week: ends {best.date()} ({best.day_name()}), {complete['sum'].max():.0f} units")

change = weekly["sum"].diff()
print("week-over-week change in units, August 2024:")
print(change.loc["2024-08-04":"2024-08-25"].to_string())
print("The -542 and the +443 are the gap, not the customers: the week ending 2024-08-18 has only 4 days.")
