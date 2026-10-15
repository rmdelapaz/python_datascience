# --- lab bootstrap: find labs_paths.py (the same three lines open every lab; see labs/README.md) ---
import pathlib, sys
sys.path[:0] = [str(p) for p in pathlib.Path(globals().get("__file__", "lab.py")).resolve().parents if (p / "labs_paths.py").is_file()]
from labs_paths import DATA
# %% [markdown]
# # Lab 2.1-A · The busiest days (SOLUTION)
# Question: which were Pinecrest's five biggest store-days by revenue, were they sale
# (promo) days, and how often does a store take in more than $15,000 in a day?

# %% Load
import pandas as pd

pd.set_option("display.width", 150)
sales = pd.read_csv(DATA / "daily_sales.csv")

# %% Step 1: greet the table
print("shape:", sales.shape)
print(sales.dtypes.to_string())
missing = sales.isna().sum()
print("columns with missing values:", missing[missing > 0].to_dict())

# %% Step 2: the five biggest days
top5 = sales.sort_values("revenue", ascending=False)[["date", "store", "revenue", "promo_day"]].head(5)
print(top5)

# %% Step 3: the $15,000 days
big = sales["revenue"] > 15000
promo = sales["promo_day"] == 1
print("days above $15,000:", big.sum())
print("  of those, promo days:", (big & promo).sum())
print("  of those, ordinary days:", (big & ~promo).sum())
print("share of all promo days that pass $15,000:", round((big & promo).sum() / promo.sum() * 100, 1), "%")

# %% Step 4: one row by its label
best_label = sales["revenue"].idxmax()
quiet_label = sales["revenue"].idxmin()
best = sales.loc[best_label, ["date", "store", "revenue"]]
quiet = sales.loc[quiet_label, ["date", "store", "revenue"]]
print(f"best day    : label {best_label}, {best['date']}, {best['store']}, ${best['revenue']:,.2f}")
print(f"quietest day: label {quiet_label}, {quiet['date']}, {quiet['store']}, ${quiet['revenue']:,.2f}")
