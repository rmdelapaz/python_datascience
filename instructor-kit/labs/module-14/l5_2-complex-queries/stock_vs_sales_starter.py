# --- lab bootstrap: find labs_paths.py (the same three lines open every lab; see labs/README.md) ---
import pathlib, sys
sys.path[:0] = [str(p) for p in pathlib.Path(globals().get("__file__", "lab.py")).resolve().parents if (p / "labs_paths.py").is_file()]
from labs_paths import DATA

# %% [markdown]
# # Lab 5.2-B · Stock against sales (STARTER)
# The warehouse lead asks: "For each category, how many units did we sell in 2025 and how
# many do we have on hand now? Where is cover thin?"
# Units sold come from `order_items` (many rows per SKU). Units on hand come from
# `inventory` (five rows per SKU, one per location). Join them directly and BOTH numbers
# are wrong. This lab makes the mistake on purpose, then fixes it with CTEs.
#
# Skills: the fan-out trap, CTEs that aggregate before joining, CASE, 100.0 arithmetic.
#
# Expected when you finish: the two true totals, the two inflated totals from the tempting
# join, the same true totals from the CTE version (242 SKUs), a nine-row category table with
# weeks of cover and a label, and one line that shows what integer division would have done.

# %% Setup (done for you)
import sqlite3
import pandas as pd

conn = sqlite3.connect((DATA / "pinecrest.db").as_uri() + "?mode=ro", uri=True)


def show(sql, params=()):
    """Run a query and print the result as a table."""
    print(pd.read_sql(sql, conn, params=params).to_string(index=False))


# %% Step 1: the two true totals, each from its own table
# TODO 1: units sold in 2025 on completed orders (order_items joined to orders for the date and
#         status), and units on hand (SUM(quantity) FROM inventory). Two separate sums.
#         These are the numbers every later step must reproduce.

# %% Step 2: the tempting query - join lines and inventory on sku, then sum
# TODO 2: FROM order_items JOIN orders ... JOIN inventory AS v ON v.sku = i.sku, same filters,
#         and select SUM(i.quantity), SUM(v.quantity), COUNT(*).
#         Compare with Step 1. By what factor is each one off, and why that factor?

# %% Step 3: aggregate each side to ONE ROW PER SKU first, then join
# TODO 3: build STOCK_SQL, a string holding three CTEs:
#           sold     - one row per sku: units sold in 2025 on completed orders
#           on_hand  - one row per sku: total quantity over all locations
#           per_sku  - products JOIN on_hand LEFT JOIN sold, with COALESCE(units_sold, 0)
#         then check: SELECT COUNT(*), SUM(units_sold), SUM(units_on_hand) FROM per_sku
STOCK_SQL = ""

# %% Step 4: one row per category, with weeks of cover and a label
# TODO 4: weeks_of_cover = 52.0 * on hand / sold, rounded to 1 decimal, and a CASE label:
#         under 26 weeks 'thin', under 45 'ok', otherwise 'heavy'. Thinnest cover first.

# %% Step 5: why 52.0 and not 52
# TODO 5: run SELECT 52 * 22815 / 30894, 52.0 * 22815 / 30894, 22815 / 30894 and explain the three results.
if not STOCK_SQL:
    print("TODO 1-5 not done yet: STOCK_SQL is empty.")
conn.close()
