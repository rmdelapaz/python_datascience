# --- lab bootstrap: find labs_paths.py (the same three lines open every lab; see labs/README.md) ---
import pathlib, sys
sys.path[:0] = [str(p) for p in pathlib.Path(globals().get("__file__", "lab.py")).resolve().parents if (p / "labs_paths.py").is_file()]
from labs_paths import DATA
# %% [markdown]
# # Lab 2.5-B · Do account holders stay home when it rains? (SOLUTION)
# Aggregate first, merge on two differently named keys, and start from the table that
# has a row for EVERY store-day.

# %% Load
import pandas as pd

pd.set_option("display.width", 150)
pd.set_option("display.max_columns", 20)

orders = pd.read_csv(DATA / "orders.csv", parse_dates=["order_date"])
weather = pd.read_csv(DATA / "store_weather.csv", parse_dates=["date"])
print(orders.shape, weather.shape)

# %% Step 1: one row per store-day that has orders
in_store = orders[orders["channel"] == "store"]
daily_orders = in_store.groupby(["order_date", "store"], as_index=False).agg(orders=("order_id", "count"))
print("store-days with at least one order:", len(daily_orders), "of", len(weather))

# %% Step 2: merge on two differently named keys
# left table = weather (it has every store-day), relationship = one-to-one, rows after = 2,924
merged = weather.merge(daily_orders, left_on=["date", "city"], right_on=["order_date", "store"],
                       how="left", validate="one_to_one", indicator=True)
print(len(weather), "->", len(merged))
print(merged["_merge"].value_counts().to_dict())

# %% Step 3: a store-day with no order row had 0 orders
merged["orders"] = merged["orders"].fillna(0)
merged["rainy"] = merged["precip_in"] >= 0.10
print("store-days with no account-holder order, by city:",
      merged[merged["_merge"] == "left_only"].groupby("city").size().to_dict())

# %% Step 4: rainy against dry, for each city
table = merged.groupby(["city", "rainy"])["orders"].mean().unstack("rainy")
table["change_pct"] = ((table[True] / table[False] - 1) * 100).round(1)
print(table.round(2))

# %% Step 5: why the left table mattered
print("average orders per store-day (every day counted):", round(merged["orders"].mean(), 2))
print("average over days that had an order row only    :", round(daily_orders["orders"].mean(), 2))
print("orders in the merged table:", int(merged["orders"].sum()), "| in-store orders:", len(in_store))
