# --- lab bootstrap: find labs_paths.py (the same three lines open every lab; see labs/README.md) ---
import pathlib, sys
sys.path[:0] = [str(p) for p in pathlib.Path(globals().get("__file__", "lab.py")).resolve().parents if (p / "labs_paths.py").is_file()]
from labs_paths import DATA, OUTPUT

# %% [markdown]
# # Lab 3.1-B · Chart repair: three charts that draw without an error and are wrong (SOLUTION)

# %% Load
import matplotlib.pyplot as plt
import pandas as pd

orders = pd.read_csv(DATA / "orders.csv", parse_dates=["order_date"])
daily = pd.read_csv(DATA / "daily_sales.csv", parse_dates=["date"])
december = orders[orders["order_date"] >= "2025-12-01"]

# %% Chart 1: ax.bar never aggregates. The wrong chart stacked 1,145 bars at 4 positions,
#    so each visible bar was that method's single LARGEST order, not its total.
by_method = december.groupby("payment_method")["order_total"].sum().sort_values(ascending=False)
fig, ax = plt.subplots(figsize=(7, 3.5), layout="constrained")
bars = ax.bar(by_method.index, by_method.values, color="#667eea")
ax.bar_label(bars, fmt="${:,.0f}")
ax.set_title("December 2025 revenue by payment method")
ax.set_ylabel("Revenue (USD)")
fig.savefig(OUTPUT / "fixed_1_payment.png")
print("Chart 1: was", len(december), "bars (largest single order per method:",
      december.groupby("payment_method")["order_total"].max().round(2).to_dict(), ")")
print("         now", len(bars), "bars:", by_method.round(2).to_dict())

# %% Chart 2: absent rows are bridged by a straight segment; NaN values break the line.
flag = daily[(daily["store"] == "Flagstaff") & (daily["date"] >= "2025-01-13") & (daily["date"] <= "2025-01-31")]
full = flag.set_index("date")["visitors"].asfreq("D")
fig, ax = plt.subplots(figsize=(8, 3.2), layout="constrained")
ax.plot(full.index, full, marker="o", color="#667eea")
ax.set_title("Flagstaff: visitors per day (January 21 and 22 were never recorded)")
ax.set_ylabel("Visitors")
fig.savefig(OUTPUT / "fixed_2_visitors.png")
print("Chart 2: was", len(flag), "rows; now", len(full), "days with", int(full.isna().sum()), "NaN on",
      [str(d.date()) for d in full[full.isna()].index])

# %% Chart 3: dates left as text are categories: one tick per row.
weather = pd.read_csv(DATA / "store_weather.csv", parse_dates=["date"])
boise = weather[weather["city"] == "Boise"]
fig, ax = plt.subplots(figsize=(8, 3.2), layout="constrained")
ax.plot(boise["date"], boise["high_f"], linewidth=0.8, color="#667eea")
ax.set_title("Boise: daily high temperature")
ax.set_ylabel("High (°F)")
fig.savefig(OUTPUT / "fixed_3_temperature.png")
print("Chart 3: dtype is now", boise["date"].dtype, "and the x axis has", len(ax.get_xticks()), "ticks (it had 731)")

# %% Close and list
plt.close("all")
print("saved:", sorted(p.name for p in OUTPUT.glob("fixed_*.png")))
