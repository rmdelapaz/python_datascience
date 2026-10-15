# --- lab bootstrap: find labs_paths.py (the same three lines open every lab; see labs/README.md) ---
import pathlib, sys
sys.path[:0] = [str(p) for p in pathlib.Path(globals().get("__file__", "lab.py")).resolve().parents if (p / "labs_paths.py").is_file()]
from labs_paths import DATA, OUTPUT
# %% [markdown]
# # Lab 2.6-B · Melt, pivot, stack: the survey by age group (STARTER)
# survey.csv is wide in one way: five satisfaction questions, each in its own column.
# Question: which question does each age group score lowest, and how many answers are
# behind each average?
#
# Expected when you finish: a tidy table of 9,000 rows, a 6 x 5 grid of means, a 6 x 5
# grid of counts, the lowest-scored question for each age group, and a tidy CSV of 30 rows
# (one per age group and question) in your output folder.

# %% Load (done for you)
import pandas as pd

pd.set_option("display.width", 150)
pd.set_option("display.max_columns", 20)

survey = pd.read_csv(DATA / "survey.csv")
sat_cols = ["sat_overall", "sat_selection", "sat_price", "sat_staff", "sat_website"]
print(survey.shape)

# %% Step 1: wide to tidy
# TODO 1: answers = survey.melt(id_vars=[..., ...], value_vars=sat_cols, var_name="item", value_name="score")
#         Keep response_id and age_group as the id columns. How many rows should there be?
answers = None

# %% Step 2: tidy to a grid of means, and a grid of counts
# TODO 2: means = answers.pivot_table(index="age_group", columns="item", values="score", aggfunc="mean")
#         n = the same call with aggfunc="count"
#         (In a scratch cell, try answers.pivot(index="age_group", columns="item", values="score")
#          and read the error. What is it telling you about the tidy table?)
means = None
n = None

# %% Step 3: read across each row
# TODO 3: lowest = means.idxmin(axis=1)      (the column name of the smallest value in each row)
#         Which two cells stand out from their columns?
lowest = None

# %% Step 4: back to tidy, and save
# TODO 4: tidy_means = means.stack().rename("mean_score").reset_index()
#         Round mean_score to 2 decimals and write it to OUTPUT / "survey_by_age.csv" with index=False.
#         Read it back and print its shape.
tidy_means = None

# %% Report
if answers is None or means is None or n is None or lowest is None or tidy_means is None:
    print("TODOs not done yet: answers, means, n, lowest or tidy_means is still None.")
else:
    print(answers.shape, means.shape, tidy_means.shape)
