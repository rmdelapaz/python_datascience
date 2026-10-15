# --- lab bootstrap: find labs_paths.py (the same three lines open every lab; see labs/README.md) ---
import pathlib, sys
sys.path[:0] = [str(p) for p in pathlib.Path(globals().get("__file__", "lab.py")).resolve().parents if (p / "labs_paths.py").is_file()]
from labs_paths import DATA

# %% [markdown]
# # Lab 5.3-A · Pay within each location (SOLUTION)
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
# Reference solution. Do not hand out before the lab.

# %% Setup (done for you)
import sqlite3
import pandas as pd

conn = sqlite3.connect((DATA / "pinecrest.db").as_uri() + "?mode=ro", uri=True)


def show(sql, params=()):
    """Run a query and print the result as a table."""
    print(pd.read_sql(sql, conn, params=params).to_string(index=False))


# %% Step 1: every employee next to their location's average (one row per employee)
show("""
    SELECT location,
           first_name || ' ' || last_name                            AS employee,
           salary,
           ROUND(AVG(salary) OVER (PARTITION BY location))           AS location_avg,
           ROUND(salary - AVG(salary) OVER (PARTITION BY location))  AS vs_avg
    FROM employees
    WHERE location = 'Boise'
    ORDER BY salary DESC
""")

# %% Step 2: share of the location's payroll, and ties in the ranking
print()
show("""
    SELECT location,
           first_name || ' ' || last_name                                 AS employee,
           salary,
           ROUND(100.0 * salary / SUM(salary) OVER (PARTITION BY location), 1) AS pct_of_payroll,
           RANK()       OVER (PARTITION BY location ORDER BY salary DESC) AS rnk,
           DENSE_RANK() OVER (PARTITION BY location ORDER BY salary DESC) AS dense_rnk
    FROM employees
    WHERE location = 'Boise'
    ORDER BY salary DESC, employee
""")

# %% Step 3: top two earners at every location (number, wrap, filter)
print()
TOP2_SQL = """
    WITH ranked AS (
        SELECT location,
               first_name || ' ' || last_name AS employee,
               title,
               salary,
               ROW_NUMBER() OVER (PARTITION BY location ORDER BY salary DESC, employee_id) AS rn
        FROM employees
    )
    SELECT location, rn, employee, title, salary
    FROM ranked
    WHERE rn <= 2
    ORDER BY location, rn
"""
top2 = pd.read_sql(TOP2_SQL, conn)
print(top2.to_string(index=False))
print("rows:", len(top2), "(6 locations x 2)")

# %% Step 4: the same three answers in pandas
print()
emp = pd.read_sql("SELECT employee_id, first_name || ' ' || last_name AS employee, location, salary FROM employees", conn)
emp["location_avg"] = emp.groupby("location")["salary"].transform("mean").round()
emp["pct_of_payroll"] = (100 * emp["salary"] / emp.groupby("location")["salary"].transform("sum")).round(1)
check = (emp.sort_values(["location", "salary", "employee_id"], ascending=[True, False, True])
            .groupby("location").head(2))
print("pandas top two match SQL:", check["employee"].tolist() == top2["employee"].tolist())
print("Boise average in pandas:", emp.loc[emp["location"] == "Boise", "location_avg"].iloc[0])
conn.close()
