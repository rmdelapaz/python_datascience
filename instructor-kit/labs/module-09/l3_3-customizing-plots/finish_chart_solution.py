# --- lab bootstrap: find labs_paths.py (the same three lines open every lab; see labs/README.md) ---
import pathlib, sys
sys.path[:0] = [str(p) for p in pathlib.Path(globals().get("__file__", "lab.py")).resolve().parents if (p / "labs_paths.py").is_file()]
from labs_paths import DATA, OUTPUT

# %% [markdown]
# # Lab 3.3-A · From first draft to finished chart (SOLUTION)

# %% Load
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

# %% The first draft
fig, ax = plt.subplots(figsize=(9, 4.2), layout="constrained")
for year in by_month.columns:
    ax.plot(by_month.index, by_month[year], label=str(year))
ax.set_title("Online revenue by month")
ax.legend()
fig.savefig(OUTPUT / "draft.png")
plt.close(fig)

# %% Step 1: check the story first
gap = by_month[2025] - by_month[2024]
best = gap.idxmax()
print("months in which 2025 beat 2024:", int((gap > 0).sum()), "of 12")
print(f"largest gap: {MONTHS[best - 1]}, ${gap[best]:,.0f} | smallest gap: {MONTHS[gap.idxmin() - 1]}, ${gap.min():,.0f}")
print(f"full year: ${by_month[2024].sum():,.0f} -> ${by_month[2025].sum():,.0f} "
      f"({(by_month[2025].sum() / by_month[2024].sum() - 1) * 100:.1f}%)")

# %% Steps 2 to 5: the edits, each in a small function
def add_titles(ax, headline, subtitle):
    ax.set_title(headline, loc="left", fontsize=13, fontweight="bold", pad=24)
    ax.text(0, 1.03, subtitle, transform=ax.transAxes, fontsize=10, color="0.35")

def thousands(x, pos):
    return f"${x / 1000:,.0f}K"

def format_axes(ax):
    ax.yaxis.set_major_formatter(FuncFormatter(thousands))
    ax.set_xticks(range(1, 13), labels=MONTHS)
    ax.set_ylim(bottom=0)

def label_line_ends(ax):
    for line in ax.lines:
        x, y = line.get_xdata()[-1], line.get_ydata()[-1]
        ax.annotate(line.get_label(), xy=(x, y), xytext=(6, 0), textcoords="offset points",
                    va="center", fontsize=10, color=line.get_color(), fontweight="bold")
    left, right = ax.get_xlim()
    ax.set_xlim(left, right + 0.06 * (right - left))

def clean_up(ax):
    ax.spines[["top", "right"]].set_visible(False)
    ax.tick_params(length=0)
    ax.grid(axis="y", color="0.9")
    ax.set_axisbelow(True)

fig, ax = plt.subplots(figsize=(9, 4.2), layout="constrained")
ax.plot(by_month.index, by_month[2024], color="0.6", linewidth=1.5, label="2024")
ax.plot(by_month.index, by_month[2025], color="#667eea", linewidth=2.8, label="2025")
add_titles(ax, "Online revenue beat 2024 in every month of 2025",
           "Completed online orders, revenue per calendar month (USD)")
format_axes(ax)
label_line_ends(ax)
ax.annotate(f"{MONTHS[best - 1]}: +${gap[best] / 1000:,.0f}K", xy=(best, by_month.loc[best, 2025]),
            xytext=(best - 3.2, by_month.loc[best, 2025] + 6000), arrowprops={"arrowstyle": "->", "color": "0.3"}, fontsize=9)
clean_up(ax)
fig.savefig(OUTPUT / "finished.png")
fig.canvas.draw()
print("y tick labels:", [t.get_text() for t in ax.get_yticklabels()][:4])
print("x tick labels:", [t.get_text() for t in ax.get_xticklabels()][:4], "...")
print("visible spines:", [side for side in ax.spines if ax.spines[side].get_visible()])
print("legend:", ax.get_legend())

plt.close("all")
print("saved:", sorted(p.name for p in OUTPUT.glob("*.png")))
