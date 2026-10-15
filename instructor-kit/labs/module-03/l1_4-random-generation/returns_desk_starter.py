# --- lab bootstrap: find labs_paths.py (the same three lines open every lab; see labs/README.md) ---
import pathlib, sys
sys.path[:0] = [str(p) for p in pathlib.Path(globals().get("__file__", "lab.py")).resolve().parents if (p / "labs_paths.py").is_file()]
from labs_paths import DATA

# %% [markdown]
# # Lab 1.4-B · How busy is the returns desk? (STARTER)
# Some of each day's orders are later returned. Customer service asks: "On how many days
# should we expect 4 or more returns from one day's orders?" You will answer by simulation
# (model, repeat, count) and then do what a careful analyst does: check the model against
# the 731 real days. Then you will try the same model on a question where it fails.
#
# Expected when you finish: the real average (about 1.56 returns per day), a simulated
# chance of 4 or more returns next to the real share of such days (they should be close),
# the same comparison for days with no returns at all, and then a second comparison,
# for days with 40 or more ORDERS, where the simulation and reality disagree badly.

# %% Count returns per day and orders per day (done for you)
import numpy as np

order_date = np.genfromtxt(DATA / "orders.csv", delimiter=",", skip_header=1, usecols=2, dtype="datetime64[D]")
status = np.genfromtxt(DATA / "orders.csv", delimiter=",", skip_header=1, usecols=5, dtype=str)

day_number = (order_date - order_date[0]).astype(int)            # 0 for 2024-01-01 ... 730 for 2025-12-31
orders_per_day = np.bincount(day_number, minlength=731)          # np.bincount counts how often each whole number appears
returns_per_day = np.bincount(day_number[status == "returned"], minlength=731)
print(returns_per_day.size, "days |", returns_per_day.sum(), "returned orders | first ten days:", returns_per_day[:10])

# %% Step 1: the generator, once, with a seed
rng = np.random.default_rng(14)

# %% Step 2: MODEL. Returns per day are counts of events at some average rate: a Poisson.
# TODO 2: rate = the mean of returns_per_day ; print it rounded to 3 places
rate = None

# %% Step 3: REPEAT. Simulate 100,000 days in ONE call (no loop).
# TODO 3: sim = rng.poisson(lam=rate, size=100_000)
sim = None

if sim is None:
    print("TODO 2-6 not done yet: `sim` is still None.")
else:
    # %% Step 4: COUNT. The chance of 4 or more returns is the mean of a mask.
    # TODO 4: print (sim >= 4).mean() and, next to it, the REAL share: (returns_per_day >= 4).mean()

    # %% Step 5: one more check: days with no returns at all (simulated and real)
    # TODO 5: the same two numbers for == 0

    # %% Step 6: the same model on a different question
    # TODO 6: simulate orders per day with rng.poisson(lam=orders_per_day.mean(), size=100_000)
    #         compare the simulated and real share of days with 40 or more orders.
    #         They disagree. Print orders_per_day.mean() and orders_per_day.var(): for a Poisson
    #         the two are about equal. What does the real data say, and why might that be?
    print("TODO 4-6: count, check against reality, then break the model")
