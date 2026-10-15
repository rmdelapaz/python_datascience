# --- lab bootstrap: find labs_paths.py (the same three lines open every lab; see labs/README.md) ---
import pathlib, sys
sys.path[:0] = [str(p) for p in pathlib.Path(globals().get("__file__", "lab.py")).resolve().parents if (p / "labs_paths.py").is_file()]
from labs_paths import DATA, OUTPUT

# %% [markdown]
# # Lab 5.1-C · Save a summary table (STARTER)
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
# Expected when you finish: a five-row summary (one per location), a below_pct column,
# `rows written: 5`, the location(s) with the highest share below the reorder point, an
# IntegrityError you caused on purpose with the row count unchanged (1210), and proof that
# the shipped database has no stock_summary table.

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
# TODO 1: write SUMMARY_SQL = text("""...""") that returns, per location: skus (COUNT(*)),
#         units (SUM(quantity)), below_reorder (SUM(quantity < reorder_point)) and
#         out_of_stock (SUM(quantity = 0)), for rows with last_counted >= :since.
#         Read it with pd.read_sql(SUMMARY_SQL, conn, params={"since": "2025-12-01"})
#         inside `with engine.connect() as conn:`.
summary = None

# %% Step 2: finish it in pandas
# TODO 2: add summary["below_pct"] = share of SKUs below their reorder point, in percent, 1 decimal.

# %% Step 3: save it as a table, then read it back with SQL
# TODO 3: summary.to_sql("stock_summary", engine, if_exists="replace", index=False) and print what
#         it returns. Then query stock_summary for the location(s) with the highest below_pct.

# %% Step 4: a transaction is all or nothing
# TODO 4: inside `with engine.begin() as conn:` insert two rows into inventory:
#         ("TNT-1001", "Popup Stand", 4, 2, "2025-12-31")   - a new location, fine by itself
#         ("TNT-1001", "Boise", 9, 3, "2025-12-31")         - breaks the primary key (sku, location)
#         Catch sqlalchemy.exc.IntegrityError. Count the rows in inventory before and after,
#         and count the "Popup Stand" rows. Predict all three numbers first.

# %% Step 5: the original is untouched
# TODO 5: engine.dispose(), then open the SHIPPED database read-only with sqlite3 and check that
#         sqlite_master has no row named 'stock_summary'.
if summary is None:
    print("TODO 1-5 not done yet: `summary` is still None.")
engine.dispose()
