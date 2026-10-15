# --- lab bootstrap: find labs_paths.py (the same three lines open every lab; see labs/README.md) ---
import pathlib, sys
sys.path[:0] = [str(p) for p in pathlib.Path(globals().get("__file__", "lab.py")).resolve().parents if (p / "labs_paths.py").is_file()]
from labs_paths import DATA
# %% [markdown]
# # Lab 2.4-A · For each store, for each kind of day (SOLUTION)
# Table: daily_sales.csv, one row per store per day (register totals for ALL in-store sales).

# %% Load
import pandas as pd

pd.set_option("display.width", 150)
pd.set_option("display.max_columns", 20)
sales = pd.read_csv(DATA / "daily_sales.csv", parse_dates=["date"])
print(sales.shape)

# %% Step 1: one row per store (named aggregation)
by_store = sales.groupby("store").agg(
    days=("date", "size"),
    days_with_revenue=("revenue", "count"),
    revenue=("revenue", "sum"),
    visitors=("visitors", "sum"),
    transactions=("transactions", "sum"),
)
by_store["conversion"] = by_store["transactions"] / by_store["visitors"]
print(by_store.round(3))
print("groups add up:", by_store["days"].sum(), "==", len(sales))

# %% Step 2: two keys, then unstack
promo = sales.groupby(["store", "promo_day"])["revenue"].mean().unstack("promo_day")
promo["lift"] = (promo[1] / promo[0]).round(2)
print(promo.round(2))

two_means = sales.groupby("promo_day")["revenue"].mean()
print("ordinary and promo day means:", two_means.round(2).tolist())
print("average of those two averages:", round(two_means.mean(), 2))
print("true average store-day       :", round(sales["revenue"].mean(), 2))

# %% Step 3: a key you compute on the spot
year = sales["date"].dt.year.rename("year")
growth = sales.groupby(["store", year])["revenue"].sum().unstack("year").round(0)
growth["growth_pct"] = ((growth[2025] / growth[2024] - 1) * 100).round(1)
print(growth.sort_values("growth_pct", ascending=False))

# %% Step 4: transform (one value per original row)
sales["store_avg"] = sales.groupby("store")["revenue"].transform("mean")
sales["vs_store_avg"] = sales["revenue"] / sales["store_avg"]
standout = sales[sales["vs_store_avg"] >= 2]
print(standout.groupby("store").size())
print("standout days:", len(standout), "| share that were promo days:", round(standout["promo_day"].mean(), 3))
print(sales.nlargest(3, "vs_store_avg")[["date", "store", "revenue", "store_avg", "vs_store_avg"]].round({"store_avg": 2, "vs_store_avg": 2}))
