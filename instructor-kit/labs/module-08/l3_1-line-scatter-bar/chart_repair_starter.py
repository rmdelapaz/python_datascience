# --- lab bootstrap: find labs_paths.py (the same three lines open every lab; see labs/README.md) ---
import pathlib, sys
sys.path[:0] = [str(p) for p in pathlib.Path(globals().get("__file__", "lab.py")).resolve().parents if (p / "labs_paths.py").is_file()]
from labs_paths import DATA, OUTPUT

# %% [markdown]
# # Lab 3.1-B · Chart repair: three charts that draw without an error and are wrong (STARTER)
# This file runs as it is. Nothing crashes. All three charts are wrong.
# For each one: read the printed clue, say what the chart is really showing, then fix it and
# save the fixed chart with fig.savefig(OUTPUT / "name.png"). Do not call plt.show().
#
# Expected when you finish:
#   - Chart 1: 4 bars instead of 1,145, sorted, showing each payment method's TOTAL
#   - Chart 2: a line that BREAKS on the two days Flagstaff's export failed
#   - Chart 3: a handful of date ticks instead of 731

# %% Load (done for you)
import matplotlib.pyplot as plt
import pandas as pd

orders = pd.read_csv(DATA / "orders.csv", parse_dates=["order_date"])
daily = pd.read_csv(DATA / "daily_sales.csv", parse_dates=["date"])
december = orders[orders["order_date"] >= "2025-12-01"]

# %% Chart 1. Question: which payment method brought in the most money in December 2025?
fig, ax = plt.subplots(figsize=(7, 3.5), layout="constrained")
bars = ax.bar(december["payment_method"], december["order_total"])
ax.set_title("December 2025 revenue by payment method")
print("Chart 1 clue:", len(bars), "bars were drawn for 4 payment methods.")
print("   tallest visible bar per method:", december.groupby("payment_method")["order_total"].max().to_dict())
plt.close(fig)
# TODO 1: what do the four visible bars really show? Aggregate FIRST (one number per method, sorted),
#         then draw the bars, label them with ax.bar_label(bars, fmt="${:,.0f}"), save "fixed_1_payment.png".

# %% Chart 2. Question: how did Flagstaff's visitor count move in late January 2025?
flag = daily[(daily["store"] == "Flagstaff") & (daily["date"] >= "2025-01-13") & (daily["date"] <= "2025-01-31")]
fig, ax = plt.subplots(figsize=(8, 3.2), layout="constrained")
ax.plot(flag["date"], flag["visitors"], marker="o")
ax.set_title("Flagstaff: visitors per day")
print("Chart 2 clue:", len(flag), "rows for the 19 days from January 13 to January 31.")
plt.close(fig)
# TODO 2: the line runs straight through two days that were never recorded. Put the calendar back
#         (set_index("date")["visitors"].asfreq("D")), plot that, and save "fixed_2_visitors.png".
#         Print how many NaN values the new Series has.

# %% Chart 3. Question: how does Boise's daily high temperature move through the two years?
weather = pd.read_csv(DATA / "store_weather.csv")                 # look closely at this line
boise = weather[weather["city"] == "Boise"]
fig, ax = plt.subplots(figsize=(8, 3.2), layout="constrained")
ax.plot(boise["date"], boise["high_f"], linewidth=0.8)
ax.set_title("Boise: daily high temperature")
print("Chart 3 clue: the date column has dtype", boise["date"].dtype, "and the x axis has", len(ax.get_xticks()), "tick labels.")
plt.close(fig)
# TODO 3: fix the cause, not the symptom. Redraw, print the new number of ticks, save "fixed_3_temperature.png".

# %% Last cell (done for you)
plt.close("all")
saved = sorted(p.name for p in OUTPUT.glob("fixed_*.png"))
print("saved:", saved if saved else "nothing yet: the three charts are still wrong")
