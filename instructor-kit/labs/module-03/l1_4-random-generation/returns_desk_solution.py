# --- lab bootstrap: find labs_paths.py (the same three lines open every lab; see labs/README.md) ---
import pathlib, sys
sys.path[:0] = [str(p) for p in pathlib.Path(globals().get("__file__", "lab.py")).resolve().parents if (p / "labs_paths.py").is_file()]
from labs_paths import DATA

# %% [markdown]
# # Lab 1.4-B · How busy is the returns desk? (SOLUTION)
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
rate = returns_per_day.mean()
print("average returns per day:", rate.round(3))

# %% Step 3: REPEAT. Simulate 100,000 days in one call.
sim = rng.poisson(lam=rate, size=100_000)
print("ten simulated days:", sim[:10])

# %% Step 4: COUNT, and check against the real days
print(f"4 or more returns: simulated {(sim >= 4).mean():.1%} | real {(returns_per_day >= 4).mean():.1%}")

# %% Step 5: days with no returns at all
print(f"no returns at all: simulated {(sim == 0).mean():.1%} | real {(returns_per_day == 0).mean():.1%}")
print("mean and variance of the real counts:", returns_per_day.mean().round(2), returns_per_day.var().round(2))
# The model passes its check: for a Poisson the mean and the variance are equal, and here
# they nearly are. About 7 days in 100 bring 4 or more returns.

# %% Step 6: the same model on a different question
sim_orders = rng.poisson(lam=orders_per_day.mean(), size=100_000)
print(f"40 or more orders: simulated {(sim_orders >= 40).mean():.1%} | real {(orders_per_day >= 40).mean():.1%}")
print("mean and variance of real orders per day:", orders_per_day.mean().round(2), orders_per_day.var().round(2))
# Here the model fails: real days vary far more than a Poisson allows (the variance is more
# than twice the mean). Orders have weekends, seasons and sale days; a single average rate
# knows none of that. More simulations would not help. Only a better model would.
