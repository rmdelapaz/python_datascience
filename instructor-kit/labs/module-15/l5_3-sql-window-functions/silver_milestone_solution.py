# --- lab bootstrap: find labs_paths.py (the same three lines open every lab; see labs/README.md) ---
import pathlib, sys
sys.path[:0] = [str(p) for p in pathlib.Path(globals().get("__file__", "lab.py")).resolve().parents if (p / "labs_paths.py").is_file()]
from labs_paths import DATA

# %% [markdown]
# # Lab 5.3-B · On which order does a customer reach Silver? (SOLUTION)
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
# Reference solution. Do not hand out before the lab.

# %% Setup (done for you)
import sqlite3
import pandas as pd

conn = sqlite3.connect((DATA / "pinecrest.db").as_uri() + "?mode=ro", uri=True)


def show(sql, params=()):
    """Run a query and print the result as a table."""
    print(pd.read_sql(sql, conn, params=params).to_string(index=False))


# %% Step 1: number each customer's completed orders and keep a running total
RUNNING = """
    WITH running AS (
        SELECT o.customer_id,
               o.order_id,
               o.order_date,
               o.order_total,
               ROW_NUMBER() OVER by_customer                       AS n,
               ROUND(SUM(o.order_total) OVER (by_customer
                     ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW), 2) AS spent_so_far
        FROM orders AS o
        JOIN customers AS c ON c.customer_id = o.customer_id
        WHERE o.status = 'completed'
        WINDOW by_customer AS (PARTITION BY o.customer_id ORDER BY o.order_date, o.order_id)
    )
"""
show(RUNNING + "SELECT * FROM running WHERE customer_id = 10034 ORDER BY n LIMIT 6")

# %% Step 2: the first order on which spent_so_far reaches 600, per customer
print()
MILESTONE = RUNNING + """
    , first_600 AS (
        SELECT customer_id, MIN(n) AS order_number
        FROM running
        WHERE spent_so_far >= 600
        GROUP BY customer_id
    )
"""
show(MILESTONE + """
    SELECT COUNT(*)                     AS customers_reaching_600,
           ROUND(AVG(order_number), 1)  AS avg_order_number,
           MIN(order_number)            AS fewest,
           MAX(order_number)            AS most
    FROM first_600
""")
show(MILESTONE + """
    SELECT order_number, COUNT(*) AS customers
    FROM first_600
    GROUP BY order_number
    ORDER BY order_number
""")

# %% Step 3: check against what we already know
print()
known = conn.execute("SELECT COUNT(*) FROM customers WHERE loyalty_tier IN ('Silver', 'Gold')").fetchone()[0]
print("customers in the Silver or Gold tier (customers table):", known)
print("The two counts agree: the running total reproduces the tier rule exactly.")

# %% Step 4: do the gaps between orders shrink? (all statuses, all buyers)
print()
show("""
    WITH gaps AS (
        SELECT ROW_NUMBER() OVER (PARTITION BY customer_id ORDER BY order_date, order_id) AS n,
               julianday(order_date)
                 - julianday(LAG(order_date) OVER (PARTITION BY customer_id
                                                   ORDER BY order_date, order_id))       AS gap_days
        FROM orders
    )
    SELECT CASE WHEN n >= 6 THEN '6th or later' ELSE 'order ' || n END AS which_order,
           COUNT(gap_days)                                            AS gaps,
           ROUND(AVG(gap_days), 1)                                    AS avg_days_since_previous
    FROM gaps
    WHERE n > 1
    GROUP BY which_order
    ORDER BY MIN(n)
""")
print("Caution: later orders come only from customers who keep buying, and frequent buyers have")
print("short gaps by definition. The table describes WHO reaches a 6th order, not a change in anyone.")
conn.close()
