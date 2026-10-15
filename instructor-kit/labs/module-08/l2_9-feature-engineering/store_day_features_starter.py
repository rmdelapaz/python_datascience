# --- lab bootstrap: find labs_paths.py (the same three lines open every lab; see labs/README.md) ---
import pathlib, sys
sys.path[:0] = [str(p) for p in pathlib.Path(globals().get("__file__", "lab.py")).resolve().parents if (p / "labs_paths.py").is_file()]
from labs_paths import DATA

# %% [markdown]
# # Lab 2.9-B · How busy will the store be tomorrow? Store-day features (STARTER)
# Unit of analysis: ONE ROW IS A STORE ON A DAY. The thing to predict is `visitors`.
# The cutoff rule here: a feature is allowed only if it is known THE EVENING BEFORE.
#
# Expected when you finish:
#   - 2,903 rows before and after merging the weather
#   - four temperature bands with no missing values, and the relative traffic in each
#   - relative traffic for rainy / dry, promotion / regular, weekend / weekday
#   - the number of rows where "7 rows back" is NOT "the same weekday last week"
#   - a correlation table that shows which columns are suspiciously good, and your verdict on each

# %% Load and merge (done for you: the key has a different name in each file)
import numpy as np
import pandas as pd

daily = pd.read_csv(DATA / "daily_sales.csv", parse_dates=["date"])
weather = pd.read_csv(DATA / "store_weather.csv", parse_dates=["date"])
t = daily.merge(weather, left_on=["date", "store"], right_on=["date", "city"], how="left", validate="one_to_one")
print("rows before and after:", len(daily), len(t))

# %% Step 1: a ratio that removes store size
# Boise always has more visitors than Asheville. Divide by each store's own average, so 1.0 means "a normal day".
# TODO 1: t["rel_visitors"] = t["visitors"] / t.groupby("store")["visitors"].transform("mean")

# %% Step 2: date parts and flags
# TODO 2: add  weekday (0 = Monday),  is_weekend,  and  rainy (precip_in >= 0.10).

# %% Step 3: bins with edges that cover everything
# TODO 3: temp_band = pd.cut of high_f with edges at 40, 60 and 80 degrees and the labels
#         ["cold", "cool", "warm", "hot"]. Start at -np.inf and end at np.inf so no value falls outside.
#         Print value_counts(sort=False) and the number of missing values (it must be 0).

# %% Step 4: check each feature against relative traffic (rate AND size)
# TODO 4: for temp_band, rainy, promo_day and is_weekend print
#         t.groupby(col)["rel_visitors"].agg(["mean", "size"])

# %% Step 5: "the same weekday last week", done wrongly and done right
# TODO 5: a) the tempting version: sort by store and date, then t.groupby("store")["visitors"].shift(7)
#         b) the right version: pivot visitors to a wide table, .asfreq("D"), .shift(7), then .stack()
#            and merge back on date and store.
#         Count the rows where both exist and differ. (Hint from Lesson 2.7: shift moves rows, not days.)

# %% Step 6: the leak audit
# TODO 6: print the correlation of visitors with: your calendar lag, transactions, units, revenue,
#         staff_on_duty, high_f and promo_day. For each one answer: known the evening before? yes or no.
print("Expected at the end: a verdict for each column: feature, or leak.")
