# --- lab bootstrap: find labs_paths.py (the same three lines open every lab; see labs/README.md) ---
import pathlib, sys
sys.path[:0] = [str(p) for p in pathlib.Path(globals().get("__file__", "lab.py")).resolve().parents if (p / "labs_paths.py").is_file()]
from labs_paths import DATA
# %% [markdown]
# # Lab 2.1-B · Who would recommend us? (SOLUTION)
# promoter = 9 or 10, passive = 7 or 8, detractor = 0 to 6;
# score = % promoters minus % detractors, among people who answered.

# %% Load
import pandas as pd

survey = pd.read_csv(DATA / "survey.csv")
print(survey.shape)

# %% Step 1: a new column, filled with .loc
survey["group"] = "no answer"
survey.loc[survey["recommend"] >= 9, "group"] = "promoter"
survey.loc[survey["recommend"].between(7, 8), "group"] = "passive"
survey.loc[survey["recommend"] <= 6, "group"] = "detractor"

# %% Step 2: count the groups
print(survey["group"].value_counts().to_string())


# %% Step 3: the score, with two masks
def recommend_score(table):
    """% promoters minus % detractors among the rows that have an answer."""
    answered = table["recommend"].notna()
    groups = table.loc[answered, "group"]
    return round(((groups == "promoter").mean() - (groups == "detractor").mean()) * 100, 1)


score = recommend_score(survey)
print("score, all shoppers:", score)

# %% Step 4: the same for one store, and a copy-on-write check
asheville = survey[survey["store"] == "Asheville"]
asheville_score = recommend_score(asheville)
print("Asheville responses:", len(asheville), "| answered:", asheville["recommend"].notna().sum())
print("score, Asheville   :", asheville_score)

asheville["group"] = "checked"          # changes the piece only
print("rows of survey that say 'checked':", (survey["group"] == "checked").sum())
print("rows of asheville that say 'checked':", (asheville["group"] == "checked").sum())
