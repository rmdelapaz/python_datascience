# --- lab bootstrap: find labs_paths.py (the same three lines open every lab; see labs/README.md) ---
import pathlib, sys
sys.path[:0] = [str(p) for p in pathlib.Path(globals().get("__file__", "lab.py")).resolve().parents if (p / "labs_paths.py").is_file()]
from labs_paths import DATA
# %% [markdown]
# # Lab 2.3-A · The repair bench, second tent (SOLUTION)
# Audit, repair in the lesson's order (structure, text, numbers, dates, missing values),
# then score against the same 31 days of daily_sales.csv.

# %% Tools
import pathlib

import pandas as pd

pd.set_option("display.width", 150)
pd.set_option("display.max_columns", 20)
LOG = pathlib.Path(globals().get("__file__", "lab.py")).resolve().parent / "asheville_may_log.csv"


def audit(df):
    """One row per column: its dtype, how many values are missing, how many are distinct."""
    return pd.DataFrame({"dtype": df.dtypes.astype(str), "missing": df.isna().sum(), "distinct": df.nunique()})


def score(clean):
    """Compare a cleaned log with the same 31 days of daily_sales.csv, cell by cell."""
    key = pd.read_csv(DATA / "daily_sales.csv", parse_dates=["date"])
    key = key[(key["store"] == "Asheville") & key["date"].between("2025-05-01", "2025-05-31")].set_index("date")
    need = ["date"] + key.columns.tolist()
    if clean.columns.tolist() != need or len(clean) != len(key) or clean["date"].isna().any():
        print("not ready to score: need 31 rows, no missing dates, and exactly these columns:", need)
        return
    mine = clean.set_index("date")
    blank = wrong = 0
    for col in key.columns:
        is_blank = mine[col].isna() & key[col].notna()
        match = (mine[col] == key[col]).fillna(False)
        blank += is_blank.sum()
        wrong += (~match & ~is_blank).sum()
    print(f"cells compared: {key.size} | still blank: {blank} | wrong: {wrong}")


# %% Step 0: audit before you touch anything
raw = pd.read_csv(LOG)
print(raw.columns.tolist())
before = audit(raw)
print(before)
print("rows:", len(raw), "| exact duplicate rows:", raw.duplicated().sum())

# %% Step 1: structure
clean = raw.copy()
clean.columns = clean.columns.str.strip().str.lower()
clean = clean.rename(columns={"revenue ($)": "revenue", "staff": "staff_on_duty", "promo?": "promo_day"})
stated_total = float(clean.loc[clean["date"] == "TOTAL", "revenue"].iloc[0])
clean = clean[clean["date"] != "TOTAL"].drop_duplicates().reset_index(drop=True)
print("after structure:", clean.shape, "| stated total:", stated_total)

# %% Step 2: text
print(clean["store"].value_counts().to_dict())
clean["store"] = clean["store"].str.strip().str.title().replace({"Ashville": "Asheville"})
print(clean["promo_day"].value_counts().to_dict())
clean["promo_day"] = clean["promo_day"].str.strip().str.lower().str[0].map({"y": 1, "n": 0})
print(clean["store"].unique().tolist(), clean["promo_day"].value_counts().to_dict())

# %% Step 3: numbers
stripped = clean["revenue"].str.replace("$", "").str.replace(",", "")
as_number = pd.to_numeric(stripped, errors="coerce")
print("not a number:", clean.loc[as_number.isna(), ["date", "revenue"]].values.tolist())
clean["revenue"] = as_number

per_sale = clean["revenue"] / clean["transactions"]
print(per_sale.describe().round(2).loc[["min", "50%", "max"]].to_dict())
lost_decimal = per_sale > 1000
print("lost decimal point:", clean.loc[lost_decimal, ["date", "transactions", "revenue"]].values.tolist())
clean.loc[lost_decimal, "revenue"] = (clean.loc[lost_decimal, "revenue"] / 100).round(2)

for col in ["visitors", "transactions", "units", "staff_on_duty"]:
    clean[col] = clean[col].astype("Int64")

# %% Step 4: dates
d = clean["date"]
iso = pd.to_datetime(d, format="%Y-%m-%d", errors="coerce")
us = pd.to_datetime(d, format="%m/%d/%Y", errors="coerce")
long = pd.to_datetime(d, format="%B %d, %Y", errors="coerce")
print("dates per format:", iso.notna().sum(), us.notna().sum(), long.notna().sum())
clean["date"] = iso.fillna(us).fillna(long)

# %% Step 5: verify
assert len(clean) == 31
assert set(clean["store"]) == {"Asheville"}
assert clean["revenue"].dropna().between(0, 20000).all()
assert clean["date"].is_unique and clean["date"].notna().all()
print(audit(clean))
print("still missing:", clean.isna().sum()[clean.isna().sum() > 0].to_dict())
score(clean)

# %% Step 6 (stretch): a blank you CAN repair
gap = clean["revenue"].isna()
recovered = round(stated_total - clean["revenue"].sum(), 2)
print("the pending day, recovered from the TOTAL row:", clean.loc[gap, "date"].dt.strftime("%Y-%m-%d").tolist(), recovered)
clean.loc[gap, "revenue"] = recovered
score(clean)
