# --- lab bootstrap: find labs_paths.py (the same three lines open every lab; see labs/README.md) ---
import pathlib, sys
sys.path[:0] = [str(p) for p in pathlib.Path(globals().get("__file__", "lab.py")).resolve().parents if (p / "labs_paths.py").is_file()]
from labs_paths import DATA

# %% [markdown]
# # Lab 4.7-B · When are online orders bigger? (STARTER)
# The e-commerce team asks: "Are there days, months or payment methods where people place
# bigger online orders? We would like to time our 'add one more item' banner."
# That is step 6 of the routine, a segment scan, and a scan needs the two disciplines:
#   1. count every comparison and correct for them (Holm);
#   2. for whatever survives, check the obvious competing explanation.
#
# Expected when you finish: one line that says how many tests you ran and how many are below
# 0.05 before and after correction, the five smallest p-values, a tent-share table, a table of
# medians with and without a tent, and a short findings note.

# %% Setup (done for you)
import pandas as pd
from scipy import stats
from statsmodels.stats.multitest import multipletests

orders = pd.read_csv(DATA / "orders.csv", parse_dates=["order_date"])
online = orders[orders["channel"] == "online"].copy()
online["weekday"] = online["order_date"].dt.day_name()
online["month"] = online["order_date"].dt.month_name()
print("online orders:", len(online), "| median order total:", online["order_total"].median())
print("order_total is right-skewed (mean", round(online["order_total"].mean(), 2),
      "), so compare medians and use the Mann-Whitney test.")

# %% Step 1: the scan - each group against all other online orders
# TODO 1: for each seg in ["weekday", "payment_method", "month"] and each level of that column,
#         compare order_total inside the group with order_total of all OTHER online orders:
#         x = online.loc[inside, "order_total"], y = online.loc[~inside, "order_total"].
#         Append a dict with segment, group, n, median, median_rest and p (stats.mannwhitneyu).
rows = []
scan = pd.DataFrame(rows)

# %% Step 2: discipline 1 - count the comparisons and correct
# TODO 2: add scan["p_holm"] with multipletests(scan["p"], method="holm")[1].
#         Print: how many tests, how many below 0.05 before correction, how many after.
#         Print the five rows with the smallest p.
if scan.empty:
    print("TODO 1-2 not done yet: `scan` is empty.")

# %% Step 3: discipline 2 - could something else explain the survivor?
# One month should survive. Before you call it "the month people spend more", think about
# what Pinecrest sells in that month (Lesson 2.4) and check it.
order_items = pd.read_csv(DATA / "order_items.csv")
# TODO 3: tent SKUs start with "TNT". Build online["has_tent"] (does the order contain a tent?)
#         and online["june"]. Compare: the share of orders with a tent in June and in other months;
#         the median order_total in the four cells of has_tent x june (pivot_table);
#         June against other months WITHIN tent orders and WITHIN non-tent orders (mannwhitneyu).

# %% Step 4: the note
# TODO 4: findings (with numbers), caveats, one next question. Which results are leads only?
note = "TODO: write your findings note here."
print(note)
