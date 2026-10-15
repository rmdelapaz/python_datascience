# --- lab bootstrap: find labs_paths.py (the same three lines open every lab; see labs/README.md) ---
import pathlib, sys
sys.path[:0] = [str(p) for p in pathlib.Path(globals().get("__file__", "lab.py")).resolve().parents if (p / "labs_paths.py").is_file()]
from labs_paths import DATA
# %% [markdown]
# # Lab 2.1-A · The busiest days (STARTER)
# Question: which were Pinecrest's five biggest store-days by revenue, were they sale
# (promo) days, and how often does a store take in more than $15,000 in a day?
#
# Table: daily_sales.csv, one row per store per day (you used it as arrays in Module 1).
# Expected when you finish: the shape and the one column with missing values, a five-row
# table of the biggest days, three counts about the $15,000 days, and the best and the
# quietest day found with .idxmax() / .idxmin() and .loc.

# %% Load (done for you)
import pandas as pd

pd.set_option("display.width", 150)
sales = pd.read_csv(DATA / "daily_sales.csv")

# %% Step 1: greet the table
# TODO 1: print sales.shape, then sales.dtypes.
#         Then print the count of missing values per column: sales.isna().sum()
print("TODO 1: shape, dtypes and missing values not printed yet")

# %% Step 2: the five biggest days
# TODO 2: sort by revenue, largest first (sort_values with ascending=False, or nlargest),
#         keep the columns date, store, revenue, promo_day, and store the first 5 rows in `top5`.
top5 = None

# %% Step 3: the $15,000 days
# TODO 3: build a mask `big` for revenue above 15000 and a mask `promo` for promo_day == 1.
#         Count: big days, big days that were promo days (use & and parentheses),
#         and big days that were NOT promo days (use ~).
big = None
promo = None

# %% Step 4: one row by its label
# TODO 4: best_label = sales["revenue"].idxmax()   (the index label of the largest revenue)
#         Use sales.loc[best_label, ["date", "store", "revenue"]] to show that row.
#         Do the same with .idxmin() for the quietest day.
best_label = None

# %% Report (runs as soon as the TODOs are done)
if top5 is None or big is None or promo is None or best_label is None:
    print("TODOs 2-4 not done yet: top5, big, promo or best_label is still None.")
else:
    print(top5)
    print("days above $15,000:", big.sum())
    print("  of those, promo days:", (big & promo).sum())
    print("  of those, ordinary days:", (big & ~promo).sum())
    best = sales.loc[best_label, ["date", "store", "revenue"]]
    print(f"best day: label {best_label}, {best['date']}, {best['store']}, ${best['revenue']:,.2f}")
