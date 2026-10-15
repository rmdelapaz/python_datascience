# --- lab bootstrap: find labs_paths.py (the same three lines open every lab; see labs/README.md) ---
import pathlib, sys
sys.path[:0] = [str(p) for p in pathlib.Path(globals().get("__file__", "lab.py")).resolve().parents if (p / "labs_paths.py").is_file()]
from labs_paths import DATA

# %% [markdown]
# # Lab 4.6-C · An A/A test (SOLUTION)
# Before trusting a testing setup, teams run an A/A test: both "arms" see the SAME page.
# Any significant result is then a false alarm by construction.
# Question: if we split the control visitors at random into two fake arms, again and again,
# how often does the two-proportion test call a winner at alpha = 0.05?
#
# Skills: a seeded simulation with NumPy, the two-proportion test from the lesson,
# reading a false-alarm rate, and why one "significant" A/A result is not a broken test.
#
# Reference solution. Do not hand out before the lab.

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
rng = np.random.default_rng(42)
half = len(control) // 2
shuffled = rng.permutation(control)
a, b = shuffled[:half], shuffled[half:]
p_one = p_two_prop(a.sum(), len(a), b.sum(), len(b))
print(f"one split: {a.mean():.2%} vs {b.mean():.2%}, p = {p_one:.3f}")

# %% Step 2: 2,000 A/A splits
p_values = []
for _ in range(2_000):
    shuffled = rng.permutation(control)
    a, b = shuffled[:half], shuffled[half:]
    p_values.append(p_two_prop(a.sum(), len(a), b.sum(), len(b)))
p_values = np.array(p_values)

# %% Step 3: read the result
print()
print(f"A/A splits with p < 0.05: {(p_values < 0.05).mean():.1%}  (the promised false-alarm rate is 5%)")
print(f"A/A splits with p < 0.01: {(p_values < 0.01).mean():.1%}")
print(f"smallest p-value in 2,000 splits: {p_values.min():.4f}")
print("p-value at the 10th, 30th, 50th, 70th, 90th percentile:", np.quantile(p_values, [0.1, 0.3, 0.5, 0.7, 0.9]).round(2))
print()
print("Reading: with no difference at all, about 1 split in 20 is 'significant', and p-values are spread")
print("evenly from 0 to 1. One significant A/A result is expected now and then; a rate far above 5% would")
print("mean the assignment or the counting is broken.")
print(f"Splits with a p-value as small as the real test's 0.0008: {(p_values <= 0.0008).sum()} of 2,000.")
