# --- lab bootstrap: find labs_paths.py (the same three lines open every lab; see labs/README.md) ---
import pathlib, sys
sys.path[:0] = [str(p) for p in pathlib.Path(globals().get("__file__", "lab.py")).resolve().parents if (p / "labs_paths.py").is_file()]
from labs_paths import DATA

# %% [markdown]
# # Lab 5.2-A · Revenue by brand, and what an inner join hides (SOLUTION)
# The buying team wants item revenue by BRAND for completed orders. Brand lives in
# `products`, revenue in `order_items`, status in `orders`: three tables.
# Before every join: write down how many rows you expect. After it: count.
#
# Known facts (from data/README.md): every order line has an order; 609 order lines use
# 6 discontinued SKUs that are not in `products`.
#
# Skills: INNER and LEFT JOIN, predicting row counts, COALESCE, the anti-join.
#
# Reference solution. Do not hand out before the lab.

# %% Setup (done for you)
import sqlite3
import pandas as pd

conn = sqlite3.connect((DATA / "pinecrest.db").as_uri() + "?mode=ro", uri=True)


def show(sql, params=()):
    """Run a query and print the result as a table."""
    print(pd.read_sql(sql, conn, params=params).to_string(index=False))


# %% Step 1: predict, then count - order lines joined to products
# Prediction: 45,490 lines; 609 have no product. INNER keeps 44,881; LEFT keeps 45,490.
show("""
    SELECT (SELECT COUNT(*) FROM order_items)                                           AS lines,
           (SELECT COUNT(*) FROM order_items AS i JOIN products AS p ON p.sku = i.sku)  AS inner_join,
           (SELECT COUNT(*) FROM order_items AS i LEFT JOIN products AS p ON p.sku = i.sku) AS left_join
""")

# %% Step 2: revenue by brand with an INNER join to products (the tempting version)
print()
show("""
    SELECT ROUND(SUM(i.quantity * i.unit_price), 2) AS revenue_inner_join,
           COUNT(*)                                 AS lines
    FROM orders AS o
    JOIN order_items AS i ON i.order_id = o.order_id
    JOIN products AS p ON p.sku = i.sku
    WHERE o.status = 'completed'
""")

# %% Step 3: the same with a LEFT join, so no line is lost
print()
show("""
    SELECT COALESCE(p.brand, 'Discontinued') AS brand,
           COUNT(*)                          AS lines,
           ROUND(SUM(i.quantity * i.unit_price), 2) AS item_revenue
    FROM orders AS o
    JOIN order_items AS i ON i.order_id = o.order_id
    LEFT JOIN products AS p ON p.sku = i.sku
    WHERE o.status = 'completed'
    GROUP BY COALESCE(p.brand, 'Discontinued')
    ORDER BY item_revenue DESC
""")
total = conn.execute("""
    SELECT ROUND(SUM(i.quantity * i.unit_price), 2), COUNT(*)
    FROM orders AS o JOIN order_items AS i ON i.order_id = o.order_id
    WHERE o.status = 'completed'
""").fetchone()
print("all completed lines:", total[1], "| item revenue:", total[0])

# %% Step 4: the anti-join - which SKUs were sold but are not in the catalog?
print()
show("""
    SELECT i.sku,
           COUNT(*)                                 AS lines,
           SUM(i.quantity)                          AS units,
           ROUND(SUM(i.quantity * i.unit_price), 2) AS item_revenue,
           MAX(o.order_date)                        AS last_sold
    FROM order_items AS i
    JOIN orders AS o ON o.order_id = i.order_id
    LEFT JOIN products AS p ON p.sku = i.sku
    WHERE p.sku IS NULL
    GROUP BY i.sku
    ORDER BY item_revenue DESC
""")

# %% Step 5: the other direction - brands with a product that has never sold
print()
show("""
    SELECT p.brand, COUNT(*) AS never_sold
    FROM products AS p
    WHERE NOT EXISTS (SELECT 1 FROM order_items AS i WHERE i.sku = p.sku)
    GROUP BY p.brand
    ORDER BY never_sold DESC, p.brand
""")
conn.close()
