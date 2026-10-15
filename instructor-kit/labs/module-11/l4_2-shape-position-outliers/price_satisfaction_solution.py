# --- lab bootstrap: find labs_paths.py (the same three lines open every lab; see labs/README.md) ---
import pathlib, sys
sys.path[:0] = [str(p) for p in pathlib.Path(globals().get("__file__", "lab.py")).resolve().parents if (p / "labs_paths.py").is_file()]
from labs_paths import DATA, OUTPUT

# %% [markdown]
# # Lab 4.2-B · Who is unhappy about prices? (SOLUTION)
# Marketing reports "price satisfaction: 3.3 out of 5" and wants to know whether any age
# group feels differently. The answers are 1-to-5 survey answers: ordered categories, not
# measurements. Summarize them as what they are, by age group, with counts.

# %% Load the survey
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

survey = pd.read_csv(DATA / "survey.csv")
price = survey["sat_price"]
print("responses:", len(price), "| answered the price question:", price.count())

# %% Step 1: the whole distribution first
table = pd.DataFrame({
    "count": price.value_counts().sort_index(),
    "percent": (price.value_counts(normalize=True).sort_index() * 100).round(1),
})
print(table)
print("median:", price.median(), "| mean (a rough index only):", round(price.mean(), 2))

# %% Step 2: by age group, as ordered categories, with n
def top_two(values):
    return (values.dropna() >= 4).mean() * 100

def bottom_two(values):
    return (values.dropna() <= 2).mean() * 100

by_age = survey.groupby("age_group")["sat_price"].agg(
    n="count", rows="size", median="median", satisfied_pct=top_two, dissatisfied_pct=bottom_two)
print(by_age.round(1))

# %% Step 3: who did not answer?
skipped = survey.groupby("age_group")["sat_price"].agg(lambda col: col.isna().mean() * 100)
print("percent who skipped the question, by age group:")
print(skipped.round(1).to_string())

# %% Step 4: the picture. One stacked bar per age group, saved to OUTPUT
shares = pd.crosstab(survey["age_group"], survey["sat_price"], normalize="index") * 100
colors = matplotlib.colormaps["RdBu"](np.linspace(0.1, 0.9, 5))
labels = ["1 very dissatisfied", "2", "3 neutral", "4", "5 very satisfied"]

fig, ax = plt.subplots(figsize=(9, 4), layout="constrained")
left = np.zeros(len(shares))
for answer, color, label in zip(shares.columns, colors, labels):
    ax.barh(shares.index, shares[answer], left=left, color=color, edgecolor="white", label=label)
    left += shares[answer].to_numpy()
ax.invert_yaxis()
ax.set_xlim(0, 100)
ax.set_xlabel("Percent of customers who answered")
ax.set_title("Satisfaction with prices, by age group", loc="left", fontweight="bold")
fig.legend(loc="outside lower center", ncols=5, fontsize=8, frameon=False)
chart = OUTPUT / "price_satisfaction_by_age.png"
fig.savefig(chart, dpi=110, facecolor="white")
plt.close(fig)
print("saved:", chart.name, plt.imread(chart).shape[:2])

# %% Step 5: the finding, as one sentence with its n
young = by_age.loc["18-24"]
rest = survey.loc[survey["age_group"] != "18-24", "sat_price"]
print(f"Among the {young['n']:.0f} customers aged 18-24 who answered, {young['satisfied_pct']:.0f}% are")
print(f"satisfied with prices and {young['dissatisfied_pct']:.0f}% are dissatisfied; among the other")
print(f"{rest.count()} it is {top_two(rest):.0f}% and {bottom_two(rest):.0f}%.")
