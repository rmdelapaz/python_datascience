# --- lab bootstrap: find labs_paths.py (the same three lines open every lab; see labs/README.md) ---
import pathlib, sys
sys.path[:0] = [str(p) for p in pathlib.Path(globals().get("__file__", "lab.py")).resolve().parents if (p / "labs_paths.py").is_file()]
from labs_paths import DATA, OUTPUT

# %% [markdown]
# # Lab 7.1-B · Who struggles with the website? (STARTER)
# Question: does website satisfaction differ by age group, and how sure are we?
# Practices: order=, errorbar=, seed=, a figure-level catplot with col=, and saying what the bars are.
#
# Expected when you finish: "saved: website_by_age.png", a six-row table (n, mean, sd, se, ci_low,
# ci_high), one line comparing the 65+ group with everyone else, a line that says what catplot
# returned and its axes shape, a small online/store table, and the share of missing ratings by shopper type.

# %% Load (done for you)
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

sns.set_theme(style="whitegrid", palette="colorblind")
ages = ["18-24", "25-34", "35-44", "45-54", "55-64", "65+"]

survey = pd.read_csv(DATA / "survey.csv")
survey["shopper"] = np.where(survey["store"] == "Online", "online", "store")
print("responses:", len(survey), "| website rating missing:", int(survey["sat_website"].isna().sum()))

# %% Step 1: the same means with two different error bars
fig, axes = plt.subplots(1, 2, figsize=(10, 3.8), sharey=True, layout="constrained")
# TODO 1: on axes[0] draw sns.pointplot of sat_website by age_group with order=ages,
#         errorbar=("ci", 95), seed=42, linestyle="none", capsize=0.2.
# TODO 2: on axes[1] draw the same chart with errorbar="sd".
# TODO 3: give each panel a title that says what its bars are, then save the figure:
#         fig.savefig(OUTPUT / "website_by_age.png", dpi=150) and print "saved: website_by_age.png"
plt.close(fig)

# %% Step 2: check the bars by hand
# TODO 4: summary = survey.groupby("age_group")["sat_website"].agg(n="count", mean="mean", sd="std", se="sem")
#         add ci_low and ci_high (mean -/+ 1.96 * se), put the rows in the order of `ages`, print rounded to 2.
#         Which panel's bars match ci_low..ci_high? Which match mean +/- sd?
summary = None

# %% Step 3: does the gap hold for online shoppers and store shoppers?
# TODO 5: g = sns.catplot(..., col="shopper", kind="point", order=ages, errorbar=("ci", 95), seed=42,
#         height=3.2, aspect=1.4). Use g.set_titles("{col_name} shoppers") and g.set_axis_labels(...).
#         Print type(g).__name__ and g.axes.shape, then g.savefig(OUTPUT / "website_by_age_shopper.png").

# %% Step 4: the caveat that belongs in the caption
# TODO 6: what share of online shoppers, and of store shoppers, gave no website rating at all?

if summary is None:
    print("TODO 1-6 not done yet: `summary` is still None and no chart has been saved.")
