# --- lab bootstrap: find labs_paths.py (the same three lines open every lab; see labs/README.md) ---
import pathlib, sys
sys.path[:0] = [str(p) for p in pathlib.Path(globals().get("__file__", "lab.py")).resolve().parents if (p / "labs_paths.py").is_file()]
from labs_paths import DATA

# %% [markdown]
# # Lab 2.8-B · The online shop: milestones, ranks and a fair baseline (SOLUTION)

# %% One number per calendar day
import pandas as pd

orders = pd.read_csv(DATA / "orders.csv", parse_dates=["order_date"])
done = orders[(orders["channel"] == "online") & (orders["status"] == "completed")]
day = done.resample("D", on="order_date")["order_total"].sum()
print("days:", len(day), "| days with no revenue:", int((day == 0).sum()), "| total:", round(day.sum(), 2))

# %% Step 1: year to date
ytd = day.groupby(day.index.year).cumsum()
for year in (2024, 2025):
    this_year = ytd.loc[str(year)]
    passed = this_year[this_year >= 1_000_000].index[0]
    print(f"{year}: passed $1,000,000 on {passed.date()} | full year {this_year.iloc[-1]:,.2f}")

# %% Step 2: rank the months inside each year
month = day.resample("ME").sum()
rank = month.groupby(month.index.year).rank(ascending=False)
table = pd.DataFrame({"revenue": month.round(0), "rank_in_year": rank.astype(int)})
table.index = table.index.strftime("%Y-%m")
print(table)

# %% Step 3: record days
records = day[day == day.cummax()]
print("record days:", len(records))
print(records.tail(3).to_string())

# %% Step 4: a baseline that cannot see the day it judges
baseline = day.groupby(day.index.dayofweek).transform(lambda s: s.shift(1).rolling(4).mean())
leaky = day.groupby(day.index.dayofweek).transform(lambda s: s.rolling(4).mean())
best = "2025-06-24"
print(f"{best} ({pd.Timestamp(best).day_name()}): revenue {day.loc[best]:,.2f}")
print(f"  mean of the 4 Tuesdays BEFORE it: {baseline.loc[best]:,.2f} -> {day.loc[best] / baseline.loc[best]:.2f} times normal")
print(f"  without shift(1):                 {leaky.loc[best]:,.2f} -> {day.loc[best] / leaky.loc[best]:.2f} times 'normal' (the day is in its own baseline)")
print("days at least 2 times their baseline: honest", int((day / baseline >= 2).sum()), "| leaky", int((day / leaky >= 2).sum()))
