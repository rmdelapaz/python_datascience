# --- lab bootstrap: find labs_paths.py (the same three lines open every lab; see labs/README.md) ---
import pathlib, sys
sys.path[:0] = [str(p) for p in pathlib.Path(globals().get("__file__", "lab.py")).resolve().parents if (p / "labs_paths.py").is_file()]
from labs_paths import DATA

# %% [markdown]
# # Lab 0.1-A · How do Pinecrest customers pay? (SOLUTION)
# Reference answers. Hand out only after the lab.

# %% Load the orders
import pandas as pd

orders = pd.read_csv(DATA / "orders.csv", parse_dates=["order_date"])
print("Loaded", DATA.name + "/orders.csv")

# %% Step 1: how big is the table?
print(orders.shape)
print(orders.head(3))

# %% Step 2: count the payment methods
methods = orders["payment_method"].value_counts()
print("Payment methods:")
print(methods)

# %% Step 3: what share of orders used a digital wallet?
wallet_pct = round((orders["payment_method"] == "digital_wallet").mean() * 100, 1)
print("Digital wallet share (%):", wallet_pct)

# %% Step 4: filter to the gift-card orders
gift = orders[orders["payment_method"] == "gift_card"]
print("Gift-card orders:", len(gift))
print(f"Average gift-card order: ${gift['order_total'].mean():.2f}")

# %% Step 5: where is cash used?
cash = orders[orders["payment_method"] == "cash"]
print(cash["channel"].value_counts())
# Cash appears only in stores: all 1,614 cash orders have channel "store".
# A website cannot take cash, so this is what the data should look like.
print("Cash orders placed online:", (cash["channel"] == "online").sum())
