# --- lab bootstrap: find labs_paths.py (the same three lines open every lab; see labs/README.md) ---
import pathlib, sys
sys.path[:0] = [str(p) for p in pathlib.Path(globals().get("__file__", "lab.py")).resolve().parents if (p / "labs_paths.py").is_file()]
from labs_paths import DATA

# %% [markdown]
# # Lab 4.6-C · An A/A test (STARTER)
# Before trusting a testing setup, teams run an A/A test: both "arms" see the SAME page.
# Any significant result is then a false alarm by construction.
# Question: if we split the control visitors at random into two fake arms, again and again,
# how often does the two-proportion test call a winner at alpha = 0.05?
#
# Skills: a seeded simulation with NumPy, the two-proportion test from the lesson,
# reading a false-alarm rate, and why one "significant" A/A result is not a broken test.
#
# Expected when you finish: the p-value of one random split, then the share of 2,000 random
# splits with p < 0.05 (close to 5%), the share below 0.01 and the smallest p-value seen.

# %% Setup (done for you)
import numpy as np
import pandas as pd
from scipy import stats

ab = pd.read_csv(DATA / "ab_test.csv", parse_dates=["date"])
control = ab.loc[ab["variant"] == "control", "converted"].to_numpy()
print("control visitors:", len(control), "| conversions:", control.sum(), f"| rate: {control.mean():.2%}")


def p_two_prop(c1, n1, c2, n2):
    """Two-sided p-value for the difference between two proportions (pooled z-test, from Lesson 4.6)."""
    pooled = (c1 + c2) / (n1 + n2)
    se = np.sqrt(pooled * (1 - pooled) * (1 / n1 + 1 / n2))
    z = (c1 / n1 - c2 / n2) / se
    return 2 * stats.norm.sf(np.abs(z))


# %% Step 1: one A/A split
# TODO 1: shuffle `control` with rng.permutation, call the first half arm A and the rest arm B,
#         and compute the p-value with p_two_prop(a.sum(), len(a), b.sum(), len(b)).
rng = np.random.default_rng(42)
half = len(control) // 2
p_one = None

# %% Step 2: 2,000 A/A splits
# TODO 2: repeat step 1 in a loop 2,000 times (keep using the same rng) and collect the
#         p-values in a NumPy array called p_values.
p_values = np.array([])

# %% Step 3: read the result
# TODO 3: print the share of p_values below 0.05, the share below 0.01 and the smallest p-value.
#         Then answer in a comment: your colleague ran ONE A/A test and got p = 0.03.
#         Is the testing tool broken?
if p_one is None or len(p_values) == 0:
    print("TODO 1-3 not done yet: `p_one` is None and `p_values` is empty.")
