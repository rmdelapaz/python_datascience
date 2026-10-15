# --- lab bootstrap: find labs_paths.py (the same three lines open every lab; see labs/README.md) ---
import pathlib, sys
sys.path[:0] = [str(p) for p in pathlib.Path(globals().get("__file__", "lab.py")).resolve().parents if (p / "labs_paths.py").is_file()]
from labs_paths import DATA

# %% [markdown]
# # Lab 4.1-A · How many orders does a buyer place? (SOLUTION)
# The loyalty team says "our customers order about five times". Is that a fair description
# of a typical buyer? Find the three centers, see how they disagree, and decide which number
# belongs in which sentence.

# %% Load the orders and count them per customer
import pandas as pd

orders = pd.read_csv(DATA / "orders.csv", parse_dates=["order_date"])
per_buyer = orders.groupby("customer_id").size()       # one number per buyer: how many orders
print("buyers:", len(per_buyer), "| orders:", per_buyer.sum())

# %% Step 1: three centers
mean = per_buyer.mean()
median = per_buyer.median()
mode = per_buyer.mode()[0]
print("mean  :", round(mean, 2))
print("median:", median)
print("mode  :", mode, f"({(per_buyer == mode).sum()} buyers ordered exactly {mode} time)")

# %% Step 2: how many buyers are below "average"?
below = per_buyer < mean                               # a column of True / False
print("share of buyers below the mean:", round(below.mean(), 3))
print("largest five counts:", per_buyer.sort_values().tail(5).tolist())

# %% Step 3: which center multiplies back to the total?
print("mean   x buyers:", round(mean * len(per_buyer)))
print("median x buyers:", round(median * len(per_buyer)))
print("real total     :", per_buyer.sum())

# %% Step 4: how much does the heaviest buyer matter?
without_top = per_buyer[per_buyer < per_buyer.max()]
print("without the top buyer: mean", round(without_top.mean(), 2), "| median", without_top.median())

# %% Step 5: the sentence for the loyalty team, built from the variables
print(f"A typical buyer placed {median:.0f} orders in two years (the median).")
print(f"The most common count is {mode}.")
print(f"The mean is {mean:.2f} because a long tail of frequent buyers pulls it up:")
print(f"{below.mean():.0%} of buyers are below it. Use the mean only for totals")
print("(mean x buyers = orders).")
