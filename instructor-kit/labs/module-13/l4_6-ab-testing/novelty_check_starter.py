# --- lab bootstrap: find labs_paths.py (the same three lines open every lab; see labs/README.md) ---
import pathlib, sys
sys.path[:0] = [str(p) for p in pathlib.Path(globals().get("__file__", "lab.py")).resolve().parents if (p / "labs_paths.py").is_file()]
from labs_paths import DATA

# %% [markdown]
# # Lab 4.6-A · Is the lift fading? (STARTER)
# A product manager worries about a NOVELTY EFFECT: "People click on anything new. I bet the
# new checkout page won big in week 1 and the gain has been shrinking ever since."
# A second colleague reads the weekly table and says the opposite: "It only worked in week 4."
# Question: do the four weeks, each taken by itself, tell a story of a lift that shrinks or grows?
#
# Skills: compare_rates on a slice, reading intervals instead of p-values, testing the
# difference between two lifts (never comparing two p-values).
#
# Expected when you finish: four lines (one per week, each week by itself), two lines for
# the first and second half of the test, one line for the difference between the two halves
# with its p-value, and a sentence you could say to the product manager.

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
# TODO 1: add a column "week" with 1 for the first seven days of the test, 2 for the next
#         seven, and so on.  Hint: (ab["date"] - ab["date"].min()).dt.days // 7 + 1
ab["week"] = 0

# %% Step 2: each week BY ITSELF (not cumulative, so this is not the peeking table)
# TODO 2: for wk in 1..4 call compare_rates on ab[ab["week"] == wk] and print it with describe().
weekly = {}          # fill it as {1: {...}, 2: {...}, 3: {...}, 4: {...}}

# %% Step 3: first half against second half
# TODO 3: early = compare_rates(weeks 1 and 2), late = compare_rates(weeks 3 and 4).
#         Then test the DIFFERENCE between the two lifts:
#             gap    = late["diff"] - early["diff"]
#             gap_se = np.sqrt(early["se"] ** 2 + late["se"] ** 2)
#             p_gap  = 2 * stats.norm.sf(abs(gap / gap_se))
early = late = None

# %% Step 4: say it
# TODO 4: replace the text below with one or two sentences for the product manager.
verdict = "TODO: is the lift fading, growing, or neither? How do you know?"

# %% Report
if not weekly or early is None:
    print("TODO 1-3 not done yet: `weekly` is empty and `early`/`late` are None.")
else:
    for wk, r in weekly.items():
        describe(f"week {wk}", r)
    describe("weeks 1-2", early)
    describe("weeks 3-4", late)
print(verdict)
