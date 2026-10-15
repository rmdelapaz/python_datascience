# --- lab bootstrap: find labs_paths.py (the same three lines open every lab; see labs/README.md) ---
import pathlib, sys
sys.path[:0] = [str(p) for p in pathlib.Path(globals().get("__file__", "lab.py")).resolve().parents if (p / "labs_paths.py").is_file()]
from labs_paths import DATA, OUTPUT

# %% [markdown]
# # Lab 3.4 · Find the bugs: the slide that arrived blank (DEBUG HANDOUT)
# A colleague's export script runs without a single error message, and still gets three
# things wrong. Run it, read what it prints, then fix it. There is no solution file: the
# lesson's Common Mistakes 3, 4 and 5 are the answer.
#
# When it is fixed, the last three lines should say:
#   slide is 1920 x 1080: True
#   slide is blank: False
#   open figures: 0

# %%
import matplotlib.pyplot as plt
import pandas as pd

daily = pd.read_csv(DATA / "daily_sales.csv", parse_dates=["date"])
monthly = daily.set_index("date")["revenue"].resample("MS").sum()

# The chart for the slide. "The text was too small, so I made the figure really big."
chart, ax = plt.subplots(figsize=(19.2, 10.8), layout="constrained")
ax.plot(monthly.index, monthly.values, color="#667eea")
ax.set_title("All stores: monthly in-store revenue")

# A quick look at something else on the way...
scratch = plt.figure()

# ...and then the save. Three problems live in the next line.
slide = OUTPUT / "revenue_slide.png"
plt.savefig(slide, dpi=100, bbox_inches="tight")

# %% The evidence
image = plt.imread(slide)
height, width = image.shape[:2]
print("saved size:", width, "x", height)
print("slide is 1920 x 1080:", (width, height) == (1920, 1080))
print("slide is blank:", bool((image[..., :3] == 1).all()))
print("open figures:", len(plt.get_fignums()))

# Questions:
# 1. Which figure did plt.savefig() save, and how do you say which one you mean?
# 2. Why is the file not 1920 x 1080 even though 19.2 inches x 100 dpi is 1920?
# 3. The text on the real chart is tiny on a slide. Which two numbers do you change, and
#    which number must stay the same?
# 4. What is missing at the end?
