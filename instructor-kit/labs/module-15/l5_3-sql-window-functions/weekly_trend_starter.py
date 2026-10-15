# --- lab bootstrap: find labs_paths.py (the same three lines open every lab; see labs/README.md) ---
import pathlib, sys
sys.path[:0] = [str(p) for p in pathlib.Path(globals().get("__file__", "lab.py")).resolve().parents if (p / "labs_paths.py").is_file()]
from labs_paths import DATA

# %% [markdown]
# # Lab 5.3-C · Online orders week by week (STARTER)
# The e-commerce team watches the number of ONLINE orders each week of 2025. They want, for
# every week: the change from the week before, a four-week moving average, and a flag for
# weeks that beat the average of the four weeks BEFORE them by more than 25%.
#
# Skills: LAG, frames (ROWS BETWEEN n PRECEDING AND CURRENT ROW / AND 1 PRECEDING),
# the partial-frame difference between SQL and pandas, NTILE, and a pandas check.
#
# Expected when you finish: a 51-row weekly table (first rows shown) with change, avg_4wk,
# weeks_in_frame and prior_4wk; the weeks more than 25% above their prior four-week average and
# their dates; two near-zero differences against pandas; and a quartile table from NTILE.

# %% Setup (done for you)
import sqlite3
import pandas as pd

conn = sqlite3.connect((DATA / "pinecrest.db").as_uri() + "?mode=ro", uri=True)

WEEKLY = """
    WITH weekly AS (
        SELECT strftime('%W', order_date) AS week,       -- weeks start on Monday; week 00 is partial
               COUNT(*)                   AS orders
        FROM orders
        WHERE channel = 'online' AND order_date >= '2025-01-06' AND order_date < '2025-12-29'
        GROUP BY week
    )
"""

# %% Step 1: change from last week and a four-week moving average
# TODO 1: from WEEKLY, select week, orders and
#           change         = orders - LAG(orders) OVER (ORDER BY week)
#           avg_4wk        = AVG(orders) over ROWS BETWEEN 3 PRECEDING AND CURRENT ROW (round to 1)
#           weeks_in_frame = COUNT(*) over the same frame
#           prior_4wk      = AVG(orders) over ROWS BETWEEN 4 PRECEDING AND 1 PRECEDING (round to 1)
#         Read it into `trend` with pd.read_sql and print the first five rows.
#         Why is prior_4wk empty in week 01, and why is avg_4wk NOT empty there?
trend = None

# %% Step 2: weeks that beat their own recent past by more than 25%
# TODO 2: trend["vs_prior_pct"] = 100 * (orders / prior_4wk - 1); show the weeks above 25.
#         Week 01 starts on Monday 2025-01-06: what dates are the spike weeks, and what happened?

# %% Step 3: check the frames against pandas
# TODO 3: rolling(4, min_periods=1).mean() should equal avg_4wk, and shift(1).rolling(4, min_periods=1)
#         should equal prior_4wk (compare the unrounded values). What does rolling(4) without
#         min_periods give in the first three rows?

# %% Step 4: quartiles of weeks with NTILE
# TODO 4: NTILE(4) OVER (ORDER BY orders) in a second CTE, then weeks, fewest and most per quartile.
if trend is None:
    print("TODO 1-4 not done yet: `trend` is None.")
conn.close()
