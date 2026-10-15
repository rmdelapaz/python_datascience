# --- lab bootstrap: find labs_paths.py (the same three lines open every lab; see labs/README.md) ---
import pathlib, sys
sys.path[:0] = [str(p) for p in pathlib.Path(globals().get("__file__", "lab.py")).resolve().parents if (p / "labs_paths.py").is_file()]
from labs_paths import DATA

# %% [markdown]
# # Lab 5.1-B · A safe stock lookup (SOLUTION)
# Store managers want to type a location and a number and get back the products that are
# running low there. Whatever they type goes into a query, so the query must be safe.
# Question: which SKUs at a given location have a quantity at or below a given number?
#
# The `inventory` table: sku, location (four stores and 'Warehouse'), quantity,
# reorder_point, last_counted. One row per product per location (1,210 rows).
#
# Skills: ? and :name placeholders, a one-item tuple, why f-strings are dangerous,
# and checking a column name against an allowed list.
#
# Reference solution. Do not hand out before the lab.

# %% Setup (done for you)
import sqlite3
import pandas as pd

conn = sqlite3.connect((DATA / "pinecrest.db").as_uri() + "?mode=ro", uri=True)


def count_low_unsafe(location, max_qty):
    """DO NOT copy this: the values are pasted into the SQL text."""
    sql = f"SELECT COUNT(*) FROM inventory WHERE location = '{location}' AND quantity <= {max_qty}"
    return conn.execute(sql).fetchone()[0]


# %% Step 1: the same count, with placeholders
def count_low(location, max_qty):
    sql = "SELECT COUNT(*) FROM inventory WHERE location = ? AND quantity <= ?"
    return conn.execute(sql, (location, max_qty)).fetchone()[0]


print("Boise, quantity <= 0:  unsafe", count_low_unsafe("Boise", 0), "| safe", count_low("Boise", 0))
print("Warehouse, quantity <= 5:  unsafe", count_low_unsafe("Warehouse", 5), "| safe", count_low("Warehouse", 5))

# %% Step 2: attack both functions with the same input
sneaky = "nowhere' OR '1'='1' --"
print()
print("crafted input, unsafe:", count_low_unsafe(sneaky, 0), "(every row in the table)")
print("crafted input, safe:  ", count_low(sneaky, 0), "(no location has that odd name)")
print("rows in inventory:    ", conn.execute("SELECT COUNT(*) FROM inventory").fetchone()[0])

# %% Step 3: a one-item tuple
print()
n_locations = conn.execute("SELECT COUNT(*) FROM inventory WHERE sku = ?", ("TNT-1001",)).fetchone()[0]
print("rows for TNT-1001:", n_locations)
try:
    conn.execute("SELECT COUNT(*) FROM inventory WHERE sku = ?", "TNT-1001")
except sqlite3.ProgrammingError as e:
    print("ProgrammingError:", e)

# %% Step 4: the lookup the managers asked for, with named placeholders and a safe sort
ALLOWED_SORT = {"quantity", "sku", "last_counted"}


def low_stock(location, max_qty, sort_by="quantity"):
    """SKUs at one location with quantity <= max_qty, as a DataFrame."""
    if sort_by not in ALLOWED_SORT:                      # a placeholder cannot stand for a column name
        raise ValueError(f"sort_by must be one of {sorted(ALLOWED_SORT)}")
    sql = f"""
        SELECT sku, quantity, reorder_point, last_counted
        FROM inventory
        WHERE location = :location AND quantity <= :max_qty
        ORDER BY {sort_by}, sku
    """
    return pd.read_sql(sql, conn, params={"location": location, "max_qty": max_qty},
                       parse_dates=["last_counted"])


found = low_stock("Flagstaff", 0, sort_by="last_counted")
print()
print("Flagstaff, out of stock:", len(found), "SKUs")
print(found.head(4).to_string(index=False))
print("last_counted dtype:", found["last_counted"].dtype)
try:
    low_stock("Flagstaff", 0, sort_by="quantity; DROP TABLE inventory")
except ValueError as e:
    print("ValueError:", e)
conn.close()
