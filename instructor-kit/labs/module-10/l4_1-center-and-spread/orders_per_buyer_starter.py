# --- lab bootstrap: find labs_paths.py (the same three lines open every lab; see labs/README.md) ---
import pathlib, sys
sys.path[:0] = [str(p) for p in pathlib.Path(globals().get("__file__", "lab.py")).resolve().parents if (p / "labs_paths.py").is_file()]
from labs_paths import DATA

# %% [markdown]
# # Lab 4.1-A · How many orders does a buyer place? (STARTER)
# The loyalty team says "our customers order about five times". Is that a fair description
# of a typical buyer? Find the three centers, see how they disagree, and decide which number
# belongs in which sentence.
#
# Expected when you finish: three centers that are all different (one of them is 1), the share
# of buyers below the mean (more than half), two totals of which only one equals 20302, and
# two sentences for the loyalty team built from your variables.

# %% Load the orders and count them per customer (done for you)
import pandas as pd

orders = pd.read_csv(DATA / "orders.csv", parse_dates=["order_date"])
per_buyer = orders.groupby("customer_id").size()       # one number per buyer: how many orders
print("buyers:", len(per_buyer), "| orders:", per_buyer.sum())

# %% Step 1: three centers
# Write your guess first: which will be largest, the mean, the median or the mode? ________
# TODO 1: compute the mean, the median and the mode of `per_buyer`.
#         (.mode() returns a Series because ties can happen: take element [0].)
mean = None
median = None
mode = None
print("mean  :", mean)
print("median:", median)
print("mode  :", mode)

# %% Step 2: how many buyers are below "average"?
# TODO 2: make a True/False column `below` (per_buyer < mean) and print its mean, rounded to 3.
#         The mean of a boolean column is a proportion.
below = None

# %% Step 3: which center multiplies back to the total?
# TODO 3: print mean * number of buyers, median * number of buyers, and per_buyer.sum().

# %% Step 4: how much does the heaviest buyer matter?
# TODO 4: drop the single largest value (per_buyer[per_buyer < per_buyer.max()]) and print the
#         mean and the median again. Which one moved?

# %% Step 5: the sentence for the loyalty team
# TODO 5: write two sentences with an f-string, using your variables (no numbers typed by hand):
#         what a typical buyer does, and what the mean is good for.
if mean is None:
    print("TODO 1-5 not done yet. Expected: three different centers, then your two sentences.")
