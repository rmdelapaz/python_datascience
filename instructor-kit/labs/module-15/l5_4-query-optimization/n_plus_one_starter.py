# --- lab bootstrap: find labs_paths.py (the same three lines open every lab; see labs/README.md) ---
import pathlib, sys
sys.path[:0] = [str(p) for p in pathlib.Path(globals().get("__file__", "lab.py")).resolve().parents if (p / "labs_paths.py").is_file()]
from labs_paths import DATA, OUTPUT

# %% [markdown]
# # Lab 5.4-B · One query, not three hundred (STARTER)
# A colleague's script builds a "customer value" table for the 300 newest Gold customers:
# for each one it runs a separate query for their completed order count and spend. That is
# the N+1 pattern (one query for the list, then one per item). You will measure it, read its
# plan, give it an index, and then replace the loop with ONE grouped query, checking that the
# answers are identical at every step.
#
# This lab creates an index, so it works on a COPY in the OUTPUT folder (cached_statements=0).
# Timings are for you to look at. Your numbers will differ; nothing depends on them.
#
# Expected when you finish: the plan of the per-customer query (SCAN), the loop's time, the one-query
# time and "same answers: True"; then the plan with an index (SEARCH), both times again and
# "same answers: True"; and a short summary table of the 300 customers.

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
    """The colleague's version (given): one query per customer."""
    rows = []
    for cid in gold_ids:
        n, spent = conn.execute(PER_CUSTOMER, (cid,)).fetchone()
        rows.append((cid, n, spent))
    return sorted(rows)


def one_query_version():
    """TODO 2: ONE query: completed orders WHERE customer_id IN (?, ?, ..., ?) GROUP BY customer_id,
    returning sorted (customer_id, count, rounded sum) tuples like loop_version().
    Build the placeholders with ", ".join("?" * len(gold_ids)) and pass gold_ids as the parameters."""
    return []


# %% Step 1: the loop, as written, with no index
# TODO 1: print the EXPLAIN QUERY PLAN of PER_CUSTOMER for gold_ids[0], then time loop_version()
#         with best_ms and keep its rows in loop_rows.
loop_rows = None

# %% Step 2: one grouped query, still no index
# TODO 2: finish one_query_version() above, time it, and print whether its rows equal loop_rows.

# %% Step 3: index the column the loop searches by, and measure both again
# TODO 3: CREATE INDEX IF NOT EXISTS idx_orders_customer_id ON orders (customer_id); commit;
#         print the new plan; time both versions again; check all answers are still equal.

# %% Step 4: the result, as a table, and what to say
# TODO 4: a DataFrame of the rows, a short describe() of orders and spent, and two sentences:
#         which fix would you keep on a server database, and why?
if loop_rows is None:
    print("TODO 1-4 not done yet: loop_rows is None.")
conn.close()
