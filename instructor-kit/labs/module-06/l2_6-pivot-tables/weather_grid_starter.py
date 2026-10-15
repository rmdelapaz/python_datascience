# --- lab bootstrap: find labs_paths.py (the same three lines open every lab; see labs/README.md) ---
import pathlib, sys
sys.path[:0] = [str(p) for p in pathlib.Path(globals().get("__file__", "lab.py")).resolve().parents if (p / "labs_paths.py").is_file()]
from labs_paths import DATA
# %% [markdown]
# # Lab 2.6-C · pivot, pivot_table and the order of months (STARTER)
# Table: store_weather.csv, one row per city per day (2,924 rows; complete, no gaps).
# Questions:
#   1. On how many days was each city the warmest of the four?
#   2. What is the average daily high in each city in January, April, July and October?
#   3. What goes wrong when the months are names instead of numbers, and how do you fix it?
#
# Expected when you finish: a 731 x 4 grid with no empty cells, four counts that add up to
# 731, a month-by-city grid of average highs, the same grid with month NAMES in calendar
# order, and a melt that gets you back to 2,924 rows.

# %% Load (done for you)
import pandas as pd

pd.set_option("display.width", 150)
pd.set_option("display.max_columns", 20)

weather = pd.read_csv(DATA / "store_weather.csv", parse_dates=["date"])
print(weather.shape, weather.duplicated(["date", "city"]).sum())

# %% Step 1: rearrange only (one row per cell already, so pivot is enough)
# TODO 1: wide = weather.pivot(index="date", columns="city", values="high_f")
#         Print wide.shape and wide.isna().sum().sum().
wide = None

# %% Step 2: read across each row
# TODO 2: warmest = wide.idxmax(axis=1)     (the city with the highest value on each date)
#         Print warmest.value_counts(). Do the counts add up to the number of days?
warmest = None

# %% Step 3: summarize, then arrange
# TODO 3: add weather["month"] = weather["date"].dt.month, then
#         by_month = weather.pivot_table(index="month", columns="city", values="high_f", aggfunc="mean")
#         Print the rows for months 1, 4, 7 and 10, rounded to 1 decimal.
by_month = None

# %% Step 4: the month-name trap
# TODO 4: weather["month_name"] = weather["date"].dt.strftime("%b")      (Jan, Feb, ...)
#         Pivot again with index="month_name" and print the index: what order is it in?
#         Fix it with .reindex([...]) using the twelve names in calendar order.
named = None

# %% Step 5: and back again
# TODO 5: tidy = wide.reset_index().melt(id_vars="date", var_name="city", value_name="high_f")
#         How many rows?
tidy = None

# %% Report
if wide is None or warmest is None or by_month is None or named is None or tidy is None:
    print("TODOs not done yet: wide, warmest, by_month, named or tidy is still None.")
else:
    print(wide.shape, len(tidy), named.index.tolist()[:4])
