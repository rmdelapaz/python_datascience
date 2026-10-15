# --- lab bootstrap: find labs_paths.py (the same three lines open every lab; see labs/README.md) ---
import pathlib, sys
sys.path[:0] = [str(p) for p in pathlib.Path(globals().get("__file__", "lab.py")).resolve().parents if (p / "labs_paths.py").is_file()]
from labs_paths import DATA

# %% [markdown]
# # Lab 5.3-C · Online orders week by week (SOLUTION)
# The e-commerce team watches the number of ONLINE orders each week of 2025. They want, for
# every week: the change from the week before, a four-week moving average, and a flag for
# weeks that beat the average of the four weeks BEFORE them by more than 25%.
#
# Skills: LAG, frames (ROWS BETWEEN n PRECEDING AND CURRENT ROW / AND 1 PRECEDING),
# the partial-frame difference between SQL and pandas, NTILE, and a pandas check.
#
# Reference solution. Do not hand out before the lab.

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
trend = pd.read_sql(WEEKLY + """
    SELECT week,
           orders,
           orders - LAG(orders) OVER (ORDER BY week)                                     AS change,
           ROUND(AVG(orders) OVER (ORDER BY week ROWS BETWEEN 3 PRECEDING AND CURRENT ROW), 1) AS avg_4wk,
           COUNT(*) OVER (ORDER BY week ROWS BETWEEN 3 PRECEDING AND CURRENT ROW)            AS weeks_in_frame,
           ROUND(AVG(orders) OVER (ORDER BY week ROWS BETWEEN 4 PRECEDING AND 1 PRECEDING), 1) AS prior_4wk
    FROM weekly
    ORDER BY week
""", conn)
print("weeks:", len(trend), "(full Monday-to-Sunday weeks of 2025)")
print(trend.head(5).to_string(index=False))

# %% Step 2: weeks that beat their own recent past by more than 25%
trend["vs_prior_pct"] = (100 * (trend["orders"] / trend["prior_4wk"] - 1)).round(1)
spikes = trend[trend["vs_prior_pct"] > 25]
print()
print(spikes[["week", "orders", "prior_4wk", "vs_prior_pct"]].to_string(index=False))
for week in spikes["week"]:
    monday = pd.Timestamp("2025-01-06") + pd.Timedelta(weeks=int(week) - 1)
    print(f"week {week}: {monday.date()} to {(monday + pd.Timedelta(days=6)).date()}")
print("All three hold a sale weekend (May 23-26, Aug 29-Sep 1, Nov 28-Dec 1): the spikes are the promotions.")

# %% Step 3: check the frames against pandas
# Compare before rounding: SQL ROUND and pandas round can disagree on a value that ends in 5.
s = trend["orders"]
sql_avg = pd.read_sql(WEEKLY + "SELECT AVG(orders) OVER (ORDER BY week ROWS BETWEEN 3 PRECEDING AND CURRENT ROW) AS a, "
                      "AVG(orders) OVER (ORDER BY week ROWS BETWEEN 4 PRECEDING AND 1 PRECEDING) AS p FROM weekly ORDER BY week", conn)
diff_avg = (s.rolling(4, min_periods=1).mean() - sql_avg["a"]).abs().max()
diff_prior = (s.shift(1).rolling(4, min_periods=1).mean() - sql_avg["p"]).abs().max()
print()
print(f"avg_4wk   against rolling(4, min_periods=1): largest difference {diff_avg:.1e}")
print(f"prior_4wk against shift(1).rolling(4, min_periods=1): largest difference {diff_prior:.1e}")
print("rolling(4) WITHOUT min_periods has", int(s.rolling(4).mean().isna().sum()), "NaN rows at the start")

# %% Step 4: quartiles of weeks with NTILE
print()
print(pd.read_sql(WEEKLY + """
    , bucketed AS (SELECT week, orders, NTILE(4) OVER (ORDER BY orders) AS quartile FROM weekly)
    SELECT quartile, COUNT(*) AS weeks, MIN(orders) AS fewest, MAX(orders) AS most
    FROM bucketed GROUP BY quartile
""", conn).to_string(index=False))
conn.close()
