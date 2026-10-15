# --- lab bootstrap: find labs_paths.py (the same three lines open every lab; see labs/README.md) ---
import pathlib, sys
sys.path[:0] = [str(p) for p in pathlib.Path(globals().get("__file__", "lab.py")).resolve().parents if (p / "labs_paths.py").is_file()]
from labs_paths import DATA

# %% [markdown]
# # Lab 4.6-A · Is the lift fading? (SOLUTION)
# A product manager worries about a NOVELTY EFFECT: "People click on anything new. I bet the
# new checkout page won big in week 1 and the gain has been shrinking ever since."
# A second colleague reads the weekly table and says the opposite: "It only worked in week 4."
# Question: do the four weeks, each taken by itself, tell a story of a lift that shrinks or grows?
#
# Skills: compare_rates on a slice, reading intervals instead of p-values, testing the
# difference between two lifts (never comparing two p-values).
#
# Reference solution. Do not hand out before the lab.

# %% Setup (done for you)
import numpy as np
import pandas as pd
from scipy import stats
from statsmodels.stats.proportion import proportions_ztest, confint_proportions_2indep

def compare_rates(df):
    """Treatment vs control conversion for the rows in df (the function from Lesson 4.6)."""
    s = df.groupby("variant")["converted"].agg(["sum", "count"])
    c_c, n_c = s.loc["control"]
    c_t, n_t = s.loc["treatment"]
    r_c, r_t = c_c / n_c, c_t / n_t
    ci = confint_proportions_2indep(c_t, n_t, c_c, n_c, compare="diff")
    return {"visitors": int(n_c + n_t), "control": r_c, "treatment": r_t,
            "diff": r_t - r_c, "ci_low": ci[0], "ci_high": ci[1],
            "se": np.sqrt(r_c * (1 - r_c) / n_c + r_t * (1 - r_t) / n_t),
            "p": proportions_ztest([c_t, c_c], [n_t, n_c])[1]}


def describe(label, r):
    print(f"{label:<12} {r['visitors']:>6,} visitors  {r['control']:.2%} -> {r['treatment']:.2%}  "
          f"{r['diff'] * 100:+.2f} pts (95% CI {r['ci_low'] * 100:+.2f} to {r['ci_high'] * 100:+.2f})  p = {r['p']:.4f}")

ab = pd.read_csv(DATA / "ab_test.csv", parse_dates=["date"])
print("rows:", len(ab), "| days:", ab["date"].nunique())

# %% Step 1: a week number for every visitor
ab["week"] = (ab["date"] - ab["date"].min()).dt.days // 7 + 1
print(ab["week"].value_counts().sort_index().to_string())

# %% Step 2: each week BY ITSELF (not cumulative, so this is not the peeking table)
print()
weekly = {wk: compare_rates(ab[ab["week"] == wk]) for wk in [1, 2, 3, 4]}
for wk, r in weekly.items():
    describe(f"week {wk}", r)
print("weeks whose own p-value is below 0.05:", [wk for wk, r in weekly.items() if r["p"] < 0.05])
print("weeks whose interval contains the overall lift of +1.17 points:",
      [wk for wk, r in weekly.items() if r["ci_low"] <= 0.0117 <= r["ci_high"]])

# %% Step 3: first half against second half
print()
early = compare_rates(ab[ab["week"] <= 2])
late = compare_rates(ab[ab["week"] >= 3])
describe("weeks 1-2", early)
describe("weeks 3-4", late)
gap = late["diff"] - early["diff"]
gap_se = np.sqrt(early["se"] ** 2 + late["se"] ** 2)
p_gap = 2 * stats.norm.sf(abs(gap / gap_se))
print(f"Late lift minus early lift: {gap * 100:+.2f} points (standard error {gap_se * 100:.2f}), p = {p_gap:.2f}")

# %% Step 4: say it
print()
print("Verdict: every week shows a positive lift (about +0.8 to +2.1 points) and every weekly interval")
print("contains the overall +1.17. One week of 7,000 visitors is too small to be significant alone,")
print("so 'only week 4 worked' is a power problem, not a finding. The late lift is not smaller than the")
print(f"early one ({late['diff'] * 100:+.2f} vs {early['diff'] * 100:+.2f} points, p = {p_gap:.2f} for the difference):")
print("no sign of a novelty effect in these four weeks. This check was not in the plan: exploratory.")
