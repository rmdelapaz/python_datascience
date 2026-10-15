# --- lab bootstrap: find labs_paths.py (the same three lines open every lab; see labs/README.md) ---
import pathlib, sys
sys.path[:0] = [str(p) for p in pathlib.Path(globals().get("__file__", "lab.py")).resolve().parents if (p / "labs_paths.py").is_file()]
from labs_paths import DATA
# %% [markdown]
# # Lab 2.5-A · One row per customer, with names (STARTER)
# In Lesson 2.4 you built a customer summary that had ids but no names, tiers or states,
# because those live in customers.csv. Connect the two.
# Questions:
#   1. Who are the five biggest spenders, by name?
#   2. How many account holders never ordered, and in which loyalty tier are they?
#   3. Which orders belong to nobody in customers.csv, and what are they worth?
#
# The pattern: AGGREGATE each table to the level you need, THEN merge.
# Before every merge write down three things: which table is on the left, the relationship
# you expect, and the row count you expect. Then check all three.
#
# Expected when you finish: a five-row table of names and spend, a three-row table by
# loyalty tier, and one line about the orders that have no customer record.

# %% Load (done for you)
import pandas as pd

pd.set_option("display.width", 150)
pd.set_option("display.max_columns", 20)

orders = pd.read_csv(DATA / "orders.csv", parse_dates=["order_date"])
customers = pd.read_csv(DATA / "customers.csv")
print(len(orders), "orders |", len(customers), "customer accounts")

# %% Step 1: aggregate first (one row per customer id that has orders)
# TODO 1: summary = orders.groupby("customer_id", as_index=False).agg(
#             orders=("order_id", "count"), spend=("order_total", "sum"), last_order=("order_date", "max"))
#         How many rows? Is customer_id unique in `summary`? In `customers`?
summary = None

# %% Step 2: attach the summary to the accounts
# My prediction: left table = ________  relationship = ________  rows after = ________
# TODO 2: profiles = customers.merge(summary, on="customer_id", how=..., validate=..., indicator=True)
#         Print len(profiles) and profiles["_merge"].value_counts().
profiles = None

# %% Step 3: no orders means 0 orders (a count and a sum: 0 is the honest value)
# TODO 3: fill the missing `orders` and `spend` with 0 (assign the result back; no inplace=True).
#         Add never_ordered = profiles["_merge"] == "left_only".
#         Print the five biggest spenders with first_name, last_name, state, loyalty_tier, orders, spend.

# %% Step 4: one row per tier
# TODO 4: by_tier = profiles.groupby("loyalty_tier").agg(
#             accounts=("customer_id", "count"), never_ordered=("never_ordered", "mean"), avg_spend=("spend", "mean"))
by_tier = None

# %% Step 5: audit the other side
# TODO 5: audit = customers[["customer_id"]].merge(summary, on="customer_id", how="outer", indicator=True)
#         The right_only rows are customer ids with orders but no account. How many ids,
#         how many orders, how much spend? (data/README.md says what they are.)
audit = None

# %% Report
if summary is None or profiles is None or by_tier is None or audit is None:
    print("TODOs not done yet: summary, profiles, by_tier or audit is still None.")
else:
    print(by_tier.round(3))
    print(audit["_merge"].value_counts().to_dict())
