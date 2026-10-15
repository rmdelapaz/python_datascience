# --- lab bootstrap: find labs_paths.py (the same three lines open every lab; see labs/README.md) ---
import pathlib, sys
sys.path[:0] = [str(p) for p in pathlib.Path(globals().get("__file__", "lab.py")).resolve().parents if (p / "labs_paths.py").is_file()]
from labs_paths import DATA, OUTPUT

# %% [markdown]
# # Lab 3.4-A · A pixel budget (STARTER)
# The Bend store manager wants one chart, "mean visitors by day of the week", in three places:
# an email, the staff newsletter (which needs an image exactly 1,400 pixels wide) and a printed
# poster. Same drawing code every time; only the sheet of paper and the scanner change.
#
# Expected when you finish: the email image is (700, 350); both newsletter images are
# (1400, 700); a PDF and an SVG exist; the report says "5 files in OUTPUT:" and the last line says "open figures: 0".
# Everything is saved into OUTPUT (an `output` folder next to this file). No plt.show() needed:
# open the saved files to look at them.

# %% Load the data and write ONE drawing function (done for you)
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


# %% Step 1: the email version
# Write your prediction here BEFORE you run: 7 x 3.5 inches at 100 dpi = ______ x ______ pixels
# TODO 1: draw the chart on a (7, 3.5) sheet, save it as OUTPUT / "bend_email.png" with dpi=100,
#         close the figure, then set `email` to the path you saved.
email = None

if email is None:
    print("TODO 1 not done yet: `email` is still None.")
else:
    print("email:", pixels(email), f"{email.stat().st_size / 1024:.0f} KB")

# %% Step 2: two ways to reach 1,400 pixels wide for the newsletter
# TODO 2: save "bend_news_big_sheet.png" from a (14, 7) sheet and "bend_news_small_sheet.png"
#         from a (7, 3.5) sheet. Choose each dpi so BOTH files are 1,400 x 700 pixels.
#         Close each figure after saving it.
news_done = False        # change to True when both files are saved

if not news_done:
    print("TODO 2 not done yet.")
else:
    for name in ("bend_news_big_sheet.png", "bend_news_small_sheet.png"):
        print(f"{name:<28}", pixels(OUTPUT / name))
    # TODO 3: open both files side by side. In which one is the text easier to read, and why?
    #         Replace the text below with your one-sentence answer.
    print("My answer: ...")

# %% Step 3: the poster. Vector formats have no pixels at all
# TODO 4: draw the chart once more on a (7, 3.5) sheet and save it twice, as
#         OUTPUT / "bend_poster.pdf" and OUTPUT / "bend_poster.svg". Close the figure.

# %% Step 4: the report every export script should end with
files = sorted(p.name for p in OUTPUT.iterdir())
print(f"{len(files)} files in OUTPUT:", *files, sep="\n  ")
print("open figures:", len(plt.get_fignums()), "(expected 0: create, draw, save, close)")
