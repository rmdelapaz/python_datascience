# --- lab bootstrap: find labs_paths.py (the same three lines open every lab; see labs/README.md) ---
import pathlib, sys
sys.path[:0] = [str(p) for p in pathlib.Path(globals().get("__file__", "lab.py")).resolve().parents if (p / "labs_paths.py").is_file()]
from labs_paths import DATA, OUTPUT

# %% [markdown]
# # Lab 5.4-A · Plans for a customer lookup screen (SOLUTION)
# The support team's new screen finds customers by STATE and CITY, and lists a city's
# customers newest sign-up first. Before anyone adds an index "to be safe", read the plans,
# predict, add ONE composite index, read the plans again, then drop it and check that the
# plan really goes back.
#
# This lab creates an index, so it works on a COPY in the OUTPUT folder.
# The connection uses cached_statements=0 so that a plan asked for again after DROP INDEX
# is planned afresh (Lesson 5.4, "Two Details in That Setup").
# Timings are printed for you to look at. Your numbers will differ; nothing depends on them.
#
# Reference solution. Do not hand out before the lab.

# %% Setup (done for you): a copy, a plan printer, a stopwatch
import shutil
import sqlite3
import time

work_db = OUTPUT / "pinecrest_plans.db"
shutil.copy(DATA / "pinecrest.db", work_db)
conn = sqlite3.connect(work_db, cached_statements=0)


def plan(sql, params=()):
    """Print the query plan, one step per line (the helper from Lesson 5.4, without nesting)."""
    for row in conn.execute("EXPLAIN QUERY PLAN " + sql, params):
        print("   ", row[3])


def timed(sql, param_list, repeat=5):
    """Best time in milliseconds to run the query once for every item of param_list."""
    best = float("inf")
    for _ in range(repeat):
        start = time.perf_counter()
        for params in param_list:
            conn.execute(sql, params).fetchall()
        best = min(best, time.perf_counter() - start)
    return best * 1000


BY_CITY = "SELECT customer_id, last_name FROM customers WHERE state = ? AND city = ?"
CITY_ONLY = "SELECT customer_id FROM customers WHERE city = ?"
NEWEST = "SELECT customer_id, signup_date FROM customers WHERE state = ? AND city = ? ORDER BY signup_date DESC"
lookups = [("ID", "Boise"), ("OR", "Bend"), ("NC", "Asheville"), ("AZ", "Flagstaff")] * 50   # 200 lookups

# %% Step 1: the plans with no index (predict first: SCAN or SEARCH?)
for label, sql, params in [("state and city", BY_CITY, ("ID", "Boise")),
                           ("city only", CITY_ONLY, ("Boise",)),
                           ("state and city, newest first", NEWEST, ("ID", "Boise"))]:
    print(label)
    plan(sql, params)
before = timed(BY_CITY, lookups)
answer_before = conn.execute(BY_CITY, ("ID", "Boise")).fetchall()

# %% Step 2: one composite index, equality columns first
conn.execute("CREATE INDEX IF NOT EXISTS idx_customers_state_city ON customers (state, city)")
conn.commit()
print()
for label, sql, params in [("state and city", BY_CITY, ("ID", "Boise")),
                           ("city only", CITY_ONLY, ("Boise",)),
                           ("state and city, newest first", NEWEST, ("ID", "Boise"))]:
    print(label)
    plan(sql, params)
after = timed(BY_CITY, lookups)
print(f"\n200 lookups: {before:.1f} ms before, {after:.1f} ms after (your numbers will differ)")
print("same answer:", sorted(answer_before) == sorted(conn.execute(BY_CITY, ("ID", "Boise")).fetchall()),
      "|", len(answer_before), "customers in Boise, ID")

# %% Step 3: a three-column index removes the sort step as well
conn.execute("CREATE INDEX IF NOT EXISTS idx_customers_state_city_signup ON customers (state, city, signup_date)")
conn.commit()
print()
print("state and city, newest first, with (state, city, signup_date):")
plan(NEWEST, ("ID", "Boise"))

# %% Step 4: drop both indexes and confirm the plan really goes back
conn.execute("DROP INDEX idx_customers_state_city")
conn.execute("DROP INDEX idx_customers_state_city_signup")
conn.commit()
print()
print("after DROP INDEX:")
plan(BY_CITY, ("ID", "Boise"))
left = conn.execute("SELECT COUNT(*) FROM sqlite_master WHERE type = 'index' AND name LIKE 'idx_%'").fetchone()[0]
print("indexes named idx_... left in the copy:", left)
conn.close()
