# --- lab bootstrap: find labs_paths.py (the same three lines open every lab; see labs/README.md) ---
import pathlib, sys
sys.path[:0] = [str(p) for p in pathlib.Path(globals().get("__file__", "lab.py")).resolve().parents if (p / "labs_paths.py").is_file()]
from labs_paths import DATA

# %% [markdown]
# # Lab 5.1-A · The staff report (SOLUTION)
# The people team wants a quick picture of Pinecrest's 55 employees. The `employees`
# table exists only in the database, so there is no CSV to fall back on.
# Questions: What columns does the table have? Who was hired first? How many people and
# how much payroll does each department have? Which locations have at least 8 people?
#
# Skills: connect, list tables and columns, cursors and rows, SELECT with WHERE,
# ORDER BY and LIMIT, aggregates, GROUP BY and HAVING.
#
# Reference solution. Do not hand out before the lab.

# %% Setup (done for you): a READ-ONLY connection, so the shipped database cannot change
import sqlite3
import pandas as pd

db_uri = (DATA / "pinecrest.db").as_uri() + "?mode=ro"
conn = sqlite3.connect(db_uri, uri=True)


def show(sql, params=()):
    """Run a query and print the result as a table (the helper from Lesson 5.1)."""
    print(pd.read_sql(sql, conn, params=params).to_string(index=False))


# %% Step 1: what is in the table?
for row in conn.execute("PRAGMA table_info(employees)"):
    print(row)
print("rows:", conn.execute("SELECT COUNT(*) FROM employees").fetchone()[0])

# %% Step 2: a cursor, one row at a time - the three longest-serving employees
print()
cur = conn.execute("""
    SELECT first_name, last_name, title, hire_date
    FROM employees
    ORDER BY hire_date, employee_id
    LIMIT 3
""")
print([col[0] for col in cur.description])
first = cur.fetchone()
print("fetchone:", first)
print("fetchall:", cur.fetchall())
print("fetchone again:", cur.fetchone())

# %% Step 3: filter and sort - store staff earning 60,000 or more
print()
show("""
    SELECT first_name || ' ' || last_name AS employee, title, location, salary
    FROM employees
    WHERE department = 'Retail'
      AND location IN ('Boise', 'Bend', 'Flagstaff', 'Asheville')
      AND salary >= 60000
    ORDER BY salary DESC, last_name
""")

# %% Step 4: one row per department
print()
show("""
    SELECT department,
           COUNT(*)              AS people,
           SUM(salary)           AS payroll,
           ROUND(AVG(salary), 0) AS avg_salary,
           MIN(hire_date)        AS first_hire
    FROM employees
    GROUP BY department
    ORDER BY payroll DESC
""")

# %% Step 5: filter the GROUPS - locations with at least 8 people
print()
show("""
    SELECT location,
           COUNT(*)              AS people,
           ROUND(AVG(salary), 0) AS avg_salary
    FROM employees
    GROUP BY location
    HAVING COUNT(*) >= 8
    ORDER BY people DESC, location
""")

# %% Step 6: the same question in pandas, as a check
print()
employees = pd.read_sql("SELECT * FROM employees", conn)
check = employees.groupby("department")["salary"].agg(["count", "sum"]).sort_values("sum", ascending=False)
print(check.to_string())
conn.close()
