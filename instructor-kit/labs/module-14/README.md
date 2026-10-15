# Session 14 labs · SQL from Python: Queries and Joins (Lessons 5.1 + 5.2)

New practice on the two lessons' skills against `pinecrest.db`. The lessons work mostly on
`orders`, `customers` and `products`; these labs lean on the two tables that exist only in the
database, `employees` and `inventory`, so every question is new.

**The shipped database is never written to.** Five of the six labs open it read-only
(`sqlite3.connect((DATA / "pinecrest.db").as_uri() + "?mode=ro", uri=True)`). The one lab that
writes (`save_summary`) copies the file to `OUTPUT` first and works on the copy.

| Lab | Practices | Where | Minutes | Expected output (solution) |
|-----|-----------|-------|---------|----------------------------|
| `l5_1-database-connections/staff_report_*.py` | `PRAGMA table_info`, cursors (`fetchone`, `fetchall`), `WHERE`, `ORDER BY`, `LIMIT`, aggregates, `GROUP BY`, `HAVING`, a pandas check | room | 12 | 10 columns, 55 rows; first hire Clara Soto 2016-02-01; four store managers at 60,000 or more; Retail 36 people / 1,841,600 payroll; locations with 8 or more people: HQ 17, Boise 10, Asheville 8, Bend 8 |
| `l5_1-database-connections/safe_lookup_*.py` | `?` and `:name` placeholders, the one-item tuple, an injection that works on an f-string and fails on a placeholder, an allowed list for a column name | room | 13 | Boise out of stock 65, Warehouse at 5 or fewer 39; crafted input: unsafe 1210, safe 0; "uses 1, and there are 8 supplied"; Flagstaff out of stock 62 SKUs |
| `l5_1-database-connections/save_summary_*.py` | a working copy in `OUTPUT`, SQLAlchemy engine, `text()`, `pd.read_sql`, `to_sql`, `engine.begin()` and rollback | home | 25 | 5 rows written; Warehouse 14,229 units, 20.2% of SKUs below reorder point; Boise and Flagstaff highest at 36.8%; IntegrityError, inventory still 1210 rows; shipped database has no `stock_summary` |
| `l5_2-complex-queries/join_row_counts_*.py` | predicting row counts, `JOIN` against `LEFT JOIN`, `COALESCE`, the anti-join, `NOT EXISTS` | room | 15 | 45,490 lines: inner 44,881, left 45,490; revenue 3,602,058.10 with the inner join against 3,636,286.35 in all (34,228.25 on six discontinued SKUs); Wrenfield is the top brand at 515,811.85 |
| `l5_2-complex-queries/stock_vs_sales_*.py` | the fan-out trap with two "many" sides, CTEs that aggregate before joining, `CASE`, real-number division | room (start) / home | 20 | true totals 30,894 sold and 22,815 on hand; the tempting join gives 154,470 and 3,693,132; Accessories has the thinnest cover (24.3 weeks), Tents the heaviest (70.7) |
| `l5_2-complex-queries/org_payroll_*.py` | self join, `WITH RECURSIVE` carrying a value down the tree, three NULL checks | home (stretch) | 25 | branches: Tamar Kimura 36 people / 1,841,600; Elise Delgado 11 / 753,600; Arjun Silva 6 / 552,500; Zane Laine 1 / 88,600; ratings 164 + 70 + 8 NULL = 242; `NOT IN` returns 0, `NOT EXISTS` 32 |

Hand out the `*_starter.py` files only. Starters run as shipped and say which TODOs are open.

Run one (from the kit folder, or from any folder):

    python labs/module-14/l5_1-database-connections/staff_report_starter.py

Each file is split into `# %%` cells, so it also opens as a notebook in VS Code or Jupyter.

Check all: `python3 labs/check_labs.py module-14` (expect `12 passed, 0 failed`).

Helpers and files these labs create: `show(sql, params=())` (the lesson's helper, defined in each
lab); `count_low`, `low_stock` and `ALLOWED_SORT` (`safe_lookup`); `STOCK_SQL` and `BRANCH_CTE`
(query strings reused inside their labs); `pinecrest_work.db` with a new `stock_summary` table,
written to `OUTPUT` by `save_summary` (an `output/` folder next to the lab, or a temporary
folder when `LABS_OFFLINE=1`).
