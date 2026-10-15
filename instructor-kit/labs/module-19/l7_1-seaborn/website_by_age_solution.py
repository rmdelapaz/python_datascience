# --- lab bootstrap: find labs_paths.py (the same three lines open every lab; see labs/README.md) ---
import pathlib, sys
sys.path[:0] = [str(p) for p in pathlib.Path(globals().get("__file__", "lab.py")).resolve().parents if (p / "labs_paths.py").is_file()]
from labs_paths import DATA, OUTPUT

# %% [markdown]
# # Lab 7.1-B · Who struggles with the website? (SOLUTION)
# Question: does website satisfaction differ by age group, and how sure are we?
# Practices: order=, errorbar=, seed=, a figure-level catplot with col=, and saying what the bars are.

# %% Load (done for you in the starter)
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

sns.set_theme(style="whitegrid", palette="colorblind")
ages = ["18-24", "25-34", "35-44", "45-54", "55-64", "65+"]

survey = pd.read_csv(DATA / "survey.csv")
survey["shopper"] = np.where(survey["store"] == "Online", "online", "store")
print("responses:", len(survey), "| website rating missing:", int(survey["sat_website"].isna().sum()))

# %% Step 1: the same means with two different error bars (axes-level, one figure)
fig, axes = plt.subplots(1, 2, figsize=(10, 3.8), sharey=True, layout="constrained")
for ax, choice, meaning in [(axes[0], ("ci", 95), "95% CI of the mean (uncertainty)"),
                            (axes[1], "sd", "mean +/- 1 standard deviation (spread)")]:
    sns.pointplot(data=survey, x="age_group", y="sat_website", order=ages,
                  errorbar=choice, seed=42, linestyle="none", capsize=0.2, ax=ax)
    ax.set_title(f"Bars: {meaning}", loc="left", fontsize=10)
    ax.set(xlabel="age group", ylabel="website satisfaction (1 to 5)")
fig.suptitle("Customers aged 65+ rate the website about 0.6 points lower")
target = OUTPUT / "website_by_age.png"
fig.savefig(target, dpi=150)
plt.close(fig)
print("saved:", target.name)

# %% Step 2: check the bars by hand
summary = survey.groupby("age_group")["sat_website"].agg(n="count", mean="mean", sd="std", se="sem").loc[ages]
summary["ci_low"] = summary["mean"] - 1.96 * summary["se"]
summary["ci_high"] = summary["mean"] + 1.96 * summary["se"]
print(summary.round(2).to_string())
others = survey.loc[survey["age_group"] != "65+", "sat_website"].mean()
print(f"65+ mean {summary.loc['65+', 'mean']:.2f} vs everyone else {others:.2f}: "
      f"gap {others - summary.loc['65+', 'mean']:.2f} points")

# %% Step 3: does the gap hold for online shoppers and store shoppers? (figure-level, col=)
g = sns.catplot(data=survey, x="age_group", y="sat_website", col="shopper", col_order=["online", "store"],
                order=ages, kind="point", errorbar=("ci", 95), seed=42, linestyle="none", capsize=0.2,
                height=3.2, aspect=1.4)
g.set_titles("{col_name} shoppers")
g.set_axis_labels("age group", "website satisfaction (mean, 95% CI)")
target2 = OUTPUT / "website_by_age_shopper.png"
g.savefig(target2, dpi=150)
plt.close(g.figure)
print("returned:", type(g).__name__, "| axes shape:", g.axes.shape, "| saved:", target2.name)
print(survey.pivot_table(index="age_group", columns="shopper", values="sat_website", aggfunc="mean").loc[ages].round(2).to_string())

# %% Step 4: the caveat that belongs in the caption
missing = survey.assign(missing=survey["sat_website"].isna()).groupby("shopper")["missing"].mean()
print("share of responses with no website rating:", {k: f"{v:.0%}" for k, v in missing.items()})
