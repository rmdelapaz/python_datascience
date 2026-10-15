# --- lab bootstrap: find labs_paths.py (the same three lines open every lab; see labs/README.md) ---
import pathlib, sys
sys.path[:0] = [str(p) for p in pathlib.Path(globals().get("__file__", "lab.py")).resolve().parents if (p / "labs_paths.py").is_file()]
from labs_paths import DATA
# %% [markdown]
# # Lab 2.4-A · For each store, for each kind of day (STARTER)
# Table: daily_sales.csv, one row per store per day (register totals for ALL in-store sales).
# Questions:
#   1. For each store: how many days, how much revenue, what share of visitors buy?
#   2. How much more does a promo day bring in, store by store?
#   3. The lesson says the register totals grew +19.7% in Flagstaff and fell 5.0% in
#      Asheville from 2024 to 2025. Check that claim.
#   4. On how many days did a store take in at least twice its own average?
#
# Expected when you finish: a four-row store table, a promo table with a "lift" column,
# a growth table sorted from best to worst, and a count per store for question 4.
# Before each TODO, say the SHAPE of the answer out loud: how many rows should come back?

# %% Load (done for you)
import pandas as pd

pd.set_option("display.width", 150)
pd.set_option("display.max_columns", 20)
sales = pd.read_csv(DATA / "daily_sales.csv", parse_dates=["date"])
print(sales.shape)

# %% Step 1: one row per store (named aggregation)
# TODO 1: by_store = sales.groupby("store").agg(
#             days=("date", "size"), days_with_revenue=("revenue", "count"),
#             revenue=("revenue", "sum"), visitors=("visitors", "sum"),
#             transactions=("transactions", "sum"))
#         Then add conversion = transactions / visitors (divide the SUMS, at the end).
#         Why are days and days_with_revenue different?
by_store = None

# %% Step 2: two keys, then unstack
# TODO 2: promo = sales.groupby(["store", "promo_day"])["revenue"].mean().unstack("promo_day")
#         Add a column lift = promo[1] / promo[0], rounded to 2 decimals.
#         Trap to check: sales.groupby("promo_day")["revenue"].mean() gives two numbers.
#         Is their average the average revenue of a store-day? Compare with sales["revenue"].mean().
promo = None

# %% Step 3: a key you compute on the spot
# TODO 3: year = sales["date"].dt.year.rename("year")
#         growth = sales.groupby(["store", year])["revenue"].sum().unstack("year")
#         Add growth_pct = (growth[2025] / growth[2024] - 1) * 100, rounded to 1 decimal,
#         and sort by it, largest first.
growth = None

# %% Step 4: transform (one value per original row)
# TODO 4: sales["store_avg"] = sales.groupby("store")["revenue"].transform("mean")
#         sales["vs_store_avg"] = sales["revenue"] / sales["store_avg"]
#         standout = sales[sales["vs_store_avg"] >= 2]
#         Print standout.groupby("store").size() and the share of standout days that were promo days.
standout = None

# %% Report
if by_store is None or promo is None or growth is None or standout is None:
    print("TODOs not done yet: by_store, promo, growth or standout is still None.")
else:
    print(by_store.round(3))
    print(promo.round(2))
    print(growth.round(0))
    print(standout.groupby("store").size())
