# --- lab bootstrap: find labs_paths.py (the same three lines open every lab; see labs/README.md) ---
import pathlib, sys
sys.path[:0] = [str(p) for p in pathlib.Path(globals().get("__file__", "lab.py")).resolve().parents if (p / "labs_paths.py").is_file()]
from labs_paths import DATA, OUTPUT

# %% [markdown]
# # Lab 5.4-A · Plans for a customer lookup screen (STARTER)
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
# Expected when you finish: three plans with no index (all SCAN, one with a TEMP B-TREE), the same
# three plans after one composite index, a before/after timing and "same answer: True", a plan
# with no sort step after a three-column index, and SCAN again after DROP INDEX.

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
# TODO 1: write your three predictions in a comment, then call plan() for BY_CITY ("ID", "Boise"),
#         CITY_ONLY ("Boise",) and NEWEST ("ID", "Boise"). Time BY_CITY over `lookups` with timed()
#         and keep the Boise answer in answer_before.
answer_before = None

# %% Step 2: one composite index, equality columns first
# TODO 2: CREATE INDEX IF NOT EXISTS idx_customers_state_city ON customers (state, city); commit;
#         plan the three queries again. Which one still scans, and why (leftmost prefix)?
#         Time BY_CITY again and check that the answer is the same rows.
#         The gain is modest: about one customer in ten lives in Boise. What does that say?

# %% Step 3: a three-column index removes the sort step as well
# TODO 3: add an index on (state, city, signup_date) and plan NEWEST again. What disappeared?

# %% Step 4: drop both indexes and confirm the plan really goes back
# TODO 4: DROP INDEX both, commit, and plan BY_CITY once more. (This works because the connection
#         was opened with cached_statements=0.)
if answer_before is None:
    print("TODO 1-4 not done yet: answer_before is None.")
conn.close()
