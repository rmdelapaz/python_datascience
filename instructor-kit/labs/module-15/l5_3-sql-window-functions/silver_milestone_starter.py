# --- lab bootstrap: find labs_paths.py (the same three lines open every lab; see labs/README.md) ---
import pathlib, sys
sys.path[:0] = [str(p) for p in pathlib.Path(globals().get("__file__", "lab.py")).resolve().parents if (p / "labs_paths.py").is_file()]
from labs_paths import DATA

# %% [markdown]
# # Lab 5.3-B · On which order does a customer reach Silver? (STARTER)
# The loyalty team knows the rule: Silver at $600 of COMPLETED spend. They ask:
#   1. On which order (1st, 2nd, 3rd, ...) does a typical customer cross $600?
#   2. Do the gaps between orders get shorter as customers keep buying?
# Both questions are about each customer's own sequence of orders: number them, keep a
# running total, look back one order. Window functions, partitioned by customer.
#
# Skills: ROW_NUMBER with a tiebreaker, a running SUM with an explicit ROWS frame,
# LAG with julianday(), "first row that meets a condition" per group, and a check against
# a number we already know (Silver + Gold customers in customers.csv).
#
# Expected when you finish: customer 10034's first six orders with a running total; one line saying
# how many customers reach $600 and on which order on average, a table of order numbers; a check
# against the Silver + Gold count in customers; and the average gap before the 2nd, 3rd, ... order.

# %% Setup (done for you)
import sqlite3
import pandas as pd

conn = sqlite3.connect((DATA / "pinecrest.db").as_uri() + "?mode=ro", uri=True)


def show(sql, params=()):
    """Run a query and print the result as a table."""
    print(pd.read_sql(sql, conn, params=params).to_string(index=False))


# %% Step 1: number each customer's completed orders and keep a running total
# TODO 1: write RUNNING, a string holding one CTE called running: completed orders joined to
#         customers (closed accounts have no tier, so leave them out), with
#           n            = ROW_NUMBER() OVER (PARTITION BY customer_id ORDER BY order_date, order_id)
#           spent_so_far = SUM(order_total) over the same window,
#                          ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
#         Tip: name the window once with WINDOW by_customer AS (...).
#         Show customer 10034's first six rows. Why is order_id in the ORDER BY?
RUNNING = ""

# %% Step 2: the first order on which spent_so_far reaches 600, per customer
# TODO 2: add a second CTE (start the extra text with a comma): for each customer, MIN(n) among
#         rows with spent_so_far >= 600. Report how many customers, the average, min and max
#         order number, then a count of customers per order number.

# %% Step 3: check against what we already know
# TODO 3: count customers whose loyalty_tier is Silver or Gold. Does it equal Step 2's count?
#         What would it mean if it did not?

# %% Step 4: do the gaps between orders shrink? (all statuses, all buyers)
# TODO 4: with LAG(order_date) over each customer's orders and julianday(), compute the days since
#         the previous order; average it by order number (2, 3, 4, 5, then "6th or later").
#         Then write one sentence of caution: who is in the "6th or later" group?
if not RUNNING:
    print("TODO 1-4 not done yet: RUNNING is empty.")
conn.close()
