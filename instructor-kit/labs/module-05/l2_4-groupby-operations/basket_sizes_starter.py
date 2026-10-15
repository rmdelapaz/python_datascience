# --- lab bootstrap: find labs_paths.py (the same three lines open every lab; see labs/README.md) ---
import pathlib, sys
sys.path[:0] = [str(p) for p in pathlib.Path(globals().get("__file__", "lab.py")).resolve().parents if (p / "labs_paths.py").is_file()]
from labs_paths import DATA
# %% [markdown]
# # Lab 2.4-B · What is in a basket? (STARTER)
# Table: order_items.csv, one row per product line on an order (45,490 lines).
# Questions:
#   1. For each ORDER: how many lines, how many units, what merchandise subtotal?
#   2. For each SKU: units sold, revenue and number of orders. Are the best sellers by
#      units the same products as the best sellers by revenue?
#   3. What share of its order does each line represent? (transform)
#   4. Which orders have six or more lines? (filter, and the transform-then-mask twin)
#
# Expected when you finish: a 20,302-row order table summarized with describe(), two
# top-three lists that are NOT the same, the number of lines that are a whole order by
# themselves, and two ways of finding the big baskets that give equal results.

# %% Load (done for you)
import pandas as pd

pd.set_option("display.width", 150)
pd.set_option("display.max_columns", 20)
items = pd.read_csv(DATA / "order_items.csv")
items["line_total"] = items["quantity"] * items["unit_price"]
print(items.shape)

# %% Step 1: one row per order
# TODO 1: baskets = items.groupby("order_id").agg(lines=..., units=..., subtotal=...)
#         lines: count the "sku" column; units: sum of "quantity"; subtotal: sum of "line_total".
#         How many rows should come back? Print len(baskets) and baskets.describe().round(2).
baskets = None

# %% Step 2: one row per product
# TODO 2: by_sku = items.groupby("sku").agg(units=..., revenue=..., orders=("order_id", "nunique"))
#         Print by_sku.nlargest(3, "units") and by_sku.nlargest(3, "revenue").
by_sku = None

# %% Step 3: transform
# TODO 3: items["order_subtotal"] = items.groupby("order_id")["line_total"].transform("sum")
#         items["share_of_order"] = items["line_total"] / items["order_subtotal"]
#         How many lines have a share of exactly 1? What kind of order are they?

# %% Step 4: filter, two ways
# TODO 4: big = items.groupby("order_id").filter(lambda g: len(g) >= 6)
#         Then the same rows without a function per group:
#         items["lines_in_order"] = items.groupby("order_id")["sku"].transform("count")
#         big2 = items[items["lines_in_order"] >= 6]
#         Compare big.shape with big2.shape and count the distinct orders.
big = None

# %% Report
if baskets is None or by_sku is None or big is None:
    print("TODOs not done yet: baskets, by_sku or big is still None.")
else:
    print(len(baskets), len(by_sku), big.shape)
