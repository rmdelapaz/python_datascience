# --- lab bootstrap: find labs_paths.py (the same three lines open every lab; see labs/README.md) ---
import pathlib, sys
sys.path[:0] = [str(p) for p in pathlib.Path(globals().get("__file__", "lab.py")).resolve().parents if (p / "labs_paths.py").is_file()]
from labs_paths import DATA
# %% [markdown]
# # Lab 2.3-B · What is each flaw worth? (SOLUTION)
# Question: if someone simply added up the Order Total column of the messy file, how far
# off would they be, and which flaw moves the sum the most?

# %% Load and tidy the headers
import pandas as pd

pd.set_option("display.width", 150)
pd.set_option("display.max_columns", 20)
raw = pd.read_csv(DATA / "orders_messy.csv")
df = raw.copy()
df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_")

# %% Step 1: set the TOTAL row aside
stated_total = float(df.loc[df["order_id"] == "TOTAL", "order_total"].iloc[0])
df = df[df["order_id"] != "TOTAL"]
df["order_id"] = df["order_id"].astype("int64")

# %% Step 2: the careless sum
df["order_total"] = pd.to_numeric(df["order_total"].str.replace("$", "").str.replace(",", ""))
careless = df["order_total"].sum()

# %% Step 3: one repair at a time, recording the sum after each
df = df.drop_duplicates().reset_index(drop=True)
after_duplicates = df["order_total"].sum()

df["order_total"] = df["order_total"].abs()
after_negatives = df["order_total"].sum()

items = pd.read_csv(DATA / "order_items.csv")
item_subtotal = (items["quantity"] * items["unit_price"]).groupby(items["order_id"]).sum()
lost_decimal = df["order_total"] / df["order_id"].map(item_subtotal) > 50
df.loc[lost_decimal, "order_total"] = (df.loc[lost_decimal, "order_total"] / 100).round(2)
after_decimals = df["order_total"].sum()

steps = pd.DataFrame({
    "step": ["careless sum", "drop 212 duplicates", "15 negatives made positive", "8 lost decimal points"],
    "sum": [careless, after_duplicates, after_negatives, after_decimals],
}).round(2)
steps["change"] = steps["sum"].diff().round(2)
steps["off_by_pct"] = ((steps["sum"] / stated_total - 1) * 100).round(2)
print(steps.to_string(index=False))

# %% Step 4: explain what is left
gap = stated_total - after_decimals
print(f"stated total (TOTAL row): {stated_total:,.2f}")
print(f"gap after all repairs   : {gap:,.2f}")

key = pd.read_csv(DATA / "orders.csv").set_index("order_id")["order_total"]
blank_ids = df.loc[df["order_total"].isna(), "order_id"]
print(f"blank totals: {len(blank_ids)} | their true sum in orders.csv: {key[blank_ids].sum():,.2f}")
print("the gap is exactly the blank totals:", abs(gap - key[blank_ids].sum()) < 0.005)
