# --- lab bootstrap: find labs_paths.py (the same three lines open every lab; see labs/README.md) ---
import pathlib, sys
sys.path[:0] = [str(p) for p in pathlib.Path(globals().get("__file__", "lab.py")).resolve().parents if (p / "labs_paths.py").is_file()]
from labs_paths import DATA, OUTPUT

# %% [markdown]
# # Lab 3.3-A · From first draft to finished chart (STARTER)
# The online team will show one chart at the year-end meeting: completed online revenue, 2024 against 2025.
# You get the first draft. Edit it, one decision at a time, until a stranger gets the point in five seconds.
#
# Expected when you finish: "draft.png" and "finished.png" in output/, and printed checks:
#   - the number of months in which 2025 beat 2024 (your headline depends on it)
#   - the month with the largest gap
#   - the y tick labels in thousands of dollars, the x tick labels as month names
#   - the visible spines of the finished chart: only left and bottom

# %% Load (done for you): one row per calendar month, one column per year
import matplotlib as mpl
import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.ticker import FuncFormatter

orders = pd.read_csv(DATA / "orders.csv", parse_dates=["order_date"])
done = orders[(orders["channel"] == "online") & (orders["status"] == "completed")]
by_month = done.groupby([done["order_date"].dt.year, done["order_date"].dt.month])["order_total"].sum().unstack(0)
by_month.index.name, by_month.columns.name = "month", "year"
print(by_month.round(0).head(3))
MONTHS = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]

# %% The first draft (done for you)
fig, ax = plt.subplots(figsize=(9, 4.2), layout="constrained")
for year in by_month.columns:
    ax.plot(by_month.index, by_month[year], label=str(year))
ax.set_title("Online revenue by month")
ax.legend()
fig.savefig(OUTPUT / "draft.png")
plt.close(fig)

# %% Step 1: check the story with numbers BEFORE writing a headline
# TODO 1: gap = by_month[2025] - by_month[2024]. Print how many months gap > 0, and gap.idxmax() with its size.

# %% Step 2: a headline that states the finding, a subtitle that says what is plotted
# TODO 2: write add_titles(ax, headline, subtitle) as in the lesson (bold, loc="left", pad=24;
#         the subtitle with ax.text(0, 1.03, ..., transform=ax.transAxes, color="0.35")).

# %% Step 3: axes people can read
# TODO 3: y ticks as "$80K" with FuncFormatter; x ticks with ax.set_xticks(range(1, 13), labels=MONTHS);
#         start y at zero.

# %% Step 4: color with a purpose, and direct labels
# TODO 4: 2024 in gray ("0.6", linewidth 1.5), 2025 in "#667eea" (linewidth 2.8). No legend: write each year
#         at the end of its line with ax.annotate(..., xytext=(6, 0), textcoords="offset points").

# %% Step 5: point at the evidence, then clean up
# TODO 5: annotate the month with the largest gap (an arrow and its dollar gap); remove the top and right
#         spines; ax.tick_params(length=0); a faint y grid behind the data. Save "finished.png".
#         Print the visible spines.

plt.close("all")
print("saved:", sorted(p.name for p in OUTPUT.glob("*.png")))
