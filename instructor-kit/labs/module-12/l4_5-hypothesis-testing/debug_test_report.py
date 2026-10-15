# --- lab bootstrap: find labs_paths.py (the same three lines open every lab; see labs/README.md) ---
import pathlib, sys
sys.path[:0] = [str(p) for p in pathlib.Path(globals().get("__file__", "lab.py")).resolve().parents if (p / "labs_paths.py").is_file()]
from labs_paths import DATA

# %% [markdown]
# # Lab 4.5 · Find the bugs: a test report with five problems (DEBUG HANDOUT)
# Every cell runs. Each printed conclusion is wrong, overstated, or computed the wrong way.
# For each one: what is wrong, and what should the code or the sentence say?
# There is no solution file: the lesson's "What a p-value Is Not" table and its Common
# Mistakes are the answer.

# %%
import numpy as np
import pandas as pd
from scipy import stats

survey = pd.read_csv(DATA / "survey.csv")
in_store = survey[survey["store"] != "Online"]
ash = in_store.loc[in_store["store"] == "Asheville", "recommend"]          # note: no dropna
oth = in_store.loc[in_store["store"] != "Asheville", "recommend"].dropna()

# %% Conclusion 1
p1 = stats.ttest_ind(ash, oth, equal_var=False).pvalue
print("Conclusion 1: p =", p1, "-> the test shows nothing")

# %% Conclusion 2
p2 = stats.ttest_ind(ash.dropna(), oth, equal_var=False).pvalue
print(f"Conclusion 2: p = {p2:.3f}, so there is a {p2:.0%} chance that Asheville is no different")

# %% Conclusion 3
bend = survey.loc[survey["store"] == "Bend", "recommend"].dropna()
flag = survey.loc[survey["store"] == "Flagstaff", "recommend"].dropna()
p3 = stats.ttest_ind(bend, flag, equal_var=False).pvalue
print(f"Conclusion 3: p = {p3:.2f}, so Bend and Flagstaff customers are equally likely to recommend us")

# %% Conclusion 4
everyone = survey["recommend"].dropna()
p4 = stats.ttest_1samp(everyone, popmean=7.5).pvalue
print(f"Conclusion 4: p = {p4:.4f}, a highly significant result, so the shortfall from 7.5 is a big problem")

# %% Conclusion 5
p5 = stats.ttest_ind(ash.dropna(), oth, equal_var=False, alternative="less").pvalue
print(f"Conclusion 5: we saw Asheville was lower, so we tested 'less' and got p = {p5:.3f}")
