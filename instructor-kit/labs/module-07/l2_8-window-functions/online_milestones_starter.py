# --- lab bootstrap: find labs_paths.py (the same three lines open every lab; see labs/README.md) ---
import pathlib, sys
sys.path[:0] = [str(p) for p in pathlib.Path(globals().get("__file__", "lab.py")).resolve().parents if (p / "labs_paths.py").is_file()]
from labs_paths import DATA

# %% [markdown]
# # Lab 2.8-B · The online shop: milestones, ranks and a fair baseline (STARTER)
# Questions: On what date did completed online revenue pass $1,000,000 in each year?
#            Where does each month rank within its own year?
#            How many times did the shop set a new best day?
#            How unusual was the best day ever (2025-06-24), judged ONLY by what was known that morning?
#
# Expected when you finish:
#   - two lines with the million-dollar dates (one per year)
#   - a 24-row table of monthly revenue and each month's rank within its year
#   - the number of record days and the last three
#   - the best day's revenue against its leak-free baseline, and against a leaky one
#   - how many days were at least 2 times their baseline: honest count and leaky count

# %% One number per calendar day (done for you)
import pandas as pd

orders = pd.read_csv(DATA / "orders.csv", parse_dates=["order_date"])
done = orders[(orders["channel"] == "online") & (orders["status"] == "completed")]
day = done.resample("D", on="order_date")["order_total"].sum()
print("days:", len(day), "| days with no revenue:", int((day == 0).sum()), "| total:", round(day.sum(), 2))

# %% Step 1: year to date
# TODO 1: ytd = day.groupby(day.index.year).cumsum()       (the running total restarts each January 1)
#         For 2024 and for 2025, print the first date on which ytd is at least 1_000_000.
ytd = None

if ytd is None:
    print("TODO 1 not done yet: `ytd` is still None.")

# %% Step 2: rank the months inside each year
# TODO 2: month = day.resample("ME").sum()
#         rank = month.groupby(month.index.year).rank(ascending=False)     (1 = best month of ITS year)
#         Print the two side by side. Which month is number 1 in both years? Number 12?
month = None

if month is None:
    print("TODO 2 not done yet: `month` is still None.")

# %% Step 3: record days
# TODO 3: a day is a record when day == day.cummax(). Print how many, and the last three.

# %% Step 4: a baseline that cannot see the day it judges
# "Normal for a Tuesday" = the mean of the 4 Tuesdays BEFORE it.
# TODO 4: baseline = day.groupby(day.index.dayofweek).transform(lambda s: s.shift(1).rolling(4).mean())
#         Print day, baseline and day / baseline for "2025-06-24" (the record day from Step 3).
# TODO 5: build `leaky` the same way but WITHOUT shift(1). Print the same three numbers.
#         Then count the days with day / baseline >= 2, and the days with day / leaky >= 2.
#         Why does the leaky version find so few unusual days?
print("Expected at the end: the record day against two baselines, and two counts of 'unusual' days.")
