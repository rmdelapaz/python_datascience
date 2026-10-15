# --- lab bootstrap: find labs_paths.py (the same three lines open every lab; see labs/README.md) ---
import pathlib, sys
sys.path[:0] = [str(p) for p in pathlib.Path(globals().get("__file__", "lab.py")).resolve().parents if (p / "labs_paths.py").is_file()]
from labs_paths import DATA, OUTPUT

# %% [markdown]
# # Lab 3.2-B · Two measures, honestly (SOLUTION)

# %% Load and merge
import matplotlib.pyplot as plt
import pandas as pd

daily = pd.read_csv(DATA / "daily_sales.csv", parse_dates=["date"])
weather = pd.read_csv(DATA / "store_weather.csv", parse_dates=["date"])
ash = daily[daily["store"] == "Asheville"].merge(
    weather[weather["city"] == "Asheville"], on="date", how="left", validate="one_to_one")
ash["rainy"] = ash["precip_in"] >= 0.10
ash["month"] = ash["date"].dt.to_period("M").dt.to_timestamp()
am = ash.groupby("month").agg(visitors=("visitors", "mean"), rainy_days=("rainy", "sum"), high_f=("high_f", "mean"))
print(am.shape, "| rainy days per month from", am["rainy_days"].min(), "to", am["rainy_days"].max())

# %% Step 1: the twin axis, twice
fig, axs = plt.subplots(1, 2, figsize=(10, 3.6), layout="constrained")
for ax, limits in zip(axs, [(0, 20), (0, 60)]):
    ax.plot(am.index, am["visitors"], color="#667eea")
    ax.set_ylabel("Visitors per day", color="#667eea")
    right = ax.twinx()
    right.plot(am.index, am["rainy_days"], color="#d95f02", linestyle="--")
    right.set_ylabel("Rainy days", color="#d95f02")
    right.set_ylim(limits)
    ax.set_title(f"Right axis from {limits[0]} to {limits[1]}")
fig.savefig(OUTPUT / "twin_two_stories.png")
print("Step 1: same data, two right-axis ranges; figure has", len(fig.axes), "Axes")

# %% Step 2: stacked panels
fig, (top, bottom) = plt.subplots(2, 1, figsize=(9, 5), sharex=True, layout="constrained")
top.plot(am.index, am["visitors"], color="#667eea")
top.set_ylabel("Visitors per day")
top.set_title("Asheville: visitors and rainy days, month by month")
bottom.bar(am.index, am["rainy_days"], width=20, color="#d95f02")
bottom.set_ylabel("Rainy days")
fig.savefig(OUTPUT / "stacked.png")

# %% Step 3: the relationship itself
r = am["rainy_days"].corr(am["visitors"])
by_day = ash.groupby("rainy")["visitors"].mean().round(1)
print("Step 3: monthly correlation of rainy days and visitors:", round(r, 2))
print("        mean visitors on dry days:", by_day[False], "| on rainy days:", by_day[True],
      f"({(by_day[True] / by_day[False] - 1) * 100:.1f}%)")

# %% Step 4: one quantity, two units
def f_to_c(f):
    return (f - 32) * 5 / 9

def c_to_f(c):
    return c * 9 / 5 + 32

fig, ax = plt.subplots(figsize=(8, 3.4), layout="constrained")
ax.plot(am.index, am["high_f"], color="#667eea", marker="o", markersize=3)
ax.set_ylabel("Mean daily high (°F)")
ax.set_title("Asheville: mean daily high temperature by month")
celsius = ax.secondary_yaxis("right", functions=(f_to_c, c_to_f))
celsius.set_ylabel("°C")
fig.savefig(OUTPUT / "temperature_two_units.png")
print(f"Step 4: warmest month {am['high_f'].idxmax():%Y-%m}, {am['high_f'].max():.1f} °F = {f_to_c(am['high_f'].max()):.1f} °C")

plt.close("all")
print("saved:", sorted(p.name for p in OUTPUT.glob("*.png")))
