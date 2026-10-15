# --- lab bootstrap: find labs_paths.py (the same three lines open every lab; see labs/README.md) ---
import pathlib, sys
sys.path[:0] = [str(p) for p in pathlib.Path(globals().get("__file__", "lab.py")).resolve().parents if (p / "labs_paths.py").is_file()]
from labs_paths import DATA, OUTPUT

# %% [markdown]
# # Lab 5.1-C · Save a summary table (SOLUTION)
# The warehouse lead wants one small table, `stock_summary`, that a dashboard can read:
# for every location, how many SKUs it holds, how many units, and how many SKUs are below
# their reorder point. You will build it with SQL, finish it in pandas, save it back to
# the database with to_sql, and watch a transaction roll back.
#
# This lab WRITES, so it works on a copy of the database in the OUTPUT folder.
# The shipped data/pinecrest.db is never opened for writing.
#
# Skills: a working copy, a SQLAlchemy engine, text() with :name parameters, pd.read_sql,
# DataFrame.to_sql, engine.begin() and rollback.
#
# Reference solution. Do not hand out before the lab.

# %% Setup (done for you): copy the database, then open the COPY
import shutil
import pandas as pd
from sqlalchemy import create_engine, inspect, text
from sqlalchemy.exc import IntegrityError

work_db = OUTPUT / "pinecrest_work.db"
shutil.copy(DATA / "pinecrest.db", work_db)
engine = create_engine(f"sqlite:///{work_db.as_posix()}")
print("dialect:", engine.dialect.name, "| tables:", inspect(engine).get_table_names())

# %% Step 1: let the database do the grouping
SUMMARY_SQL = text("""
    SELECT location,
           COUNT(*)                      AS skus,
           SUM(quantity)                 AS units,
           SUM(quantity < reorder_point) AS below_reorder,
           SUM(quantity = 0)             AS out_of_stock
    FROM inventory
    WHERE last_counted >= :since
    GROUP BY location
    ORDER BY units DESC
""")
with engine.connect() as conn:
    summary = pd.read_sql(SUMMARY_SQL, conn, params={"since": "2025-12-01"})
print()
print(summary.to_string(index=False))

# %% Step 2: finish it in pandas
summary["below_pct"] = (summary["below_reorder"] / summary["skus"] * 100).round(1)
print()
print(summary[["location", "below_reorder", "below_pct"]].to_string(index=False))

# %% Step 3: save it as a table, then read it back with SQL
rows = summary.to_sql("stock_summary", engine, if_exists="replace", index=False)
print()
print("rows written:", rows)
with engine.connect() as conn:
    worst = conn.execute(text("""
        SELECT location, below_pct FROM stock_summary
        WHERE below_pct = (SELECT MAX(below_pct) FROM stock_summary)
        ORDER BY location
    """)).all()
print("highest share below reorder point:", [(r.location, r.below_pct) for r in worst])
print("tables now:", inspect(engine).get_table_names())

# %% Step 4: a transaction is all or nothing
# Both inserts are in ONE transaction. The second breaks the primary key of inventory
# (sku, location), so the first is rolled back too.
count_sql = text("SELECT COUNT(*) FROM inventory")
with engine.connect() as conn:
    before = conn.execute(count_sql).scalar()
try:
    with engine.begin() as conn:
        insert = text("INSERT INTO inventory VALUES (:sku, :location, :quantity, :reorder_point, :last_counted)")
        conn.execute(insert, {"sku": "TNT-1001", "location": "Popup Stand", "quantity": 4,
                              "reorder_point": 2, "last_counted": "2025-12-31"})
        conn.execute(insert, {"sku": "TNT-1001", "location": "Boise", "quantity": 9,
                              "reorder_point": 3, "last_counted": "2025-12-31"})      # duplicate key
except IntegrityError as e:
    print()
    print("IntegrityError:", str(e.orig))
with engine.connect() as conn:
    after = conn.execute(count_sql).scalar()
    popup = conn.execute(text("SELECT COUNT(*) FROM inventory WHERE location = :loc"), {"loc": "Popup Stand"}).scalar()
print("inventory rows before:", before, "| after:", after, "| Popup Stand rows:", popup)

# %% Step 5: the original is untouched
engine.dispose()
import sqlite3
original = sqlite3.connect((DATA / "pinecrest.db").as_uri() + "?mode=ro", uri=True)
has_table = original.execute("SELECT COUNT(*) FROM sqlite_master WHERE name = 'stock_summary'").fetchone()[0]
original.close()
print()
print("stock_summary in the shipped database:", bool(has_table), "| in the working copy: True")
