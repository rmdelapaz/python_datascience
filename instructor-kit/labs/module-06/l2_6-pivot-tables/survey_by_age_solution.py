# --- lab bootstrap: find labs_paths.py (the same three lines open every lab; see labs/README.md) ---
import pathlib, sys
sys.path[:0] = [str(p) for p in pathlib.Path(globals().get("__file__", "lab.py")).resolve().parents if (p / "labs_paths.py").is_file()]
from labs_paths import DATA, OUTPUT
# %% [markdown]
# # Lab 2.6-B · Melt, pivot, stack: the survey by age group (SOLUTION)
# Question: which question does each age group score lowest, and how many answers are
# behind each average?

# %% Load
import pandas as pd

pd.set_option("display.width", 150)
pd.set_option("display.max_columns", 20)

survey = pd.read_csv(DATA / "survey.csv")
sat_cols = ["sat_overall", "sat_selection", "sat_price", "sat_staff", "sat_website"]
print(survey.shape)

# %% Step 1: wide to tidy
answers = survey.melt(id_vars=["response_id", "age_group"], value_vars=sat_cols,
                      var_name="item", value_name="score")
print("tidy rows:", len(answers), "=", len(survey), "responses x", len(sat_cols), "questions")

# %% Step 2: tidy to a grid of means, and a grid of counts
means = answers.pivot_table(index="age_group", columns="item", values="score", aggfunc="mean")
n = answers.pivot_table(index="age_group", columns="item", values="score", aggfunc="count")
print(means.round(2))
print(n)
print("repeated (age_group, item) pairs:", answers.duplicated(["age_group", "item"]).sum(),
      "-> pivot() cannot be used, pivot_table() must combine them")

# %% Step 3: read across each row
lowest = means.idxmin(axis=1)
print(lowest.to_dict())

# %% Step 4: back to tidy, and save
tidy_means = means.stack().rename("mean_score").reset_index()
tidy_means["mean_score"] = tidy_means["mean_score"].round(2)
tidy_means.to_csv(OUTPUT / "survey_by_age.csv", index=False)
back = pd.read_csv(OUTPUT / "survey_by_age.csv")
print("saved and read back:", back.shape, back.columns.tolist())
print(back.nsmallest(2, "mean_score").to_string(index=False))
