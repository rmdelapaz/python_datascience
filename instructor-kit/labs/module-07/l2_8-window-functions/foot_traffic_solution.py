# --- lab bootstrap: find labs_paths.py (the same three lines open every lab; see labs/README.md) ---
import pathlib, sys
sys.path[:0] = [str(p) for p in pathlib.Path(globals().get("__file__", "lab.py")).resolve().parents if (p / "labs_paths.py").is_file()]
from labs_paths import DATA

# %% [markdown]
# # Lab 2.8-A · Foot traffic: when did Flagstaff pass Bend? (SOLUTION)

# %% The clean calendar from Lesson 2.7, this time for visitors
import pandas as pd

daily = pd.read_csv(DATA / "daily_sales.csv", parse_dates=["date"])
visitors = daily.pivot(index="date", columns="store", values="visitors")
calendar = pd.date_range(visitors.index.min(), visitors.index.max(), freq="D")
closed_days = calendar.difference(visitors.index)
visitors = visitors.asfreq("D")
visitors.loc[closed_days] = 0
print(visitors.shape, "| unknown store-days:", int(visitors.isna().sum().sum()))

# %% Step 1: a 7-day rolling mean
avg7 = visitors.rolling(7).mean()
print("Boise, 7-day average, first 8 days:")
print(avg7["Boise"].head(8).round(1).to_string())

# %% Step 2: a 28-day rolling mean that survives a few unknown days
avg28 = visitors.rolling(28, min_periods=21).mean()
print("28-day average visitors:")
print(avg28.loc[["2024-06-30", "2024-12-31", "2025-06-30", "2025-12-31"]].round(0))

# %% Step 3: the crossover
ahead = avg28["Flagstaff"] > avg28["Bend"]
first_ahead = ahead[ahead].index[0]
known = avg28[["Flagstaff", "Bend"]].notna().all(axis=1)
last_behind = ahead[known & ~ahead].index[-1]
print("Flagstaff first ahead of Bend on:", first_ahead.date())
print("days with Flagstaff ahead:", int(ahead.sum()))
print("Bend last ahead on:", last_behind.date(), "| Flagstaff ahead for good since:", (last_behind + pd.Timedelta(days=1)).date())

# %% Step 4: record days
flag = visitors["Flagstaff"]
records = flag[flag == flag.cummax()]
print("Flagstaff record days:", len(records))
print(records.tail(3).to_string())

# %% Step 5: each store's busiest 7 consecutive days
sum7 = visitors.rolling(7).sum()
for store in visitors.columns:
    end = sum7[store].idxmax()
    start = end - pd.Timedelta(days=6)
    print(f"{store:<10} {start.date()} to {end.date()}  {sum7[store].max():,.0f} visitors")
