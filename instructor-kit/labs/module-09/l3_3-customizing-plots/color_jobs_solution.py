# --- lab bootstrap: find labs_paths.py (the same three lines open every lab; see labs/README.md) ---
import pathlib, sys
sys.path[:0] = [str(p) for p in pathlib.Path(globals().get("__file__", "lab.py")).resolve().parents if (p / "labs_paths.py").is_file()]
from labs_paths import DATA, OUTPUT

# %% [markdown]
# # Lab 3.3-B · Give color a job (SOLUTION)

# %% Load
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

daily = pd.read_csv(DATA / "daily_sales.csv", parse_dates=["date"])
daily["year"], daily["month"] = daily["date"].dt.year, daily["date"].dt.month
visitors = daily.pivot_table(index="store", columns="month", values="visitors", aggfunc="mean")
revenue = daily.pivot_table(index=["store", "month"], columns="year", values="revenue", aggfunc="sum")
yoy = ((revenue[2025] / revenue[2024] - 1) * 100).unstack("month")
print("visitors table:", visitors.shape, "| change table:", yoy.shape)
MONTHS = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]

# %% Step 1: sequential
fig, ax = plt.subplots(figsize=(9, 3.2), layout="constrained")
image = ax.imshow(visitors.values, cmap="viridis", aspect="auto")
fig.colorbar(image, ax=ax, label="Mean visitors per day")
ax.set_xticks(range(12), labels=MONTHS)
ax.set_yticks(range(4), labels=visitors.index)
ax.set_title("Boise is the busiest store in every month; summer and December are busiest everywhere",
             loc="left", fontweight="bold", fontsize=10)
fig.savefig(OUTPUT / "heat_visitors.png")
print(f"Step 1: lowest cell {visitors.min().min():.0f}, highest cell {visitors.max().max():.0f}")

# %% Step 2: diverging, centered on zero
limit = float(np.nanmax(np.abs(yoy.values)))
fig, ax = plt.subplots(figsize=(9, 3.2), layout="constrained")
image = ax.imshow(yoy.values, cmap="RdBu", vmin=-limit, vmax=limit, aspect="auto")
fig.colorbar(image, ax=ax, label="Change against same month of 2024 (%)")
ax.set_xticks(range(12), labels=MONTHS)
ax.set_yticks(range(4), labels=yoy.index)
ax.set_title("Flagstaff and Boise grew in every month; Asheville shrank in 9 of 12", loc="left", fontweight="bold", fontsize=10)
fig.savefig(OUTPUT / "heat_change.png")
print(f"Step 2: changes from {yoy.min().min():.1f}% to {yoy.max().max():.1f}%; color limits {-limit:.1f} to {limit:.1f}")

# %% Step 3: check what the colors claim
print("Step 3: months that shrank against 2024:", (yoy < 0).sum(axis=1).to_dict())
plt.close("all")
print("saved:", sorted(p.name for p in OUTPUT.glob("*.png")))
