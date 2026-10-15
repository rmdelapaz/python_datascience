# --- lab bootstrap: find labs_paths.py (the same three lines open every lab; see labs/README.md) ---
import pathlib, sys
sys.path[:0] = [str(p) for p in pathlib.Path(globals().get("__file__", "lab.py")).resolve().parents if (p / "labs_paths.py").is_file()]
from labs_paths import DATA

# %% [markdown]
# # Lab 4.7-C · Missing for whom? The customer table (SOLUTION)
# Steps 2 and 3 of the routine on a table the lesson did not explore: customers.csv.
# In the survey, missing answers followed a pattern (online shoppers skipped the staff
# question). Is that true here as well, or are these gaps just gaps?
#
# Questions, written first:
#   1. What is one row, and what identifies it?
#   2. Which columns have missing values, and are they missing for a particular kind of customer?
#   3. Who is in orders.csv but NOT in this table, and do their orders look different?
#
# Reference solution. Do not hand out before the lab.

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
print(overview(customers).to_string())
print()
print("grain: one row per customer account | key customer_id unique:", customers["customer_id"].is_unique,
      "| email unique:", customers["email"].is_unique)

# %% Step 2: missing for whom?
print()
for col in ["phone", "birth_year"]:
    customers[col + "_missing"] = customers[col].isna()
    for by in ["acquisition_channel", "loyalty_tier"]:
        table = pd.crosstab(customers[by], customers[col + "_missing"])
        share = (customers.groupby(by)[col + "_missing"].mean() * 100).round(1)
        print(f"{col} missing by {by}: {share.to_dict()}  chi-square p = {stats.chi2_contingency(table).pvalue:.2f}")
print("Four checks, none below 0.05: no sign that either column is missing for a particular kind of customer.")

# %% Step 3: who is not in the table?
print()
merged = orders.merge(customers[["customer_id", "loyalty_tier"]], on="customer_id", how="left",
                      validate="many_to_one", indicator=True)
print(merged["_merge"].value_counts().to_string())
orphans = merged[merged["_merge"] == "left_only"]
print("orders with no customer row:", len(orphans), "from", orphans["customer_id"].nunique(), "customer ids")
print("ids between 10001 and 15000 that are absent from customers.csv:", 5000 - len(customers))

# %% Step 4: do the orphan orders look different?
merged["orphan"] = merged["_merge"] == "left_only"
print()
print("share online:", (merged.groupby("orphan")["channel"].apply(lambda s: (s == "online").mean()) * 100).round(1).to_dict())
print("share returned:", (merged.groupby("orphan")["status"].apply(lambda s: (s == "returned").mean()) * 100).round(1).to_dict())
print("median order total:", merged.groupby("orphan")["order_total"].median().to_dict())
p_total = stats.mannwhitneyu(merged.loc[merged["orphan"], "order_total"], merged.loc[~merged["orphan"], "order_total"]).pvalue
print(f"order total, orphan against matched (Mann-Whitney): p = {p_total:.2f}")
print("first and last orphan order:", orphans["order_date"].min().date(), "to", orphans["order_date"].max().date())

# %% Step 5: the note
print()
print("FINDINGS")
print("- One row per account, keyed by customer_id (4,850 rows). phone is missing for 5.8% and")
print("  birth_year for 9.1%; neither is tied to acquisition channel or loyalty tier.")
print("- 739 orders (3.6%) belong to 150 customer ids with no row in customers.csv: exactly the 150")
print("  ids missing from the 10001-15000 range (closed accounts). Their orders span both years and")
print("  have the same channel mix and return rate as everyone else's.")
print("CAVEATS")
print("- 'Not tied to channel or tier' covers the columns checked, not every possible pattern.")
print("- An inner merge of orders with customers silently drops those 739 orders. Their median total is")
print(f"  a little higher ($158.95 against $146.70) but within what chance produces (p = {p_total:.2f}).")
