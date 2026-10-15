# --- lab bootstrap: find labs_paths.py (the same three lines open every lab; see labs/README.md) ---
import pathlib, sys
sys.path[:0] = [str(p) for p in pathlib.Path(globals().get("__file__", "lab.py")).resolve().parents if (p / "labs_paths.py").is_file()]
from labs_paths import DATA

# %% [markdown]
# # Lab 5.1-A · The staff report (STARTER)
# The people team wants a quick picture of Pinecrest's 55 employees. The `employees`
# table exists only in the database, so there is no CSV to fall back on.
# Questions: What columns does the table have? Who was hired first? How many people and
# how much payroll does each department have? Which locations have at least 8 people?
#
# Skills: connect, list tables and columns, cursors and rows, SELECT with WHERE,
# ORDER BY and LIMIT, aggregates, GROUP BY and HAVING.
#
# Expected when you finish: the ten columns of the table and its row count, three rows read
# through a cursor, a filtered list of store staff, one row per department, and the
# locations with at least 8 people.

# %% Setup (done for you): a READ-ONLY connection, so the shipped database cannot change
import sqlite3
import pandas as pd

db_uri = (DATA / "pinecrest.db").as_uri() + "?mode=ro"
conn = sqlite3.connect(db_uri, uri=True)


def show(sql, params=()):
    """Run a query and print the result as a table (the helper from Lesson 5.1)."""
    print(pd.read_sql(sql, conn, params=params).to_string(index=False))


# %% Step 1: what is in the table?
# TODO 1: loop over conn.execute("PRAGMA table_info(employees)") and print each row.
#         Then print the number of rows with SELECT COUNT(*) ... .fetchone()[0].

# %% Step 2: a cursor, one row at a time - the three longest-serving employees
# TODO 2: run a query for first_name, last_name, title, hire_date, ordered by hire_date
#         (then employee_id), LIMIT 3. Keep the cursor in `cur`.
#         Print the column names from cur.description, then cur.fetchone(), then cur.fetchall(),
#         then cur.fetchone() once more. Predict that last line before you run it.
cur = None

# %% Step 3: filter and sort - store staff earning 60,000 or more
# TODO 3: with show(), list employee (first || ' ' || last), title, location and salary for the
#         Retail department, in the four store locations only (not HQ), with salary >= 60000,
#         highest salary first.

# %% Step 4: one row per department
# TODO 4: department, number of people, total salary (payroll), average salary rounded to 0
#         decimals, and the earliest hire_date. Largest payroll first.

# %% Step 5: filter the GROUPS - locations with at least 8 people
# TODO 5: location, people and average salary, only for locations with at least 8 people.
#         Which clause holds the "at least 8" condition, and why can it not be WHERE?

# %% Step 6: the same question in pandas, as a check
# TODO 6: employees = pd.read_sql("SELECT * FROM employees", conn), then the groupby that
#         reproduces Step 4's people and payroll columns. Do the numbers match?
if cur is None:
    print("TODO 1-6 not done yet: `cur` is still None.")
conn.close()
