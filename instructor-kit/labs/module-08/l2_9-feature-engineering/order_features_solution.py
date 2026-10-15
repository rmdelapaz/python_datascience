# --- lab bootstrap: find labs_paths.py (the same three lines open every lab; see labs/README.md) ---
import pathlib, sys
sys.path[:0] = [str(p) for p in pathlib.Path(globals().get("__file__", "lab.py")).resolve().parents if (p / "labs_paths.py").is_file()]
from labs_paths import DATA

# %% [markdown]
# # Lab 2.9-A · Which orders come back? An order-level feature table (SOLUTION)
# Unit of analysis: one row is an order.

# %% Load
import numpy as np
import pandas as pd

orders = pd.read_csv(DATA / "orders.csv", parse_dates=["order_date"])
items = pd.read_csv(DATA / "order_items.csv")
print("orders:", orders.shape, "| order lines:", items.shape)

# %% Step 1: the target and three derived columns
feat = orders[["order_id", "order_date", "channel", "status", "promo_code", "order_total"]].copy()
feat["returned"] = feat["status"] == "returned"
feat["is_online"] = feat["channel"] == "online"
feat["used_promo"] = feat["promo_code"].notna()
feat["is_weekend"] = feat["order_date"].dt.dayofweek >= 5

# %% Step 2: per-order aggregates from the order lines
items["is_footwear"] = items["sku"].str.startswith("FTW")
per_order = items.groupby("order_id").agg(
    n_lines=("sku", "count"),
    n_units=("quantity", "sum"),
    has_footwear=("is_footwear", "any"),
)
print("per_order rows:", len(per_order))

# %% Step 3: join back without losing or multiplying orders
before = len(feat)
feat = feat.merge(per_order, on="order_id", how="left", validate="one_to_one")
print("rows before and after the merge:", before, len(feat), "| orders with no lines:", int(feat["n_lines"].isna().sum()))

# %% Step 4: bins
feat["value_band"] = pd.qcut(feat["order_total"], q=4, labels=["low", "mid", "high", "top"])
feat["lines_band"] = pd.cut(feat["n_lines"], bins=[0, 1, 2, 4, 8], labels=["1", "2", "3-4", "5+"])
print("missing after binning:", int(feat["value_band"].isna().sum()), int(feat["lines_band"].isna().sum()))

# %% Step 5: does each feature separate returned from kept orders?
print("overall return rate:", round(feat["returned"].mean(), 4))
for col in ["is_online", "used_promo", "is_weekend", "has_footwear", "value_band", "lines_band"]:
    print(feat.groupby(col, observed=True)["returned"].agg(["mean", "size"]).round(3))

# %% Step 6: a feature made of two features
feat["online_footwear"] = feat["is_online"] & feat["has_footwear"]
print(feat.groupby("online_footwear")["returned"].agg(["mean", "size"]).round(3))
print(feat.groupby(["is_online", "has_footwear"])["returned"].agg(["mean", "size"]).round(3))

# %% Step 7: the leak question
print("TODO 7: `status` IS the answer. returned is computed from it, so a table that keeps status as a feature")
print("has the target written into it. Drop it (and anything else recorded after the order shipped).")
