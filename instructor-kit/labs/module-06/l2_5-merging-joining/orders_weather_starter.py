# --- lab bootstrap: find labs_paths.py (the same three lines open every lab; see labs/README.md) ---
import pathlib, sys
sys.path[:0] = [str(p) for p in pathlib.Path(globals().get("__file__", "lab.py")).resolve().parents if (p / "labs_paths.py").is_file()]
from labs_paths import DATA
# %% [markdown]
# # Lab 2.5-B · Do account holders stay home when it rains? (STARTER)
# Question: on rainy days (at least 0.10 inch of precipitation), how many orders do signed-in
# customers place in each store, compared with dry days?
#
# Two tables, and their keys are awkward on purpose:
#   orders.csv         one row per ORDER      (order_date, store)   store can also be "Online"
#   store_weather.csv  one row per CITY-DAY   (date, city)
# Aggregate first, then merge on TWO columns whose names differ. And think hard about
# which table goes on the left: a day with no orders has no row in orders.csv at all.
#
# Expected when you finish: 2,924 rows after the merge, the number of store-days with no
# account-holder order, a four-row table (dry, rainy, change in percent), and two "average
# orders per store-day" figures that differ, with the reason.

# %% Load (done for you)
import pandas as pd

pd.set_option("display.width", 150)
pd.set_option("display.max_columns", 20)

orders = pd.read_csv(DATA / "orders.csv", parse_dates=["order_date"])
weather = pd.read_csv(DATA / "store_weather.csv", parse_dates=["date"])
print(orders.shape, weather.shape)

# %% Step 1: one row per store-day that has orders
# TODO 1: keep the in-store orders (channel == "store"), then
#         daily_orders = ....groupby(["order_date", "store"], as_index=False).agg(orders=("order_id", "count"))
#         How many rows? weather has 2,924. What does the difference mean?
daily_orders = None

# %% Step 2: merge on two differently named keys
# First try  weather.merge(daily_orders, on=["date", "store"])  in a scratch cell and read the error.
# My prediction: left table = ________  relationship = ________  rows after = ________
# TODO 2: merged = weather.merge(daily_orders, left_on=[..., ...], right_on=[..., ...],
#                                how=..., validate=..., indicator=True)
#         Print len(merged) and merged["_merge"].value_counts().
merged = None

# %% Step 3: a store-day with no order row had 0 orders
# TODO 3: merged["orders"] = merged["orders"].fillna(0)
#         merged["rainy"] = merged["precip_in"] >= 0.10

# %% Step 4: rainy against dry, for each city
# TODO 4: table = merged.groupby(["city", "rainy"])["orders"].mean().unstack("rainy")
#         Add change_pct = (table[True] / table[False] - 1) * 100, rounded to 1 decimal.
table = None

# %% Step 5: why the left table mattered
# TODO 5: compare merged["orders"].mean() with daily_orders["orders"].mean().
#         Which one is "average orders per store-day"? What did the other one leave out?
if daily_orders is None or merged is None or table is None:
    print("TODOs not done yet: daily_orders, merged or table is still None.")
else:
    print(table.round(2))
