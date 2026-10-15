# --- lab bootstrap: find labs_paths.py (the same three lines open every lab; see labs/README.md) ---
import pathlib, sys
sys.path[:0] = [str(p) for p in pathlib.Path(globals().get("__file__", "lab.py")).resolve().parents if (p / "labs_paths.py").is_file()]
from labs_paths import DATA

# %% [markdown]
# # Lab 5.3-A · Pay within each location (STARTER)
# The people team asks three things about the 55 employees, location by location:
#   1. How does each person's salary compare with the average at their location?
#   2. What share of the location's payroll does each person earn?
#   3. Who are the two highest-paid people at each location?
# Every answer must keep one row per employee (or per top earner), so this is window work,
# not GROUP BY work.
#
# Skills: AVG/SUM ... OVER (PARTITION BY ...), RANK against DENSE_RANK, top N per group with a
# CTE, and the pandas check (transform, rank, groupby().head()).
#
# Expected when you finish: Boise's ten employees next to the location average (43,950); the same
# ten with their share of payroll and two rank columns that disagree after a tie; a 12-row table
# of the top two earners at each of the 6 locations; and a line saying pandas agrees.

# %% Setup (done for you)
import sqlite3
import pandas as pd

conn = sqlite3.connect((DATA / "pinecrest.db").as_uri() + "?mode=ro", uri=True)


def show(sql, params=()):
    """Run a query and print the result as a table."""
    print(pd.read_sql(sql, conn, params=params).to_string(index=False))


# %% Step 1: every employee next to their location's average (one row per employee)
# TODO 1: for location = 'Boise': location, full name, salary, the location's average salary
#         (AVG(salary) OVER (PARTITION BY location), rounded) and the difference. Highest salary first.
#         How many rows come back? How many would GROUP BY location give?

# %% Step 2: share of the location's payroll, and ties in the ranking
# TODO 2: still Boise: add pct_of_payroll (100.0 * salary / SUM(salary) OVER (PARTITION BY location)),
#         RANK() and DENSE_RANK() over the same partition ordered by salary DESC.
#         Find the tie. Where do the two rank columns start to disagree, and why?

# %% Step 3: top two earners at every location (number, wrap, filter)
# TODO 3: in a CTE, number the employees with ROW_NUMBER() OVER (PARTITION BY location
#         ORDER BY salary DESC, employee_id); outside it keep rn <= 2. Store the SQL in TOP2_SQL.
#         Why can the rn <= 2 filter not go in the same SELECT as ROW_NUMBER()?
TOP2_SQL = ""

# %% Step 4: the same three answers in pandas
# TODO 4: read employees into a DataFrame and reproduce Step 1 with groupby().transform("mean"),
#         Step 2's share with transform("sum"), and Step 3 with sort_values + groupby().head(2).
if not TOP2_SQL:
    print("TODO 1-4 not done yet: TOP2_SQL is empty.")
conn.close()
