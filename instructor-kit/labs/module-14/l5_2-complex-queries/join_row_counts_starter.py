# --- lab bootstrap: find labs_paths.py (the same three lines open every lab; see labs/README.md) ---
import pathlib, sys
sys.path[:0] = [str(p) for p in pathlib.Path(globals().get("__file__", "lab.py")).resolve().parents if (p / "labs_paths.py").is_file()]
from labs_paths import DATA

# %% [markdown]
# # Lab 5.2-A · Revenue by brand, and what an inner join hides (STARTER)
# The buying team wants item revenue by BRAND for completed orders. Brand lives in
# `products`, revenue in `order_items`, status in `orders`: three tables.
# Before every join: write down how many rows you expect. After it: count.
#
# Known facts (from data/README.md): every order line has an order; 609 order lines use
# 6 discontinued SKUs that are not in `products`.
#
# Skills: INNER and LEFT JOIN, predicting row counts, COALESCE, the anti-join.
#
# Expected when you finish: three row counts that match your predictions, revenue from the
# tempting inner join, a brand table with a 'Discontinued' row whose revenue adds up to the
# total of all completed lines, the six missing SKUs, and the brands with unsold products.

# %% Setup (done for you)
import sqlite3
import pandas as pd

conn = sqlite3.connect((DATA / "pinecrest.db").as_uri() + "?mode=ro", uri=True)


def show(sql, params=()):
    """Run a query and print the result as a table."""
    print(pd.read_sql(sql, conn, params=params).to_string(index=False))


# %% Step 1: predict, then count - order lines joined to products
# Write your three predictions here BEFORE running anything:
#   rows in order_items: ______   after INNER JOIN products: ______   after LEFT JOIN products: ______
# TODO 1: one query (or three) that returns the three counts.

# %% Step 2: revenue by brand with an INNER join to products (the tempting version)
# TODO 2: orders JOIN order_items JOIN products, completed orders only:
#         total of quantity * unit_price, and the number of lines. Keep the two numbers.

# %% Step 3: the same with a LEFT join, so no line is lost
# TODO 3: item revenue and number of lines per brand, with the link to products as a LEFT JOIN
#         and COALESCE(p.brand, 'Discontinued') as the brand. Then print the total over ALL
#         completed lines (no products table at all). How much revenue did Step 2 lose?

# %% Step 4: the anti-join - which SKUs were sold but are not in the catalog?
# TODO 4: LEFT JOIN products and keep the rows WHERE p.sku IS NULL. Per sku: lines, units,
#         item revenue and the last order date (you need orders for the date).

# %% Step 5: the other direction - brands with a product that has never sold
# TODO 5: products for which NOT EXISTS (SELECT 1 FROM order_items ...), counted by brand.
print("TODO 1-5 not done yet. Predictions first, then queries.")
conn.close()
