# --- lab bootstrap: find labs_paths.py (the same three lines open every lab; see labs/README.md) ---
import pathlib, sys
sys.path[:0] = [str(p) for p in pathlib.Path(globals().get("__file__", "lab.py")).resolve().parents if (p / "labs_paths.py").is_file()]
from labs_paths import DATA

# %% [markdown]
# # Lab 1.5-A · Payroll is a receipt (STARTER)
# Staff hours times pay rates, added up: the lesson's receipt with different things on it.
# Each part is ONE @. Before each one, write the shapes going in and the shape you expect out.
#
# Expected when you finish: a weighted average rating next to the plain average; the payroll
# for each of 7 days (shape (7,)); a (7, 2) table of payroll under two pay scales; each
# store's payroll for the week (shape (4,)); and three hourly rates recovered from three
# days of payroll totals, checked with np.allclose.

# %% Load (done for you)
import numpy as np


def load(col, dtype=float):
    """Read one column of daily_sales.csv into an array (the helper from Lesson 1.2)."""
    return np.genfromtxt(DATA / "daily_sales.csv", delimiter=",", skip_header=1, usecols=col, dtype=dtype)

staff = load(6)                                  # staff_on_duty, one value per store-day
week = staff[:28].reshape(7, 4)                  # 7 days x 4 stores: Asheville, Bend, Boise, Flagstaff
print(week)

rating = np.genfromtxt(DATA / "products.csv", delimiter=",", skip_header=1, usecols=9)
reviews = np.genfromtxt(DATA / "products.csv", delimiter=",", skip_header=1, usecols=10)
has_rating = ~np.isnan(rating)                   # 8 products have no reviews yet, so no rating
rating, reviews = rating[has_rating], reviews[has_rating]
print(rating.size, "rated products |", int(reviews.sum()), "reviews")

day_cost = np.array([168.0, 176.0, 184.0, 172.0])        # dollars per staff member per day, by store
pay_scales = np.array([[168.0, 180.0],                    # Asheville: current, proposed
                       [176.0, 188.0],                    # Bend
                       [184.0, 196.0],                    # Boise
                       [172.0, 184.0]])                   # Flagstaff

# %% Part 1: a dot product is a weighted sum.  (234,) @ (234,) -> one number
# TODO 1: plain = rating.mean() ; weighted = rating @ reviews / reviews.sum()
#         print both rounded to 3 places. Which is higher, and what does that tell you?
print("TODO 1: plain and weighted average rating")

# %% Part 2: matrix @ vector.  (7, 4) @ (4,) -> shape ________
# TODO 2: payroll_per_day = week @ day_cost ; print it and its shape
payroll_per_day = None
print("payroll per day:", payroll_per_day)

# %% Part 3: matrix @ matrix.  (7, 4) @ (4, 2) -> shape ________
# TODO 3: both = week @ pay_scales ; print its shape and the weekly total under each scale (sum over axis 0)
print("TODO 3: payroll under two pay scales")

# %% Part 4: per STORE instead of per day. week * day_cost broadcasts (a table and a row).
# TODO 4: per_store = (week * day_cost).sum(axis=0) ; print it.
#         Then explain in a comment why `day_cost @ week` raises an error, and what `week.T` would fix.
print("TODO 4: payroll per store")

# %% Part 5: run the receipt backward with np.linalg.solve
# Three days at a pop-up stall. Hours worked by a lead, a seller and a trainee, and the day's payroll:
hours = np.array([[8.0, 16.0, 4.0],
                  [8.0,  8.0, 8.0],
                  [4.0, 16.0, 0.0]])
payroll = np.array([548.0, 464.0, 392.0])
# TODO 5: rates = np.linalg.solve(hours, payroll) ; print rates, then check with np.allclose(hours @ rates, payroll)
print("TODO 5: three hourly rates")
