# --- lab bootstrap: find labs_paths.py (the same three lines open every lab; see labs/README.md) ---
import pathlib, sys
sys.path[:0] = [str(p) for p in pathlib.Path(globals().get("__file__", "lab.py")).resolve().parents if (p / "labs_paths.py").is_file()]
from labs_paths import DATA

# %% [markdown]
# # Lab 4.6-B · Plan the follow-up test (STARTER)
# The checkout test's memo called the mobile result "exploratory" and asked for a follow-up
# test on mobile visitors only. Write the size part of that plan.
# Question: how many mobile visitors per arm, and how many days, does a mobile-only test need?
#
# Skills: proportion_effectsize, NormalIndPower().solve_power and .power, turning visitors
# into days, and the "raw difference as effect size" mistake.
#
# Expected when you finish: the mobile baseline rate and visitors per day, three lines
# (one per target rate) with visitors per arm and days, the power of a 28-day test, and
# the wrong answer you get from passing the raw difference as the effect size.

# %% Setup (done for you)
import pandas as pd
from statsmodels.stats.power import NormalIndPower
from statsmodels.stats.proportion import proportion_effectsize

ab = pd.read_csv(DATA / "ab_test.csv", parse_dates=["date"])
mobile = ab[ab["device"] == "mobile"]
print("mobile visitors:", len(mobile), "in", mobile["date"].nunique(), "days")

# %% Step 1: the two planning inputs, from the data you already have
# TODO 1: baseline = conversion rate of mobile visitors in the CONTROL arm, rounded to 3 decimals.
#         per_day  = mobile visitors per day (both arms together), as a whole number.
baseline = None
per_day = None

# %% Step 2: sample size for three possible targets
# The old test saw 8.6% on mobile. Planning on the observed rate is optimistic (lucky tests
# overstate their effect), so size the test for smaller lifts as well.
# TODO 2: for each target in [0.076, 0.080, 0.086]:
#             h = proportion_effectsize(target, baseline)
#             n = NormalIndPower().solve_power(effect_size=h, alpha=0.05, power=0.80)
#         and store (target, n, days) in `plans`, where days = 2 * n / per_day.
plans = []

# %% Step 3: what would four full weeks buy?
# TODO 3: n_28 = visitors per arm in 28 days (per_day * 28 / 2). Use
#         NormalIndPower().power(effect_size=..., nobs1=n_28, alpha=0.05) for the 6.8% -> 8.0% plan.
power_28 = None

# %% Step 4: the silent mistake
# TODO 4: call solve_power with effect_size=0.012 (the raw difference 0.080 - 0.068) and compare
#         the answer with the 8.0% line above.
wrong_n = None

# %% Report
if baseline is None or not plans:
    print("TODO 1-2 not done yet: `baseline` is None and `plans` is empty.")
else:
    print(f"baseline {baseline:.1%}, about {per_day} mobile visitors a day")
    for target, n, days in plans:
        print(f"detect {baseline:.1%} -> {target:.1%}: {n:>7,.0f} per arm, about {days:>3.0f} days")
if power_28 is not None:
    print(f"power of a 28-day test for 6.8% -> 8.0%: {power_28:.2f}")
if wrong_n is not None:
    print(f"with the raw difference as effect size: {wrong_n:,.0f} per arm (wrong)")
