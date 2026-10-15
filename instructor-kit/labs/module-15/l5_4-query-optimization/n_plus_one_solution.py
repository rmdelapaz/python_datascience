# --- lab bootstrap: find labs_paths.py (the same three lines open every lab; see labs/README.md) ---
import pathlib, sys
sys.path[:0] = [str(p) for p in pathlib.Path(globals().get("__file__", "lab.py")).resolve().parents if (p / "labs_paths.py").is_file()]
from labs_paths import DATA, OUTPUT

# %% [markdown]
# # Lab 5.4-B · One query, not three hundred (SOLUTION)
# A colleague's script builds a "customer value" table for the 300 newest Gold customers:
# for each one it runs a separate query for their completed order count and spend. That is
# the N+1 pattern (one query for the list, then one per item). You will measure it, read its
# plan, give it an index, and then replace the loop with ONE grouped query, checking that the
# answers are identical at every step.
#
# This lab creates an index, so it works on a COPY in the OUTPUT folder (cached_statements=0).
# Timings are for you to look at. Your numbers will differ; nothing depends on them.
#
# Reference solution. Do not hand out before the lab.

# %% Setup (done for you)
import shutil
import sqlite3
import time
import pandas as pd

work_db = OUTPUT / "pinecrest_nplus1.db"
shutil.copy(DATA / "pinecrest.db", work_db)
conn = sqlite3.connect(work_db, cached_statements=0)

gold_ids = [row[0] for row in conn.execute(
    "SELECT customer_id FROM customers WHERE loyalty_tier = 'Gold' ORDER BY signup_date DESC, customer_id LIMIT 300")]
print("Gold customers in the list:", len(gold_ids))

PER_CUSTOMER = """
    SELECT COUNT(*), ROUND(SUM(order_total), 2)
    FROM orders
    WHERE customer_id = ? AND status = 'completed'
"""


def best_ms(func, repeat=3):
    """Best of `repeat` runs, in milliseconds, and the last result."""
    best, result = float("inf"), None
    for _ in range(repeat):
        start = time.perf_counter()
        result = func()
        best = min(best, time.perf_counter() - start)
    return best * 1000, result


def loop_version():
    rows = []
    for cid in gold_ids:
        n, spent = conn.execute(PER_CUSTOMER, (cid,)).fetchone()
        rows.append((cid, n, spent))
    return sorted(rows)


def one_query_version():
    marks = ", ".join("?" * len(gold_ids))          # one placeholder per id: values still go in as parameters
    sql = f"""
        SELECT customer_id, COUNT(*), ROUND(SUM(order_total), 2)
        FROM orders
        WHERE status = 'completed' AND customer_id IN ({marks})
        GROUP BY customer_id
    """
    return sorted(conn.execute(sql, gold_ids).fetchall())


# %% Step 1: the loop, as written, with no index
print("\nplan of the per-customer query:")
for row in conn.execute("EXPLAIN QUERY PLAN " + PER_CUSTOMER, (gold_ids[0],)):
    print("   ", row[3])
t_loop, loop_rows = best_ms(loop_version)
print(f"300 queries in a loop: {t_loop:.0f} ms (your numbers will differ)")

# %% Step 2: one grouped query, still no index
t_one, one_rows = best_ms(one_query_version)
print(f"one GROUP BY query:    {t_one:.1f} ms")
print("same answers:", loop_rows == one_rows)

# %% Step 3: index the column the loop searches by, and measure both again
conn.execute("CREATE INDEX IF NOT EXISTS idx_orders_customer_id ON orders (customer_id)")
conn.commit()
print("\nplan with idx_orders_customer_id:")
for row in conn.execute("EXPLAIN QUERY PLAN " + PER_CUSTOMER, (gold_ids[0],)):
    print("   ", row[3])
t_loop_idx, loop_rows_idx = best_ms(loop_version)
t_one_idx, one_rows_idx = best_ms(one_query_version)
print(f"300 queries in a loop: {t_loop_idx:.1f} ms")
print(f"one GROUP BY query:    {t_one_idx:.1f} ms")
print("same answers:", loop_rows_idx == one_rows_idx == loop_rows)

# %% Step 4: the result, as a table, and what to say
table = pd.DataFrame(one_rows, columns=["customer_id", "orders", "spent"])
print()
print(table[["orders", "spent"]].describe().loc[["count", "mean", "min", "max"]].round(1).to_string())
print()
print("The loop was the slow part, not SQL: 300 scans of 20,302 orders. Either fix works; together")
print("they are best. On a server database each loop query also pays a network round trip, which no")
print("index can remove, so the one-query version is the habit to keep.")
conn.close()
