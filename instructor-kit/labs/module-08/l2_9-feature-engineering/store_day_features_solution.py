# --- lab bootstrap: find labs_paths.py (the same three lines open every lab; see labs/README.md) ---
import pathlib, sys
sys.path[:0] = [str(p) for p in pathlib.Path(globals().get("__file__", "lab.py")).resolve().parents if (p / "labs_paths.py").is_file()]
from labs_paths import DATA

# %% [markdown]
# # Lab 2.9-B · How busy will the store be tomorrow? Store-day features (SOLUTION)
# Unit of analysis: one row is a store on a day. Cutoff rule: known the evening before.

# %% Load and merge
import numpy as np
import pandas as pd

daily = pd.read_csv(DATA / "daily_sales.csv", parse_dates=["date"])
weather = pd.read_csv(DATA / "store_weather.csv", parse_dates=["date"])
t = daily.merge(weather, left_on=["date", "store"], right_on=["date", "city"], how="left", validate="one_to_one")
print("rows before and after:", len(daily), len(t))

# %% Step 1: a ratio that removes store size
t["rel_visitors"] = t["visitors"] / t.groupby("store")["visitors"].transform("mean")
print(t.groupby("store")[["visitors", "rel_visitors"]].mean().round(2))

# %% Step 2: date parts and flags
t["weekday"] = t["date"].dt.dayofweek
t["is_weekend"] = t["weekday"] >= 5
t["rainy"] = t["precip_in"] >= 0.10

# %% Step 3: bins with edges that cover everything
t["temp_band"] = pd.cut(t["high_f"], bins=[-np.inf, 40, 60, 80, np.inf], labels=["cold", "cool", "warm", "hot"])
print(t["temp_band"].value_counts(sort=False).to_string())
print("missing temp_band:", int(t["temp_band"].isna().sum()))

# %% Step 4: check each feature against relative traffic
for col in ["temp_band", "rainy", "promo_day", "is_weekend"]:
    print(t.groupby(col, observed=True)["rel_visitors"].agg(["mean", "size"]).round(3))

# %% Step 5: "the same weekday last week", done wrongly and done right
t = t.sort_values(["store", "date"]).reset_index(drop=True)
t["lag7_rows"] = t.groupby("store")["visitors"].shift(7)                       # 7 ROWS back
wide = daily.pivot(index="date", columns="store", values="visitors").asfreq("D")
lag = wide.shift(7).stack().rename("lag7_calendar").reset_index()              # 7 DAYS back
t = t.merge(lag, on=["date", "store"], how="left", validate="one_to_one")
both = t["lag7_rows"].notna() & t["lag7_calendar"].notna()
differ = both & (t["lag7_rows"] != t["lag7_calendar"])
print("rows where 7 rows back is not 7 days back:", int(differ.sum()))
print(t.loc[differ, ["date", "store", "visitors", "lag7_rows", "lag7_calendar"]].head(3).to_string(index=False))

# %% Step 6: the leak audit
cols = ["lag7_calendar", "staff_on_duty", "promo_day", "high_f", "transactions", "units", "revenue"]
corr = t[cols].corrwith(t["visitors"]).round(2)
verdict = {"lag7_calendar": "feature: last week is in the past",
           "staff_on_duty": "feature: the schedule is fixed in advance (but it encodes someone's forecast)",
           "promo_day": "feature: the sale calendar is planned",
           "high_f": "only as a FORECAST made the evening before, not the measured high",
           "transactions": "LEAK: counted during the day being predicted",
           "units": "LEAK: counted during the day being predicted",
           "revenue": "LEAK: counted during the day being predicted"}
for col in cols:
    print(f"{col:<14} r = {corr[col]:>5.2f}   {verdict[col]}")
