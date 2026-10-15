# --- lab bootstrap: find labs_paths.py (the same three lines open every lab; see labs/README.md) ---
import pathlib, sys
sys.path[:0] = [str(p) for p in pathlib.Path(globals().get("__file__", "lab.py")).resolve().parents if (p / "labs_paths.py").is_file()]
from labs_paths import DATA

# %% [markdown]
# # Lab 0.1-A · How do Pinecrest customers pay? (STARTER)
# The same three pandas moves as the lesson (read a file, pick a column, count and filter),
# aimed at a new question: which payment methods do customers use, and is one of them
# special in some way?
#
# Expected when you finish: the table size, four payment methods with their counts,
# the percentage of orders paid by digital wallet, the number and average size of
# gift-card orders, and one sentence about where cash is used.

# %% Load the orders (done for you)
import pandas as pd

orders = pd.read_csv(DATA / "orders.csv", parse_dates=["order_date"])
print("Loaded", DATA.name + "/orders.csv")

# %% Step 1: how big is the table?
# TODO 1: print orders.shape, then the first three rows with orders.head(3)
print("TODO 1: print the shape and the first three rows")

# %% Step 2: count the payment methods
# TODO 2: store the counts in `methods` with .value_counts() on the payment_method column
methods = None
print("Payment methods:")
print(methods if methods is not None else "TODO 2: `methods` is still None")

# %% Step 3: what share of orders used a digital wallet?
# TODO 3: (orders["payment_method"] == "digital_wallet") is a True/False column.
#         Its .mean() is the fraction that is True. Multiply by 100 and round to 1 place.
wallet_pct = None
print("Digital wallet share (%):", wallet_pct if wallet_pct is not None else "TODO 3")

# %% Step 4: filter to the gift-card orders
# TODO 4: gift = orders[ ... ]   (the same pattern as the lesson's `completed` filter)
gift = None
if gift is None:
    print("TODO 4: `gift` is still None")
else:
    print("Gift-card orders:", len(gift))
    print(f"Average gift-card order: ${gift['order_total'].mean():.2f}")

# %% Step 5: where is cash used?
# TODO 5: filter to the cash orders, then count their `channel` column.
#         Write what you see as a comment: is cash ever used online?
cash = None
print(cash["channel"].value_counts() if cash is not None else "TODO 5: `cash` is still None")
