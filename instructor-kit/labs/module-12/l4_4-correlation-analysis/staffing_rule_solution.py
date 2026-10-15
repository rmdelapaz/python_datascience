# --- lab bootstrap: find labs_paths.py (the same three lines open every lab; see labs/README.md) ---
import pathlib, sys
sys.path[:0] = [str(p) for p in pathlib.Path(globals().get("__file__", "lab.py")).resolve().parents if (p / "labs_paths.py").is_file()]
from labs_paths import DATA

# %% [markdown]
# # Lab 4.4-B · Recover the staffing rule (SOLUTION)
# Managers schedule staff in advance from the traffic they expect. Can a regression line
# recover their rule of thumb from the data? Fit it, read every number in the units of the
# data, use it carefully, and see why the same data gives a different line the other way round.

# %% Load the store-days
import numpy as np
import pandas as pd
from scipy import stats

daily = pd.read_csv(DATA / "daily_sales.csv", parse_dates=["date"])
x, y = daily["visitors"], daily["staff_on_duty"]
print("store-days:", len(daily), "| visitors", x.min(), "to", x.max(), "| staff", y.min(), "to", y.max())

# %% Step 1: the line, staff predicted from visitors
fit = stats.linregress(x, y)
print("slope    :", round(fit.slope, 4), "staff per visitor")
print("         =", round(fit.slope * 100, 2), "staff per 100 visitors")
print("intercept:", round(fit.intercept, 2))
print("r        :", round(fit.rvalue, 3), "| r squared:", round(fit.rvalue ** 2, 3))

# %% Step 2: use it, with its typical miss
leftover = y - (fit.intercept + fit.slope * x)
print("predicted staff for a 400-visitor day:", round(fit.intercept + fit.slope * 400, 1))
print("typical miss (SD of the residuals)   :", round(leftover.std(), 2), "staff")

# %% Step 3: one rule for every store?
for store, g in daily.groupby("store"):
    f = stats.linregress(g["visitors"], g["staff_on_duty"])
    print(f"{store:<10} slope per 100 visitors {f.slope * 100:5.2f}   intercept {f.intercept:5.2f}")

# %% Step 4: the other way round gives a different line, with the same r
back = stats.linregress(y, x)
print("visitors predicted from staff: slope", round(back.slope, 1), "visitors per staff member")
print("1 / (staff per visitor)      :", round(1 / fit.slope, 1), " (not the same line)")
print("r both ways:", round(fit.rvalue, 3), round(back.rvalue, 3))

# %% Step 5: what the line does not say
print("The slope describes how staffing differs across days with different traffic:")
print("about 1.6 more staff per 100 extra visitors, the same in all four stores.")
print("It does not say that adding staff brings visitors: managers set staff FROM")
print("expected visitors. And it says nothing about a 3,000-visitor day (outside 125-1164).")
