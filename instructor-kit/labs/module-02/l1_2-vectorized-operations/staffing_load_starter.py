# --- lab bootstrap: find labs_paths.py (the same three lines open every lab; see labs/README.md) ---
import pathlib, sys
sys.path[:0] = [str(p) for p in pathlib.Path(globals().get("__file__", "lab.py")).resolve().parents if (p / "labs_paths.py").is_file()]
from labs_paths import DATA

# %% [markdown]
# # Lab 1.2-A · How stretched is the staff? (STARTER)
# The lesson measured conversion and basket value. Here the question is about people:
# how many visitors does each staff member look after, and on which days is a store stretched?
# Everything is one array expression or one mask. No loop over the 2,903 rows.
#
# Expected when you finish: the mean, smallest and largest visitors-per-staff figure,
# the number and share of "stretched" store-days (60 or more visitors per staff member),
# two counts from combined masks, a three-way label tally (quiet / steady / stretched),
# and the date and store of the most stretched day in two years.

# %% Load the columns (done for you)
import numpy as np


def load(col, dtype=float):
    """Read one column of daily_sales.csv into an array (the helper from Lesson 1.2)."""
    return np.genfromtxt(DATA / "daily_sales.csv", delimiter=",", skip_header=1, usecols=col, dtype=dtype)

dates = load(0, dtype="datetime64[D]")
stores = load(1, dtype=str)
visitors = load(2)
staff = load(6)          # staff_on_duty
promo = load(7)          # 1 on sale days
print(visitors[:4], staff[:4])

# %% Step 1: one expression for every store-day
# TODO 1: per_staff = visitors divided by staff, for all rows at once
per_staff = None

if per_staff is None:
    print("TODO 1-6 not done yet: `per_staff` is still None.")
else:
    # %% Step 2: summarize it
    # TODO 2: print the mean, min and max of per_staff, each rounded to 1 decimal place

    # %% Step 3: a mask, then count and measure
    # TODO 3: stretched = per_staff >= 60 ; print how many (sum) and what fraction (mean)

    # %% Step 4: combine masks (parentheses around every comparison; & for and, | for or)
    # TODO 4: print how many store-days were stretched AND a sale day,
    #         and how many were stretched OR a sale day

    # %% Step 5: three labels with np.select (first true condition wins)
    # TODO 5: "stretched" at 60 or more, "steady" at 45 or more, otherwise "quiet";
    #         tally them with np.unique(labels, return_counts=True)

    # %% Step 6: where and when was the most stretched day?
    # TODO 6: i = per_staff.argmax(); print dates[i], stores[i], visitors[i], staff[i]
    print("TODO 2-6: summarize, mask, combine, label, locate")
