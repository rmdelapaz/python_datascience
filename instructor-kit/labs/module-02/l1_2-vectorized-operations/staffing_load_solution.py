# --- lab bootstrap: find labs_paths.py (the same three lines open every lab; see labs/README.md) ---
import pathlib, sys
sys.path[:0] = [str(p) for p in pathlib.Path(globals().get("__file__", "lab.py")).resolve().parents if (p / "labs_paths.py").is_file()]
from labs_paths import DATA

# %% [markdown]
# # Lab 1.2-A · How stretched is the staff? (SOLUTION)
# Reference answers. Hand out only after the lab.

# %% Load the columns
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
per_staff = visitors / staff

# %% Step 2: summarize it
print("visitors per staff member: mean", per_staff.mean().round(1),
      "| min", per_staff.min().round(1), "| max", per_staff.max().round(1))

# %% Step 3: a mask, then count and measure
stretched = per_staff >= 60
print(stretched.sum(), "stretched store-days,", f"{stretched.mean():.1%} of all store-days")

# %% Step 4: combine masks
is_promo = promo == 1
print("stretched AND sale day:", (stretched & is_promo).sum())
print("stretched OR sale day: ", (stretched | is_promo).sum())

# %% Step 5: three labels with np.select (first true condition wins)
labels = np.select([per_staff >= 60, per_staff >= 45], ["stretched", "steady"], default="quiet")
names, counts = np.unique(labels, return_counts=True)
for name, count in zip(names, counts):
    print(f"{name:<10}{count:>6}")

# %% Step 6: where and when was the most stretched day?
i = per_staff.argmax()
print("most stretched:", dates[i], stores[i], "|", int(visitors[i]), "visitors,", int(staff[i]), "staff")

# %% Extra: is any store more stretched than the others? (a loop over 4 stores is fine)
for name in np.unique(stores):
    m = stores == name
    print(f"{name:<10} staff {staff[m].mean():>5.2f}   visitors per staff {per_staff[m].mean():>5.1f}")
# The four stores are close (52 to 58): staff are scheduled from expected demand,
# so a bigger store simply has more people on duty.
