# --- lab bootstrap: find labs_paths.py (the same three lines open every lab; see labs/README.md) ---
import pathlib, sys
sys.path[:0] = [str(p) for p in pathlib.Path(globals().get("__file__", "lab.py")).resolve().parents if (p / "labs_paths.py").is_file()]
from labs_paths import DATA

# %% [markdown]
# # Lab 4.5-B · Do orders with footwear come back more often? (STARTER)
# Lesson 3.3 drew the chart. Now test it: online orders that contain footwear against online
# orders that do not, then the same question for store orders. Two tests, so correct for both.
#
# Expected when you finish: an online 2 x 2 table, return rates of about 14% and 5%, a
# chi-square p-value far below 0.001 with every expected count well above 5; a store result
# that is NOT significant; Holm-adjusted p-values; and a report that words the store result
# as "not detected", not "no difference".

# %% Flag every order that contains a footwear line (done for you)
import numpy as np
import pandas as pd
from scipy import stats
from scipy.stats.contingency import association
from statsmodels.stats.multitest import multipletests

orders = pd.read_csv(DATA / "orders.csv", parse_dates=["order_date"])
items = pd.read_csv(DATA / "order_items.csv")
footwear_ids = items.loc[items["sku"].str.startswith("FTW"), "order_id"].unique()
orders["footwear"] = orders["order_id"].isin(footwear_ids)
orders["returned"] = orders["status"] == "returned"
print("orders with footwear:", orders["footwear"].sum(), "of", len(orders))

# TODO 0: write H0, H1 and alpha here before you test.

# %% Step 1: online orders. The table, the rates, the test
online = orders[orders["channel"] == "online"]
# TODO 1: table = pd.crosstab(online["footwear"], online["returned"]); print it.
#         Print the two return rates and their ratio (groupby("footwear")["returned"].mean()).
#         chi = stats.chi2_contingency(table): print the statistic, df and p, the smallest
#         expected count, and Cramer's V with association(table, method="cramer").
chi = None

# %% Step 2: store orders, the same question
# TODO 2: repeat Step 1 for channel == "store".

# %% Step 3: two tests, so adjust
# TODO 3: multipletests([p_online, p_store], method="holm")[1] gives the adjusted p-values.

# %% Step 4: the report
# TODO 4: print a report: both rates for each channel, the ratio, the adjusted p-values, and
#         a careful sentence about the store result.
if chi is None:
    print("TODO 1-4 not done yet: `chi` is still None.")
