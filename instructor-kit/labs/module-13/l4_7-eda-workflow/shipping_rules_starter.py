# --- lab bootstrap: find labs_paths.py (the same three lines open every lab; see labs/README.md) ---
import pathlib, sys
sys.path[:0] = [str(p) for p in pathlib.Path(globals().get("__file__", "lab.py")).resolve().parents if (p / "labs_paths.py").is_file()]
from labs_paths import DATA

# %% [markdown]
# # Lab 4.7-A · Who pays for shipping? (STARTER)
# Nobody at Pinecrest can find the document that says how shipping is charged. The data
# dictionary only says: shipping_cost is 0.00, 6.95 or 14.95.
# Run the routine on one column and work the rule out from the data.
#
# Step 1, the questions (written before loading anything):
#   1. Which orders are charged shipping at all?
#   2. What decides whether an order pays 0.00, 6.95 or 14.95?
#   3. What can the data not tell us about shipping?
#
# Expected when you finish: a channel-by-charge table, the share of online orders at each
# charge, a table of goods value for each charge, a two-by-three table that shows the rule,
# and a findings note with at least one caveat.

# %% Step 2: structure (done for you)
import pandas as pd

orders = pd.read_csv(DATA / "orders.csv", parse_dates=["order_date"])
print("rows:", len(orders), "| order_id unique:", orders["order_id"].is_unique)
print("grain: one row per order")

# %% Step 3: quality - anything missing or impossible in the columns we need?
# TODO 1: print the missing-value counts of channel, shipping_cost and order_total, the distinct
#         shipping values, and pd.crosstab(orders["channel"], orders["shipping_cost"]).
#         Which channel can you set aside, and why?

# %% Step 4: one variable - how common is each charge online?
# TODO 2: keep the online orders (use .copy()) and print the share of each shipping charge in percent.
online = orders[orders["channel"] == "online"].copy()

# %% Step 5: two variables - the charge against the value of the goods
# order_total includes the shipping, so take it out first.
# TODO 3: online["goods"] = order_total minus shipping_cost, rounded to 2 decimals.
#         Then for each shipping charge print count, min, median and max of goods.
#         Look hard at the min and max columns. What number keeps appearing?

# %% Step 5b: the picture suggests a threshold - test the idea directly
# TODO 4: make a True/False column for "goods is at least <your threshold>" and crosstab it
#         against shipping_cost. A rule with no exceptions shows up as zeros in the table.

# %% Step 6: segments - is the 14.95 charge tied to order size?
# TODO 5: cut goods into bands with pd.cut(online["goods"], [0, 25, 50, 75, 100, 150, 300, 5000], right=False)
#         and print the share of each charge within each band (crosstab with normalize="index").

# %% Step 7: findings, caveats, next questions
# TODO 6: replace the lines below with your note: two or three findings with numbers,
#         at least one caveat (what did you infer, and what does no column record?), one next question.
findings = ["TODO: finding 1", "TODO: finding 2"]
caveats = ["TODO: caveat"]
print()
print("FINDINGS:", *findings, sep="\n- ")
print("CAVEATS:", *caveats, sep="\n- ")
