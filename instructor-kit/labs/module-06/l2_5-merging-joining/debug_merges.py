# --- lab bootstrap: find labs_paths.py (the same three lines open every lab; see labs/README.md) ---
import pathlib, sys
sys.path[:0] = [str(p) for p in pathlib.Path(globals().get("__file__", "lab.py")).resolve().parents if (p / "labs_paths.py").is_file()]
from labs_paths import DATA

# %% [markdown]
# # Find the bug · five broken merges (2.5)
# This file is broken ON PURPOSE. Three bugs stop the program: read the LAST line of the
# error, fix it, run again. Two bugs are QUIET: the merge runs and the number is wrong.
# Each result has a "should print" note. Count rows before and after every merge.

# %%
import pandas as pd

orders = pd.read_csv(DATA / "orders.csv", parse_dates=["order_date"])
customers = pd.read_csv(DATA / "customers.csv")
items = pd.read_csv(DATA / "order_items.csv")
products = pd.read_csv(DATA / "products.csv")
daily = pd.read_csv(DATA / "daily_sales.csv", parse_dates=["date"])
weather = pd.read_csv(DATA / "store_weather.csv", parse_dates=["date"])

# %% Bug 1 (stops the program): an id that was read as text
items_text = items.assign(order_id=items["order_id"].astype("str"))
lines = items_text.merge(orders[["order_id", "status"]], on="order_id", how="left")
print(len(lines))                                              # should print 45490

# %% Bug 2 (stops the program): sales with the weather attached
sales_weather = daily.merge(weather, on=["date", "store"], how="left")
print(len(sales_weather))                                      # should print 2903

# %% Bug 3 (stops the program): each line with its product's category
with_category = items.merge(products[["sku", "category"]], on="sku", how="left", validate="one_to_many")
print(len(with_category))                                      # should print 45490

# %% Bug 4 (quiet): total order value, after attaching each customer's loyalty tier
with_tier = orders.merge(customers[["customer_id", "loyalty_tier"]], on="customer_id")
print(round(with_tier["order_total"].sum(), 2))                # should print 3950701.45

# %% Bug 5 (quiet): the average order total
order_lines = orders.merge(items, on="order_id")
print(round(order_lines["order_total"].mean(), 2))             # should print 194.6
