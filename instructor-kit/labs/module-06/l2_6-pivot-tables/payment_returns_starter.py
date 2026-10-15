# --- lab bootstrap: find labs_paths.py (the same three lines open every lab; see labs/README.md) ---
import pathlib, sys
sys.path[:0] = [str(p) for p in pathlib.Path(globals().get("__file__", "lab.py")).resolve().parents if (p / "labs_paths.py").is_file()]
from labs_paths import DATA
# %% [markdown]
# # Lab 2.6-A · Returns by payment method: read the grid honestly (STARTER)
# Question: are orders paid one way returned more often than orders paid another way?
# You will build the grid, then put it through the lesson's checks before believing it:
# the aggregation, the counts behind the cells, the empty cells, the totals, and whether
# a total hides a difference inside it.
#
# Before each pivot say the four things out loud: rows, columns, values, how to combine.
#
# Expected when you finish: a count grid whose corner is 20,302, a return-rate grid in
# percent with one honestly empty cell, the weakest cell and how few orders are behind
# it, two crosstabs that answer two different questions, and a channel split.

# %% Load (done for you)
import pandas as pd

pd.set_option("display.width", 150)
pd.set_option("display.max_columns", 20)

orders = pd.read_csv(DATA / "orders.csv", parse_dates=["order_date"])
orders["returned"] = orders["status"] == "returned"
print(orders.shape)

# %% Step 1: how many orders are behind each cell?
# TODO 1: counts = orders.pivot_table(index="payment_method", columns="store", values="order_id",
#                                     aggfunc="count", fill_value=0, margins=True, margins_name="Total")
#         Is the bottom-right corner the number of rows in `orders`?
counts = None

# %% Step 2: the return rate in each cell (the mean of True/False, times 100)
# TODO 2: rate = orders.pivot_table(index=..., columns=..., values="returned", aggfunc=..., margins=True) * 100
#         One cell is NaN. Should you use fill_value=0 here? Write your answer as a comment.
rate = None

# %% Step 3: a mean without its count is half a fact
# TODO 3: the lowest rate among the STORES belongs to gift cards in Bend.
#         Read that cell from `rate` and from `counts` with .loc[row, column].
#         How many returned orders is that?

# %% Step 4: two crosstabs, two questions
# TODO 4: of_method = pd.crosstab(orders["payment_method"], orders["status"], normalize="index") * 100
#         of_status = pd.crosstab(orders["payment_method"], orders["status"], normalize="columns") * 100
#         Finish the sentences:  "Of digital-wallet orders, ___% were returned."
#                                "Of returned orders, ___% were paid by digital wallet."
of_method = of_status = None

# %% Step 5: does the total hide a difference inside it?
# TODO 5: by_channel = orders.pivot_table(index="payment_method", columns="channel", values="returned",
#                                         aggfunc="mean", margins=True) * 100
#         Compare the "All" column with the online and store columns.
by_channel = None

# %% Report
if counts is None or rate is None or of_method is None or by_channel is None:
    print("TODOs not done yet: counts, rate, of_method or by_channel is still None.")
else:
    print(counts)
    print(rate.round(1))
    print(by_channel.round(1))
