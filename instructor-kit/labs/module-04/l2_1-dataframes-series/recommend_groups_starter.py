# --- lab bootstrap: find labs_paths.py (the same three lines open every lab; see labs/README.md) ---
import pathlib, sys
sys.path[:0] = [str(p) for p in pathlib.Path(globals().get("__file__", "lab.py")).resolve().parents if (p / "labs_paths.py").is_file()]
from labs_paths import DATA
# %% [markdown]
# # Lab 2.1-B · Who would recommend us? (STARTER)
# Question: the survey asks "How likely are you to recommend us?" from 0 to 10.
# Split the answers into three groups and compare Asheville shoppers with everyone.
#
#   promoter  = 9 or 10      passive = 7 or 8      detractor = 0 to 6
#   score     = % promoters minus % detractors, among people who answered
#
# Expected when you finish: a count of the four groups (the fourth is "no answer"),
# the score for all shoppers and for Asheville shoppers, and a line that proves the
# full survey table was not changed when you changed the Asheville piece.

# %% Load (done for you)
import pandas as pd

survey = pd.read_csv(DATA / "survey.csv")
print(survey.shape)
print(survey["recommend"].value_counts(dropna=False).sort_index().to_string())

# %% Step 1: a new column, filled with .loc
# TODO 1: survey["group"] = "no answer"
#         then three lines of the shape  survey.loc[mask, "group"] = "..."
#         (>= 9 promoter, .between(7, 8) passive, <= 6 detractor)
#         A comparison with a missing value is False, so the 54 blanks stay "no answer".

# %% Step 2: count the groups
# TODO 2: print survey["group"].value_counts()

# %% Step 3: the score, with two masks
# TODO 3: answered = survey["recommend"].notna()
#         The mean of a mask is the share of True values, so
#         (survey.loc[answered, "group"] == "promoter").mean() is the share of promoters.
#         score = (share of promoters - share of detractors) * 100, rounded to 1 decimal.
score = None

# %% Step 4: the same for one store, and a copy-on-write check
# TODO 4: asheville = survey[survey["store"] == "Asheville"]
#         Compute its score the same way, then set asheville["group"] = "checked"
#         and count how many rows of `survey` say "checked" (predict the number first).
asheville_score = None

# %% Report
if "group" not in survey.columns or score is None or asheville_score is None:
    print("TODOs not done yet: add the group column, then score and asheville_score.")
else:
    print("score, all shoppers:", score)
    print("score, Asheville   :", asheville_score)
