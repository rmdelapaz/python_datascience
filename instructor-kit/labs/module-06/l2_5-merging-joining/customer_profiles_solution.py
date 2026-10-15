# --- lab bootstrap: find labs_paths.py (the same three lines open every lab; see labs/README.md) ---
import pathlib, sys
sys.path[:0] = [str(p) for p in pathlib.Path(globals().get("__file__", "lab.py")).resolve().parents if (p / "labs_paths.py").is_file()]
from labs_paths import DATA
# %% [markdown]
# # Lab 2.5-A · One row per customer, with names (SOLUTION)
# Aggregate each table to the level you need, then merge. Count before, count after.

# %% Load
import pandas as pd

pd.set_option("display.width", 150)
pd.set_option("display.max_columns", 20)

orders = pd.read_csv(DATA / "orders.csv", parse_dates=["order_date"])
customers = pd.read_csv(DATA / "customers.csv")
print(len(orders), "orders |", len(customers), "customer accounts")

# %% Step 1: aggregate first (one row per customer id that has orders)
summary = orders.groupby("customer_id", as_index=False).agg(
    orders=("order_id", "count"),
    spend=("order_total", "sum"),
    last_order=("order_date", "max"),
)
print("summary rows:", len(summary), "| key unique in summary:", summary["customer_id"].is_unique,
      "| in customers:", customers["customer_id"].is_unique)

# %% Step 2: attach the summary to the accounts
# left table = customers, relationship = one-to-one, rows after = 4,850
profiles = customers.merge(summary, on="customer_id", how="left", validate="one_to_one", indicator=True)
print(len(customers), "->", len(profiles))
print(profiles["_merge"].value_counts().to_dict())

# %% Step 3: no orders means 0 orders
profiles["orders"] = profiles["orders"].fillna(0).astype("int64")
profiles["spend"] = profiles["spend"].fillna(0.0)
profiles["never_ordered"] = profiles["_merge"] == "left_only"
print(profiles.nlargest(5, "spend")[["first_name", "last_name", "state", "loyalty_tier", "orders", "spend"]])

# %% Step 4: one row per tier
by_tier = profiles.groupby("loyalty_tier").agg(
    accounts=("customer_id", "count"),
    never_ordered=("never_ordered", "mean"),
    avg_spend=("spend", "mean"),
)
print(by_tier.round(3))
print("accounts add up:", by_tier["accounts"].sum() == len(customers))

# %% Step 5: audit the other side
audit = customers[["customer_id"]].merge(summary, on="customer_id", how="outer", indicator=True)
print(audit["_merge"].value_counts().to_dict())
no_account = audit[audit["_merge"] == "right_only"]
print(f"ids with orders but no account: {len(no_account)} | their orders: {int(no_account['orders'].sum())}"
      f" | their spend: ${no_account['spend'].sum():,.2f}")
print(f"spend that reached the profiles table: ${profiles['spend'].sum():,.2f}"
      f" of ${orders['order_total'].sum():,.2f}")
