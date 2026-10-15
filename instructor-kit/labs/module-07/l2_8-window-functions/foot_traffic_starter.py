# --- lab bootstrap: find labs_paths.py (the same three lines open every lab; see labs/README.md) ---
import pathlib, sys
sys.path[:0] = [str(p) for p in pathlib.Path(globals().get("__file__", "lab.py")).resolve().parents if (p / "labs_paths.py").is_file()]
from labs_paths import DATA

# %% [markdown]
# # Lab 2.8-A · Foot traffic: when did Flagstaff pass Bend? (STARTER)
# The door counters give visitors per store per day. Daily counts zigzag with the week, so the
# question needs a smoother.
# Questions: On the 28-day average, when did Flagstaff first have more visitors than Bend?
#            From which date has Flagstaff stayed ahead?
#            How many times did Flagstaff set a new single-day visitor record?
#            Which 7 consecutive days were each store's busiest?
#
# Expected when you finish:
#   - the first 8 rows of Boise's 7-day average (6 NaN, then 2 numbers)
#   - the 28-day averages of all four stores on four dates
#   - three lines about Flagstaff and Bend: first day ahead, days ahead in total, ahead for good since
#   - the number of record days and the last three records
#   - four lines: each store's busiest 7 days

# %% The clean calendar from Lesson 2.7, this time for visitors (done for you)
import pandas as pd

daily = pd.read_csv(DATA / "daily_sales.csv", parse_dates=["date"])
visitors = daily.pivot(index="date", columns="store", values="visitors")
calendar = pd.date_range(visitors.index.min(), visitors.index.max(), freq="D")
closed_days = calendar.difference(visitors.index)
visitors = visitors.asfreq("D")
visitors.loc[closed_days] = 0            # closed: nobody came in. Failed exports stay NaN.
print(visitors.shape, "| unknown store-days:", int(visitors.isna().sum().sum()))

# %% Step 1: a 7-day rolling mean
# TODO 1: avg7 = visitors.rolling(7).mean()
#         Print the first 8 rows of the Boise column, rounded to 1 decimal. Why are 6 of them NaN?
avg7 = None

if avg7 is None:
    print("TODO 1 not done yet: `avg7` is still None.")

# %% Step 2: a 28-day rolling mean that survives a few unknown days
# TODO 2: avg28 = visitors.rolling(28, min_periods=21).mean()
#         Print it, rounded to 0 decimals, for these four dates:
check_dates = ["2024-06-30", "2024-12-31", "2025-06-30", "2025-12-31"]
avg28 = None

if avg28 is None:
    print("TODO 2 not done yet: `avg28` is still None.")

# %% Step 3: the crossover
# TODO 3: ahead = avg28["Flagstaff"] > avg28["Bend"]        (a True/False Series)
#         a) the first date on which it is True:   ahead[ahead].index[0]
#         b) how many days it is True:             ahead.sum()
#         c) the last date on which Bend was ahead: keep the rows where avg28 has a value and
#            `ahead` is False, and take the last index label. Flagstaff leads from the next day.
if avg28 is not None:
    print("TODO 3: write your code here.")

# %% Step 4: record days
# TODO 4: flag = visitors["Flagstaff"]; a day is a record when flag == flag.cummax().
#         Print how many records there are, and the last three.

# %% Step 5: each store's busiest 7 consecutive days
# TODO 5: sum7 = visitors.rolling(7).sum(); for each store print the END date (.idxmax())
#         and the total (.max()). A rolling sum finds the best stretch wherever it starts.
print("Expected at the end: four lines, one per store, each naming the end date of its busiest 7 days.")
