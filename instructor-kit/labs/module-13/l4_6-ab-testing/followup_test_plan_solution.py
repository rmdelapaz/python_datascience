# --- lab bootstrap: find labs_paths.py (the same three lines open every lab; see labs/README.md) ---
import pathlib, sys
sys.path[:0] = [str(p) for p in pathlib.Path(globals().get("__file__", "lab.py")).resolve().parents if (p / "labs_paths.py").is_file()]
from labs_paths import DATA

# %% [markdown]
# # Lab 4.6-B · Plan the follow-up test (SOLUTION)
# The checkout test's memo called the mobile result "exploratory" and asked for a follow-up
# test on mobile visitors only. Write the size part of that plan.
# Question: how many mobile visitors per arm, and how many days, does a mobile-only test need?
#
# Skills: proportion_effectsize, NormalIndPower().solve_power and .power, turning visitors
# into days, and the "raw difference as effect size" mistake.
#
# Reference solution. Do not hand out before the lab.

# %% Setup (done for you)
import pandas as pd
from statsmodels.stats.power import NormalIndPower
from statsmodels.stats.proportion import proportion_effectsize

ab = pd.read_csv(DATA / "ab_test.csv", parse_dates=["date"])
mobile = ab[ab["device"] == "mobile"]
print("mobile visitors:", len(mobile), "in", mobile["date"].nunique(), "days")

# %% Step 1: the two planning inputs, from the data you already have
baseline = round(mobile.loc[mobile["variant"] == "control", "converted"].mean(), 3)
per_day = round(len(mobile) / mobile["date"].nunique())
print(f"baseline {baseline:.1%}, about {per_day} mobile visitors a day")

# %% Step 2: sample size for three possible targets
print()
plans = []
for target in [0.076, 0.080, 0.086]:
    h = proportion_effectsize(target, baseline)
    n = NormalIndPower().solve_power(effect_size=h, alpha=0.05, power=0.80)
    plans.append((target, n, 2 * n / per_day))
    print(f"detect {baseline:.1%} -> {target:.1%} (+{(target - baseline) * 100:.1f} points, h = {h:.4f}): "
          f"{n:>7,.0f} per arm, about {2 * n / per_day:>3.0f} days")

# %% Step 3: what would four full weeks buy?
print()
n_28 = per_day * 28 / 2
power_28 = NormalIndPower().power(effect_size=proportion_effectsize(0.080, baseline), nobs1=n_28, alpha=0.05)
print(f"28 days = {n_28:,.0f} mobile visitors per arm")
print(f"power of a 28-day test for 6.8% -> 8.0%: {power_28:.2f}")
power_small = NormalIndPower().power(effect_size=proportion_effectsize(0.076, baseline), nobs1=n_28, alpha=0.05)
print(f"power of the same test for 6.8% -> 7.6%: {power_small:.2f}")

# %% Step 4: the silent mistake
print()
wrong_n = NormalIndPower().solve_power(effect_size=0.012, alpha=0.05, power=0.80)
print(f"with the raw difference 0.012 as effect size: {wrong_n:,.0f} per arm (wrong: effect_size is Cohen's h)")

# %% The plan, in one paragraph
print()
print("Plan: mobile visitors only, 50/50 at random, primary metric conversion per visitor, two-sided,")
print(f"alpha 0.05. Run 28 days (four full weeks, about {n_28:,.0f} per arm): {power_28:.0%} power to detect")
print(f"6.8% -> 8.0%. A true lift as small as 0.8 points would be caught only {power_small:.0%} of the time;")
print("say so in the plan. One analysis, after day 28.")
