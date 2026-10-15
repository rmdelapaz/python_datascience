# --- lab bootstrap: find labs_paths.py (the same three lines open every lab; see labs/README.md) ---
import pathlib, sys
sys.path[:0] = [str(p) for p in pathlib.Path(globals().get("__file__", "lab.py")).resolve().parents if (p / "labs_paths.py").is_file()]
from labs_paths import DATA

# %% [markdown]
# # Lab 5.2-B · Stock against sales (SOLUTION)
# The warehouse lead asks: "For each category, how many units did we sell in 2025 and how
# many do we have on hand now? Where is cover thin?"
# Units sold come from `order_items` (many rows per SKU). Units on hand come from
# `inventory` (five rows per SKU, one per location). Join them directly and BOTH numbers
# are wrong. This lab makes the mistake on purpose, then fixes it with CTEs.
#
# Skills: the fan-out trap, CTEs that aggregate before joining, CASE, 100.0 arithmetic.
#
# Reference solution. Do not hand out before the lab.

# %% Setup (done for you)
import sqlite3
import pandas as pd

conn = sqlite3.connect((DATA / "pinecrest.db").as_uri() + "?mode=ro", uri=True)


def show(sql, params=()):
    """Run a query and print the result as a table."""
    print(pd.read_sql(sql, conn, params=params).to_string(index=False))


# %% Step 1: the two true totals, each from its own table
show("""
    SELECT (SELECT SUM(i.quantity)
            FROM order_items AS i JOIN orders AS o ON o.order_id = i.order_id
            WHERE o.status = 'completed' AND o.order_date >= '2025-01-01') AS units_sold_2025,
           (SELECT SUM(quantity) FROM inventory)                           AS units_on_hand
""")

# %% Step 2: the tempting query - join lines and inventory on sku, then sum
print()
show("""
    SELECT SUM(i.quantity)  AS units_sold_2025,
           SUM(v.quantity)  AS units_on_hand,
           COUNT(*)         AS rows_summed
    FROM order_items AS i
    JOIN orders AS o ON o.order_id = i.order_id
    JOIN inventory AS v ON v.sku = i.sku
    WHERE o.status = 'completed' AND o.order_date >= '2025-01-01'
""")
print("Each order line met its SKU's five inventory rows (units sold x 5), and each inventory")
print("row was repeated once per order line of that SKU (units on hand x 162). No error, no warning.")

# %% Step 3: aggregate each side to ONE ROW PER SKU first, then join
print()
STOCK_SQL = """
    WITH sold AS (
        SELECT i.sku, SUM(i.quantity) AS units_sold
        FROM order_items AS i
        JOIN orders AS o ON o.order_id = i.order_id
        WHERE o.status = 'completed' AND o.order_date >= '2025-01-01'
        GROUP BY i.sku
    ),
    on_hand AS (
        SELECT sku, SUM(quantity) AS units_on_hand
        FROM inventory
        GROUP BY sku
    ),
    per_sku AS (
        SELECT p.sku, p.category,
               COALESCE(s.units_sold, 0) AS units_sold,
               h.units_on_hand
        FROM products AS p
        JOIN on_hand AS h ON h.sku = p.sku
        LEFT JOIN sold AS s ON s.sku = p.sku
    )
"""
show(STOCK_SQL + "SELECT COUNT(*) AS skus, SUM(units_sold) AS units_sold_2025, SUM(units_on_hand) AS units_on_hand FROM per_sku")

# %% Step 4: one row per category, with weeks of cover and a label
print()
show(STOCK_SQL + """
    SELECT category,
           SUM(units_sold)                                    AS sold_2025,
           SUM(units_on_hand)                                 AS on_hand,
           ROUND(52.0 * SUM(units_on_hand) / SUM(units_sold), 1) AS weeks_of_cover,
           CASE
               WHEN 52.0 * SUM(units_on_hand) / SUM(units_sold) < 26 THEN 'thin'
               WHEN 52.0 * SUM(units_on_hand) / SUM(units_sold) < 45 THEN 'ok'
               ELSE                                                    'heavy'
           END                                                AS cover
    FROM per_sku
    GROUP BY category
    ORDER BY weeks_of_cover
""")

# %% Step 5: why 52.0 and not 52
print()
show("SELECT 52 * 22815 / 30894 AS integer_math, 52.0 * 22815 / 30894 AS real_math, 22815 / 30894 AS ratio_as_integers")
print("Check: 2025 lines on SKUs that are not in products (they would be missing from per_sku):",
      conn.execute("""
          SELECT COUNT(*)
          FROM order_items AS i JOIN orders AS o ON o.order_id = i.order_id
          LEFT JOIN products AS p ON p.sku = i.sku
          WHERE o.status = 'completed' AND o.order_date >= '2025-01-01' AND p.sku IS NULL
      """).fetchone()[0])
conn.close()
