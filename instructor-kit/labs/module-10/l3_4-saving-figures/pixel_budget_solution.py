# --- lab bootstrap: find labs_paths.py (the same three lines open every lab; see labs/README.md) ---
import pathlib, sys
sys.path[:0] = [str(p) for p in pathlib.Path(globals().get("__file__", "lab.py")).resolve().parents if (p / "labs_paths.py").is_file()]
from labs_paths import DATA, OUTPUT

# %% [markdown]
# # Lab 3.4-A · A pixel budget (SOLUTION)
# The Bend store manager wants one chart, "mean visitors by day of the week", in three places:
# an email, the staff newsletter (which needs an image exactly 1,400 pixels wide) and a printed
# poster. Same drawing code every time; only the sheet of paper and the scanner change.

# %% Load the data and write ONE drawing function
import matplotlib.pyplot as plt
import pandas as pd

daily = pd.read_csv(DATA / "daily_sales.csv", parse_dates=["date"])
bend = daily[daily["store"] == "Bend"]
by_day = bend.groupby(bend["date"].dt.dayofweek)["visitors"].mean()
DAYS = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
print("mean visitors by weekday:", by_day.round(0).astype(int).tolist())


def weekday_chart(figsize):
    """Draw Bend's mean visitors by weekday on a sheet of the given size (inches)."""
    fig, ax = plt.subplots(figsize=figsize, layout="constrained")
    ax.bar(DAYS, by_day.values, color="#667eea")
    ax.set_title("Bend: Saturday brings almost twice Tuesday's visitors", loc="left", fontweight="bold")
    ax.set_ylabel("Mean visitors per day")
    ax.spines[["top", "right"]].set_visible(False)
    return fig


def pixels(path):
    """Width and height of a saved PNG, read back from the file."""
    rows, cols = plt.imread(path).shape[:2]
    return cols, rows


# %% Step 1: the email version. Predict first: 7 x 3.5 inches at 100 dpi is ... pixels
fig = weekday_chart((7, 3.5))
email = OUTPUT / "bend_email.png"
fig.savefig(email, dpi=100)
plt.close(fig)
print("email:", pixels(email), f"{email.stat().st_size / 1024:.0f} KB")

# %% Step 2: two ways to reach 1,400 pixels wide for the newsletter
big = weekday_chart((14, 7))                 # a big sheet, scanned coarsely
big.savefig(OUTPUT / "bend_news_big_sheet.png", dpi=100)
plt.close(big)

small = weekday_chart((7, 3.5))              # a small sheet, scanned finely
small.savefig(OUTPUT / "bend_news_small_sheet.png", dpi=200)
plt.close(small)

for name in ("bend_news_big_sheet.png", "bend_news_small_sheet.png"):
    print(f"{name:<28}", pixels(OUTPUT / name))
print("Same pixels. On the 7 x 3.5 inch sheet the text is twice as large relative")
print("to the chart: a 12-point title is 12/72 inch on any sheet, and the dpi then")
print("scales the whole sheet.")
print("title height in pixels: big sheet", round(12 / 72 * 100, 1), "| small sheet", round(12 / 72 * 200, 1))

# %% Step 3: the poster. Vector formats have no pixels at all
poster = weekday_chart((7, 3.5))
for extension in ("pdf", "svg"):
    path = OUTPUT / f"bend_poster.{extension}"
    poster.savefig(path)
    print(f"{path.name:<16} {path.stat().st_size / 1024:5.1f} KB (vector: no pixel size to check)")
plt.close(poster)

# %% Step 4: the report every export script should end with
files = sorted(p.name for p in OUTPUT.iterdir())
print(f"{len(files)} files in OUTPUT:", *files, sep="\n  ")
print("open figures:", len(plt.get_fignums()))
