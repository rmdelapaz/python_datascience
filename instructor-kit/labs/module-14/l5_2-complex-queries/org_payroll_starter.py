# --- lab bootstrap: find labs_paths.py (the same three lines open every lab; see labs/README.md) ---
import pathlib, sys
sys.path[:0] = [str(p) for p in pathlib.Path(globals().get("__file__", "lab.py")).resolve().parents if (p / "labs_paths.py").is_file()]
from labs_paths import DATA

# %% [markdown]
# # Lab 5.2-C · Payroll under each VP, and three NULL checks (STARTER)
# Finance asks: "How many people, and how much salary, sit under each of the CEO's direct
# reports, however deep the tree goes?" That needs a recursive CTE that remembers which
# branch every employee belongs to.
# The second half is three short NULL checks on `products` (8 products have no rating,
# 14 have no weight).
#
# Skills: self join, WITH RECURSIVE (anchor, UNION ALL, recursive part), carrying a value
# down the tree, IS NULL, COALESCE, and why NOT IN is risky.
#
# Expected when you finish: the CEO's four direct reports, one row per branch with people,
# depth and payroll, a check that 54 of 55 employees are in exactly one branch, and three
# small tables that each show one NULL surprise.

# %% Setup (done for you)
import sqlite3
import pandas as pd

conn = sqlite3.connect((DATA / "pinecrest.db").as_uri() + "?mode=ro", uri=True)


def show(sql, params=()):
    """Run a query and print the result as a table."""
    print(pd.read_sql(sql, conn, params=params).to_string(index=False))


# %% Step 1: one level with a self join - the CEO's direct reports
# TODO 1: join employees (alias e) to employees (alias m) on m.employee_id = e.manager_id and
#         keep the rows whose MANAGER has no manager (m.manager_id IS NULL).
#         Show employee_id, full name, title and the manager's title.

# %% Step 2: every level - a recursive CTE that carries the branch head down the tree
# TODO 2: write BRANCH_CTE = """ WITH RECURSIVE branch (employee_id, salary, head, depth) AS ( ... ) """
#         anchor:         the rows from Step 1, with head = their own full name and depth 0
#         UNION ALL
#         recursive part: employees whose manager_id is already in branch; they INHERIT
#                         branch.head and get branch.depth + 1
#         Then: per head, COUNT(*), MAX(depth) and SUM(salary), largest payroll first.
BRANCH_CTE = ""

# %% Step 3: check the tree - everyone except the CEO is in exactly one branch
# TODO 3: from branch, compare COUNT(*) and COUNT(DISTINCT employee_id) with the 55 rows of
#         employees. Whose salary is not in any branch?

# %% Step 4: NULL check 1 - a condition and its opposite do not add up
# TODO 4: from products: COUNT(*), SUM(rating >= 4.0), SUM(rating < 4.0), SUM(rating IS NULL),
#         COUNT(rating). Which of these add up to 242, and which do not?

# %% Step 5: NULL check 2 - aggregates skip NULL, COALESCE does not
# TODO 5: AVG(weight_kg) against AVG(COALESCE(weight_kg, 0)). Which one would you report, and why?

# %% Step 6: NULL check 3 - NOT IN with a NULL in the list
# TODO 6: count employees who manage nobody, first with NOT IN (SELECT manager_id FROM employees),
#         then with NOT EXISTS. Explain the first result in one comment line.
if not BRANCH_CTE:
    print("TODO 1-6 not done yet: BRANCH_CTE is empty.")
conn.close()
