# --- lab bootstrap: find labs_paths.py (the same three lines open every lab; see labs/README.md) ---
import pathlib, sys
sys.path[:0] = [str(p) for p in pathlib.Path(globals().get("__file__", "lab.py")).resolve().parents if (p / "labs_paths.py").is_file()]
from labs_paths import DATA

# %% [markdown]
# # Lab 5.1-B · A safe stock lookup (STARTER)
# Store managers want to type a location and a number and get back the products that are
# running low there. Whatever they type goes into a query, so the query must be safe.
# Question: which SKUs at a given location have a quantity at or below a given number?
#
# The `inventory` table: sku, location (four stores and 'Warehouse'), quantity,
# reorder_point, last_counted. One row per product per location (1,210 rows).
#
# Skills: ? and :name placeholders, a one-item tuple, why f-strings are dangerous,
# and checking a column name against an allowed list.
#
# Expected when you finish: matching counts from the unsafe and the safe function for honest
# input; 1210 against 0 for the crafted input; a ProgrammingError you caused on purpose; and a
# small table of out-of-stock SKUs in Flagstaff sorted by a column you checked first.

# %% Setup (done for you)
import sqlite3
import pandas as pd

conn = sqlite3.connect((DATA / "pinecrest.db").as_uri() + "?mode=ro", uri=True)


def count_low_unsafe(location, max_qty):
    """DO NOT copy this: the values are pasted into the SQL text."""
    sql = f"SELECT COUNT(*) FROM inventory WHERE location = '{location}' AND quantity <= {max_qty}"
    return conn.execute(sql).fetchone()[0]


# %% Step 1: the same count, with placeholders
# TODO 1: write count_low(location, max_qty) with two ? placeholders and a tuple of values.
#         It must return the same numbers as count_low_unsafe for ("Boise", 0) and ("Warehouse", 5).
def count_low(location, max_qty):
    return None


print("Boise, quantity <= 0:  unsafe", count_low_unsafe("Boise", 0), "| safe", count_low("Boise", 0))

# %% Step 2: attack both functions with the same input
# TODO 2: call both functions with the location below and max_qty 0, and print the two results
#         next to the number of rows in the table. Then print the SQL text the unsafe function
#         built, and explain in a comment what the quote and the two dashes did.
sneaky = "nowhere' OR '1'='1' --"

# %% Step 3: a one-item tuple
# TODO 3: count the inventory rows for sku "TNT-1001" with one ? placeholder.
#         Then pass the string itself instead of a tuple, inside try/except sqlite3.ProgrammingError,
#         and print the message. Why does it say 8?

# %% Step 4: the lookup the managers asked for, with named placeholders and a safe sort
# TODO 4: write low_stock(location, max_qty, sort_by="quantity") that returns a DataFrame of
#         sku, quantity, reorder_point, last_counted (as real dates) using :location and :max_qty.
#         A placeholder cannot stand for a column name, so check sort_by against ALLOWED_SORT
#         and raise ValueError if it is not there. Only then put it in the ORDER BY.
ALLOWED_SORT = {"quantity", "sku", "last_counted"}

if count_low("Boise", 0) is None:
    print("TODO 1-4 not done yet: count_low returns None.")
conn.close()
