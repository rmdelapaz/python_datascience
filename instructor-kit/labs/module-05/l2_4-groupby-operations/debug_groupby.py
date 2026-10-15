# --- lab bootstrap: find labs_paths.py (the same three lines open every lab; see labs/README.md) ---
import pathlib, sys
sys.path[:0] = [str(p) for p in pathlib.Path(globals().get("__file__", "lab.py")).resolve().parents if (p / "labs_paths.py").is_file()]
from labs_paths import DATA

# %% [markdown]
# # Find the bug · five broken summaries (2.4)
# This file is broken ON PURPOSE. Two bugs stop the program: read the LAST line of the
# error, fix it, run again. Three bugs are QUIET: the code runs and prints a plausible
# number that is wrong. Find them by checking each result against its "should print" note.

# %%
import pandas as pd

orders = pd.read_csv(DATA / "orders.csv", parse_dates=["order_date"])

# %% Bug 1 (stops the program)
print(orders.groupby("store").mean().round(2))            # should print the mean order_total per store (5 rows)

# %% Bug 2 (stops the program)
summary = orders.groupby("store").agg(orders=("order_id", "count"), revenue=("order_total", "sum"))
print(summary["store"].tolist())                          # should print the five store names

# %% Bug 3 (quiet): how many orders were paid with each payment method?
print(orders.groupby("payment_method")["promo_code"].count())     # card should be 12392

# %% Bug 4 (quiet): do the promo-code groups account for every order?
groups = orders.groupby("promo_code").size()
print(groups.sum(), "of", len(orders))                    # should print 20302 of 20302

# %% Bug 5 (quiet): what is the average order value across the company?
store_means = orders.groupby("store")["order_total"].mean()
print(round(store_means.mean(), 2))                       # should print 194.6
