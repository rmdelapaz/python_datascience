# --- lab bootstrap: find labs_paths.py (the same three lines open every lab; see labs/README.md) ---
import pathlib, sys
sys.path[:0] = [str(p) for p in pathlib.Path(globals().get("__file__", "lab.py")).resolve().parents if (p / "labs_paths.py").is_file()]
from labs_paths import DATA, OUTPUT

# %% [markdown]
# # Lab 3.2-A · Foot traffic on one page (SOLUTION)

# %% Load
import matplotlib.pyplot as plt
import pandas as pd

daily = pd.read_csv(DATA / "daily_sales.csv", parse_dates=["date"])
daily["month"] = daily["date"].dt.to_period("M").dt.to_timestamp()
traffic = daily.pivot_table(index="month", columns="store", values="visitors", aggfunc="mean")
stores = list(traffic.columns)
print("monthly mean visitors:", traffic.shape, stores)

growth = (traffic.loc["2025"].mean() / traffic.loc["2024"].mean() - 1) * 100
print("change in mean daily visitors, 2025 vs 2024 (%):", growth.round(1).to_dict())

# %% Step 1: own scales
fig, axs = plt.subplots(2, 2, figsize=(9, 5.5), layout="constrained")
for ax, store in zip(axs.flat, stores):
    ax.plot(traffic.index, traffic[store], color="#667eea")
    ax.set_title(store)
fig.suptitle("Mean visitors per day, by month (each panel has its own scale)")
fig.savefig(OUTPUT / "grid_own_scales.png")
print("Step 1 y ranges:", [tuple(round(v) for v in ax.get_ylim()) for ax in axs.flat])

# %% Step 2: one scale
fig, axs = plt.subplots(2, 2, figsize=(9, 5.5), sharex=True, sharey=True, layout="constrained")
for ax, store in zip(axs.flat, stores):
    ax.plot(traffic.index, traffic[store], color="#667eea")
    ax.set_title(store)
fig.suptitle("Mean visitors per day, by month, on one scale")
fig.supylabel("Visitors per day")
fig.savefig(OUTPUT / "grid_shared.png")
print("Step 2 same y range in every panel:", axs[0, 0].get_ylim() == axs[1, 1].get_ylim())

# %% Step 3: small multiples with context
def draw_store(ax, table, store):
    """One store in color, the others in gray behind it."""
    for other in table.columns:
        if other != store:
            ax.plot(table.index, table[other], color="lightgray", linewidth=1)
    ax.plot(table.index, table[store], color="#667eea", linewidth=2)
    ax.set_title(store)
    ax.set_xticks(pd.to_datetime(["2024-01-01", "2025-01-01"]), labels=["2024", "2025"])

fig, axs = plt.subplots(1, 4, figsize=(10, 2.8), sharey=True, layout="constrained")
for ax, store in zip(axs, stores):
    draw_store(ax, traffic, store)
fig.suptitle("Mean visitors per day: each store against the others")
fig.savefig(OUTPUT / "small_multiples.png")
print("Step 3 lines per panel:", [len(ax.lines) for ax in axs])

# %% Step 4: a named layout
flag = daily[daily["store"] == "Flagstaff"]
by_weekday = flag.groupby(flag["date"].dt.dayofweek)["visitors"].mean()
print("Flagstaff rows:", len(flag))
fig, axd = plt.subplot_mosaic([["trend", "trend"], ["week", "spread"]], figsize=(9, 6), layout="constrained")
axd["trend"].plot(traffic.index, traffic["Flagstaff"], marker="o", markersize=3, color="#667eea")
axd["trend"].set_title("Mean visitors per day, by month")
axd["week"].bar(["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"], by_weekday.values, color="#667eea")
axd["week"].set_title("Mean visitors by day of the week")
axd["spread"].hist(flag["visitors"], bins=30, color="#667eea", edgecolor="white")
axd["spread"].set_title("How daily visitors are distributed")
axd["spread"].set_xlabel("Visitors per day")
fig.suptitle("Flagstaff store, 2024 and 2025")
fig.savefig(OUTPUT / "flagstaff_summary.png")
print("Step 4 panels:", list(axd), "| busiest weekday:", ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"][by_weekday.idxmax()],
      round(by_weekday.max()), "| quietest:", round(by_weekday.min()))

# %% Close and list
plt.close("all")
print("saved:", sorted(p.name for p in OUTPUT.glob("*.png")))
