# --- lab bootstrap: find labs_paths.py (the same three lines open every lab; see labs/README.md) ---
import pathlib, sys
sys.path[:0] = [str(p) for p in pathlib.Path(globals().get("__file__", "lab.py")).resolve().parents if (p / "labs_paths.py").is_file()]
from labs_paths import DATA
# %% [markdown]
# # Lab 2.6-C · pivot, pivot_table and the order of months (SOLUTION)
# Table: store_weather.csv, one row per city per day (2,924 rows; complete, no gaps).

# %% Load
import pandas as pd

pd.set_option("display.width", 150)
pd.set_option("display.max_columns", 20)

weather = pd.read_csv(DATA / "store_weather.csv", parse_dates=["date"])
print(weather.shape, "| repeated (date, city) pairs:", weather.duplicated(["date", "city"]).sum())

# %% Step 1: rearrange only (one row per cell already, so pivot is enough)
wide = weather.pivot(index="date", columns="city", values="high_f")
print("wide:", wide.shape, "| empty cells:", wide.isna().sum().sum())
print(wide.head(3))

# %% Step 2: read across each row
warmest = wide.idxmax(axis=1)
print(warmest.value_counts().to_dict(), "| total:", warmest.value_counts().sum())

# %% Step 3: summarize, then arrange
weather["month"] = weather["date"].dt.month
by_month = weather.pivot_table(index="month", columns="city", values="high_f", aggfunc="mean")
print(by_month.loc[[1, 4, 7, 10]].round(1))

# %% Step 4: the month-name trap
weather["month_name"] = weather["date"].dt.strftime("%b")
named = weather.pivot_table(index="month_name", columns="city", values="high_f", aggfunc="mean")
print("as pivoted:", named.index.tolist())
calendar = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
named = named.reindex(calendar)
print("reindexed :", named.index.tolist())
print(named.loc[["Jan", "Jul"]].round(1))

# %% Step 5: and back again
tidy = wide.reset_index().melt(id_vars="date", var_name="city", value_name="high_f")
print("tidy rows:", len(tidy), "| same as the file:", len(tidy) == len(weather))
