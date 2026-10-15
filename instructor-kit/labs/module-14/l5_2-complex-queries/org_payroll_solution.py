# --- lab bootstrap: find labs_paths.py (the same three lines open every lab; see labs/README.md) ---
import pathlib, sys
sys.path[:0] = [str(p) for p in pathlib.Path(globals().get("__file__", "lab.py")).resolve().parents if (p / "labs_paths.py").is_file()]
from labs_paths import DATA

# %% [markdown]
# # Lab 5.2-C · Payroll under each VP, and three NULL checks (SOLUTION)
# Finance asks: "How many people, and how much salary, sit under each of the CEO's direct
# reports, however deep the tree goes?" That needs a recursive CTE that remembers which
# branch every employee belongs to.
# The second half is three short NULL checks on `products` (8 products have no rating,
# 14 have no weight).
#
# Skills: self join, WITH RECURSIVE (anchor, UNION ALL, recursive part), carrying a value
# down the tree, IS NULL, COALESCE, and why NOT IN is risky.
#
# Reference solution. Do not hand out before the lab.

# %% Setup (done for you)
import sqlite3
import pandas as pd

conn = sqlite3.connect((DATA / "pinecrest.db").as_uri() + "?mode=ro", uri=True)


def show(sql, params=()):
    """Run a query and print the result as a table."""
    print(pd.read_sql(sql, conn, params=params).to_string(index=False))


# %% Step 1: one level with a self join - the CEO's direct reports
show("""
    SELECT e.employee_id,
           e.first_name || ' ' || e.last_name AS employee,
           e.title,
           m.title                            AS reports_to
    FROM employees AS e
    JOIN employees AS m ON m.employee_id = e.manager_id
    WHERE m.manager_id IS NULL
    ORDER BY e.employee_id
""")

# %% Step 2: every level - a recursive CTE that carries the branch head down the tree
BRANCH_CTE = """
    WITH RECURSIVE branch (employee_id, salary, head, depth) AS (
        -- anchor: the CEO's direct reports, each the head of a branch
        SELECT e.employee_id, e.salary, e.first_name || ' ' || e.last_name, 0
        FROM employees AS e
        JOIN employees AS m ON m.employee_id = e.manager_id
        WHERE m.manager_id IS NULL
        UNION ALL
        -- recursive part: people whose manager is already in a branch inherit its head
        SELECT e.employee_id, e.salary, branch.head, branch.depth + 1
        FROM employees AS e
        JOIN branch ON e.manager_id = branch.employee_id
    )
"""
print()
show(BRANCH_CTE + """
    SELECT head,
           COUNT(*)    AS people_including_head,
           MAX(depth)  AS levels_below,
           SUM(salary) AS payroll
    FROM branch
    GROUP BY head
    ORDER BY payroll DESC
""")

# %% Step 3: check the tree - everyone except the CEO is in exactly one branch
print()
show(BRANCH_CTE + """
    SELECT (SELECT COUNT(*) FROM employees)             AS employees,
           COUNT(*)                                     AS in_a_branch,
           COUNT(DISTINCT employee_id)                  AS distinct_people,
           (SELECT SUM(salary) FROM employees) - SUM(salary) AS salary_not_in_a_branch
    FROM branch
""")

# %% Step 4: NULL check 1 - a condition and its opposite do not add up
print()
show("""
    SELECT COUNT(*)                AS products,
           SUM(rating >= 4.0)      AS rated_4_or_more,
           SUM(rating < 4.0)       AS rated_below_4,
           SUM(rating IS NULL)     AS no_rating,
           COUNT(rating)           AS count_rating
    FROM products
""")

# %% Step 5: NULL check 2 - aggregates skip NULL, COALESCE does not
print()
show("""
    SELECT ROUND(AVG(weight_kg), 3)              AS avg_weight_known,
           ROUND(AVG(COALESCE(weight_kg, 0)), 3) AS avg_with_zero_filled,
           COUNT(weight_kg)                      AS with_weight,
           COUNT(*)                              AS all_products
    FROM products
""")

# %% Step 6: NULL check 3 - NOT IN with a NULL in the list
print()
show("""
    SELECT (SELECT COUNT(*) FROM employees
            WHERE employee_id NOT IN (SELECT manager_id FROM employees))          AS not_in,
           (SELECT COUNT(*) FROM employees AS e
            WHERE NOT EXISTS (SELECT 1 FROM employees AS x
                              WHERE x.manager_id = e.employee_id))                AS not_exists,
           (SELECT COUNT(DISTINCT manager_id) FROM employees)                     AS managers
""")
conn.close()
