# --- lab bootstrap: find labs_paths.py (the same three lines open every lab; see labs/README.md) ---
import pathlib, sys
sys.path[:0] = [str(p) for p in pathlib.Path(globals().get("__file__", "lab.py")).resolve().parents if (p / "labs_paths.py").is_file()]
from labs_paths import DATA, OUTPUT

# %% [markdown]
# # Lab 3.2-A · Foot traffic on one page (STARTER)
# Question: which store's foot traffic is growing, and how big is each store's traffic next to the others?
# Every figure: plt.subplots(...) or plt.subplot_mosaic(...) with layout="constrained", methods on each Axes,
# fig.savefig(OUTPUT / "name.png"). No plt.show() in a lab file.
#
# Expected when you finish (four PNG files in output/):
#   - a 2 x 2 grid with separate y scales, and the four y ranges printed (they differ)
#   - the same grid with sharey=True: one y range for all four (printed: True)
#   - small multiples: each store in color with the other three in gray behind it
#   - a Flagstaff summary built with subplot_mosaic: a wide trend panel and two smaller ones

# %% Load (done for you): mean visitors per day, one row per month, one column per store
import matplotlib.pyplot as plt
import pandas as pd

daily = pd.read_csv(DATA / "daily_sales.csv", parse_dates=["date"])
daily["month"] = daily["date"].dt.to_period("M").dt.to_timestamp()
traffic = daily.pivot_table(index="month", columns="store", values="visitors", aggfunc="mean")
stores = list(traffic.columns)
print("monthly mean visitors:", traffic.shape, stores)

# %% Step 1: a 2 x 2 grid, each panel with its own scale
# TODO 1: fig, axs = plt.subplots(2, 2, figsize=(9, 5.5), layout="constrained")
#         loop:  for ax, store in zip(axs.flat, stores):  plot traffic[store], set the panel title.
#         Add fig.suptitle(...) that SAYS the scales differ. Save "grid_own_scales.png".
#         Print [ax.get_ylim() for ax in axs.flat] rounded: are the four ranges the same?

# %% Step 2: the same grid on one scale
# TODO 2: the same figure with sharex=True, sharey=True and fig.supylabel("Visitors per day").
#         Save "grid_shared.png". Print whether axs[0, 0].get_ylim() == axs[1, 1].get_ylim().

# %% Step 3: small multiples with context
# TODO 3: write draw_store(ax, table, store): every OTHER store in "lightgray" (linewidth=1),
#         then `store` in "#667eea" (linewidth=2), then the title.
#         Use it in a 1 x 4 grid (figsize=(10, 2.8), sharey=True). Save "small_multiples.png".

# %% Step 4: one store, three views, with a named layout
flag = daily[daily["store"] == "Flagstaff"]
by_weekday = flag.groupby(flag["date"].dt.dayofweek)["visitors"].mean()   # 0 = Monday
print("Flagstaff rows:", len(flag))
# TODO 4: fig, axd = plt.subplot_mosaic([["trend", "trend"], ["week", "spread"]], figsize=(9, 6), layout="constrained")
#         axd["trend"]: traffic["Flagstaff"] as a line;  axd["week"]: bars of by_weekday (Mon..Sun);
#         axd["spread"]: a histogram of flag["visitors"] (bins=30). Titles on all three, one suptitle.
#         Save "flagstaff_summary.png". Print list(axd).

# %% Last cell (done for you)
plt.close("all")
saved = sorted(p.name for p in OUTPUT.glob("*.png"))
print("saved:", saved if saved else "nothing yet: the TODOs are still open")
