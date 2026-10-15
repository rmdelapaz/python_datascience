# --- lab bootstrap: find labs_paths.py (the same three lines open every lab; see labs/README.md) ---
import pathlib, sys
sys.path[:0] = [str(p) for p in pathlib.Path(globals().get("__file__", "lab.py")).resolve().parents if (p / "labs_paths.py").is_file()]
from labs_paths import DATA

# %% [markdown]
# # Lab 4.7-C · Missing for whom? The customer table (STARTER)
# Steps 2 and 3 of the routine on a table the lesson did not explore: customers.csv.
# In the survey, missing answers followed a pattern (online shoppers skipped the staff
# question). Is that true here as well, or are these gaps just gaps?
#
# Questions, written first:
#   1. What is one row, and what identifies it?
#   2. Which columns have missing values, and are they missing for a particular kind of customer?
#   3. Who is in orders.csv but NOT in this table, and do their orders look different?
#
# Expected when you finish: the overview table, four lines that say whether phone and birth_year
# are missing more often for some channel or tier, the count of orders with no customer row,
# a comparison of those orders with the rest, and a findings note.

# %% Setup (done for you)
import pandas as pd
from scipy import stats


def overview(df):
    """One row per column: type, missing values, distinct values and an example (from Lesson 4.7)."""
    return pd.DataFrame({
        "dtype": df.dtypes.astype(str),
        "missing": df.isna().sum(),
        "missing_pct": (df.isna().mean() * 100).round(1),
        "unique": df.nunique(),
        "example": df.apply(lambda col: str(col.dropna().iloc[0])[:22]),
    })


customers = pd.read_csv(DATA / "customers.csv", parse_dates=["signup_date"])
orders = pd.read_csv(DATA / "orders.csv", parse_dates=["order_date"])

# %% Step 1: structure
# TODO 1: print overview(customers). State the grain and the key in a comment, and prove the key
#         with .is_unique. Which two columns have missing values?

# %% Step 2: missing for whom?
# TODO 2: for col in ["phone", "birth_year"] and by in ["acquisition_channel", "loyalty_tier"]:
#         print the share of customers with col missing in each group, and the p-value of
#         stats.chi2_contingency(pd.crosstab(customers[by], customers[col].isna())).
#         You are running four tests. What would you expect to see if nothing is going on?

# %% Step 3: who is not in the table?
# TODO 3: merge orders with customers[["customer_id", "loyalty_tier"]] using how="left",
#         validate="many_to_one" and indicator=True. How many orders found no customer?
#         From how many distinct customer ids?
merged = None

# %% Step 4: do the orphan orders look different?
# TODO 4: compare orphan orders with matched orders: share online, share returned,
#         median order_total (and a Mann-Whitney test on order_total).

# %% Step 5: the note
# TODO 5: two findings with numbers and at least one caveat. What would an inner merge have done?
if merged is None:
    print("TODO 1-5 not done yet: `merged` is None.")
