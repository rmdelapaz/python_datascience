# --- lab bootstrap: find labs_paths.py (the same three lines open every lab; see labs/README.md) ---
import pathlib, sys
sys.path[:0] = [str(p) for p in pathlib.Path(globals().get("__file__", "lab.py")).resolve().parents if (p / "labs_paths.py").is_file()]
from labs_paths import DATA

# %% [markdown]
# # Lab 4.1-B · Which store has the steadiest foot traffic? (SOLUTION)
# Staffing is easy when every day looks alike and hard when days swing. Measure how much each
# store's daily visitor count varies, four ways, and see which measures survive a bad row.

# %% Load the door-counter data
import numpy as np
import pandas as pd

daily = pd.read_csv(DATA / "daily_sales.csv", parse_dates=["date"])
print("rows:", len(daily), "| visitors present:", daily["visitors"].count())

# %% Step 1: a variance by hand, on Bend's first five days
five = daily.loc[daily["store"] == "Bend", "visitors"].head(5).to_numpy()
deviations = five - five.mean()
print("five days         :", five, " mean:", five.mean())
print("deviations        :", deviations, " sum:", round(deviations.sum(), 6))
print("sum of squares    :", (deviations ** 2).sum())
print("variance, / n     :", (deviations ** 2).sum() / len(five))
print("variance, / (n-1) :", (deviations ** 2).sum() / (len(five) - 1))

# %% Step 2: match the libraries
print("np.var(five)             :", np.var(five))                 # ddof=0
print("pd.Series(five).var()    :", pd.Series(five).var())        # ddof=1
print("np.std(five)             :", round(np.std(five), 2))
print("pd.Series(five).std()    :", round(pd.Series(five).std(), 2))
print("np.std(five, ddof=1)     :", round(np.std(five, ddof=1), 2))

# %% Step 3: four measures of spread for every store
def spread(values):
    q1, q3 = values.quantile(0.25), values.quantile(0.75)
    return pd.Series({"mean": values.mean(), "median": values.median(),
                      "range": values.max() - values.min(), "sd": values.std(), "iqr": q3 - q1})

table = daily.groupby("store")["visitors"].apply(spread).unstack().round(1)
print(table)

# %% Step 4: steadiest in visitors, or steadiest for its size?
table["sd_over_mean"] = (table["sd"] / table["mean"]).round(3)
print(table[["mean", "sd", "sd_over_mean"]])
print("smallest SD:", table["sd"].idxmin(), "| largest SD:", table["sd"].idxmax())
print("largest SD relative to its mean:", table["sd_over_mean"].idxmax())

# %% Step 5: stress test. The door counter at Bend records 7950 instead of 795 on its busiest day
bend = daily.loc[daily["store"] == "Bend", "visitors"]
broken = bend.copy()
broken.loc[bend.idxmax()] = 7950
for label, col in [("clean ", bend), ("broken", broken)]:
    iqr = col.quantile(0.75) - col.quantile(0.25)
    print(f"{label} mean {col.mean():6.1f}  median {col.median():5.1f}  "
          f"range {col.max() - col.min():5d}  SD {col.std():6.1f}  IQR {iqr:6.2f}")
