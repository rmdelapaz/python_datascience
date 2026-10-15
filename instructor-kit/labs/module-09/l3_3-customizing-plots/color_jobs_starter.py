# --- lab bootstrap: find labs_paths.py (the same three lines open every lab; see labs/README.md) ---
import pathlib, sys
sys.path[:0] = [str(p) for p in pathlib.Path(globals().get("__file__", "lab.py")).resolve().parents if (p / "labs_paths.py").is_file()]
from labs_paths import DATA, OUTPUT

# %% [markdown]
# # Lab 3.3-B · Give color a job (STARTER)
# Two tables, two different jobs for color.
#   visitors: mean visitors per day, store x month  -> a number from low to high   -> SEQUENTIAL
#   yoy:      revenue change against last year (%) -> above or below zero matters -> DIVERGING, centered on 0
#
# Expected when you finish: "heat_visitors.png" and "heat_change.png" in output/, and printed checks:
#   - the lowest and highest cell of each table
#   - the color limits of the change map (they must be symmetric around zero)
#   - how many store-months shrank, per store

# %% Load (done for you)
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

# %% Step 1: a sequential heatmap
# TODO 1: image = ax.imshow(visitors.values, cmap="viridis", aspect="auto"); fig.colorbar(image, ax=ax, label=...)
#         ax.set_xticks(range(12), labels=MONTHS); ax.set_yticks(range(4), labels=visitors.index)
#         A title that states what the reader should see. Save "heat_visitors.png".

# %% Step 2: a diverging heatmap that is centered
# TODO 2: limit = np.nanmax(np.abs(yoy.values)); use cmap="RdBu", vmin=-limit, vmax=limit, so that 0 is the
#         neutral middle color. Same ticks, a colorbar labeled in percent. Save "heat_change.png".
#         Why would vmin=yoy.min().min(), vmax=yoy.max().max() mislead?

# %% Step 3: check what the colors claim
# TODO 3: print (yoy < 0).sum(axis=1): the number of months each store shrank against 2024.
print("Expected at the end: two heatmaps and a count of shrinking months per store.")
