# --- lab bootstrap: find labs_paths.py (the same three lines open every lab; see labs/README.md) ---
import pathlib, sys
sys.path[:0] = [str(p) for p in pathlib.Path(globals().get("__file__", "lab.py")).resolve().parents if (p / "labs_paths.py").is_file()]
from labs_paths import DATA
# %% [markdown]
# # Lab 2.4-B · What is in a basket? (SOLUTION)
# Table: order_items.csv, one row per product line on an order (45,490 lines).

# %% Load
import pandas as pd

pd.set_option("display.width", 150)
pd.set_option("display.max_columns", 20)
items = pd.read_csv(DATA / "order_items.csv")
items["line_total"] = items["quantity"] * items["unit_price"]
print(items.shape)

# %% Step 1: one row per order
baskets = items.groupby("order_id").agg(
    lines=("sku", "count"),
    units=("quantity", "sum"),
    subtotal=("line_total", "sum"),
)
print("orders:", len(baskets), "| lines add up:", baskets["lines"].sum() == len(items))
print(baskets.describe().round(2).loc[["mean", "50%", "max"]])
print(baskets["lines"].value_counts().sort_index().to_dict())

# %% Step 2: one row per product
by_sku = items.groupby("sku").agg(
    units=("quantity", "sum"),
    revenue=("line_total", "sum"),
    orders=("order_id", "nunique"),
)
print("products sold:", len(by_sku))
print(by_sku.nlargest(3, "units").round(2))
print(by_sku.nlargest(3, "revenue").round(2))

# %% Step 3: transform
items["order_subtotal"] = items.groupby("order_id")["line_total"].transform("sum")
items["share_of_order"] = items["line_total"] / items["order_subtotal"]
print(items[["order_id", "sku", "line_total", "order_subtotal", "share_of_order"]].head(4).round(3))
print("lines that are a whole order:", (items["share_of_order"] == 1).sum())

# %% Step 4: filter, two ways
big = items.groupby("order_id").filter(lambda g: len(g) >= 6)
items["lines_in_order"] = items.groupby("order_id")["sku"].transform("count")
big2 = items[items["lines_in_order"] >= 6]
print("filter       :", big.shape[0], "lines in", big["order_id"].nunique(), "orders")
print("transform+mask:", big2.shape[0], "lines in", big2["order_id"].nunique(), "orders")
print("same rows:", big.index.equals(big2.index))
