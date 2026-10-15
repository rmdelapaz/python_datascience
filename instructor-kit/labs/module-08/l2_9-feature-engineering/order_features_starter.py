# --- lab bootstrap: find labs_paths.py (the same three lines open every lab; see labs/README.md) ---
import pathlib, sys
sys.path[:0] = [str(p) for p in pathlib.Path(globals().get("__file__", "lab.py")).resolve().parents if (p / "labs_paths.py").is_file()]
from labs_paths import DATA

# %% [markdown]
# # Lab 2.9-A · Which orders come back? An order-level feature table (STARTER)
# The returns desk asks: "Which kinds of orders get returned?"
# Unit of analysis: ONE ROW IS AN ORDER. Every feature must be a fact about that order.
#
# Expected when you finish:
#   - a feature table with exactly 20,302 rows (one per order), before and after the merge
#   - the overall return rate (about 5.6%)
#   - a small table per feature: return rate and group size
#   - the one combination that stands out: online orders that contain footwear
#   - one sentence naming a column that must NOT be used as a feature, and why

# %% Load (done for you)
import numpy as np
import pandas as pd

orders = pd.read_csv(DATA / "orders.csv", parse_dates=["order_date"])
items = pd.read_csv(DATA / "order_items.csv")
print("orders:", orders.shape, "| order lines:", items.shape)

# %% Step 1: the target and three derived columns (flags and a date part)
feat = orders[["order_id", "order_date", "channel", "status", "promo_code", "order_total"]].copy()
feat["returned"] = feat["status"] == "returned"          # the target: what we want to explain

# TODO 1: add three True/False columns to `feat`:
#   is_online   the channel is "online"
#   used_promo  promo_code is not missing            (.notna())
#   is_weekend  the order was placed on a Saturday or Sunday   (.dt.dayofweek >= 5)

# %% Step 2: per-order aggregates from the order lines
# The category of a line is in its SKU prefix: "FTW-1004" is Footwear.
items["is_footwear"] = items["sku"].str.startswith("FTW")

# TODO 2: group `items` by order_id and build `per_order` with named aggregations:
#   n_lines       = ("sku", "count")
#   n_units       = ("quantity", "sum")
#   has_footwear  = ("is_footwear", "any")
per_order = None

# %% Step 3: join back WITHOUT losing or multiplying orders
# TODO 3: left-merge `per_order` onto `feat` on order_id, with validate="one_to_one".
#         Print len(feat) before and after: both must be 20302.
if per_order is None:
    print("TODO 2 and 3 not done yet: `per_order` is still None.")

# %% Step 4: bins
# TODO 4: value_band = pd.qcut of order_total into 4 equal-sized groups, labels ["low", "mid", "high", "top"]
#         lines_band = pd.cut of n_lines with bins=[0, 1, 2, 4, 8] and labels ["1", "2", "3-4", "5+"]
#         Check that neither new column has missing values.

# %% Step 5: does each feature separate returned from kept orders?
# TODO 5: for each feature, print the return rate AND the group size:
#         feat.groupby("is_online")["returned"].agg(["mean", "size"])
#         Do the same for used_promo, is_weekend, has_footwear, value_band and lines_band.
print("overall return rate:", round(feat["returned"].mean(), 4))

# %% Step 6: a feature made of two features
# TODO 6: feat["online_footwear"] = feat["is_online"] & feat["has_footwear"]
#         Print its return rate and size. Then group by BOTH is_online and has_footwear.

# %% Step 7: the leak question
# TODO 7: `status` is still in the table. Why must it never be used as a feature for "will this order be returned"?
print("My answer to TODO 7: (write it here)")
