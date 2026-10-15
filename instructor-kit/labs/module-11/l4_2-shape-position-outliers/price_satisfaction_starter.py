# --- lab bootstrap: find labs_paths.py (the same three lines open every lab; see labs/README.md) ---
import pathlib, sys
sys.path[:0] = [str(p) for p in pathlib.Path(globals().get("__file__", "lab.py")).resolve().parents if (p / "labs_paths.py").is_file()]
from labs_paths import DATA, OUTPUT

# %% [markdown]
# # Lab 4.2-B · Who is unhappy about prices? (STARTER)
# Marketing reports "price satisfaction: 3.3 out of 5" and wants to know whether any age
# group feels differently. The answers are 1-to-5 survey answers: ordered categories, not
# measurements. Summarize them as what they are, by age group, with counts.
#
# Expected when you finish: a five-row table of counts and percentages; a table with one row
# per age group (n, rows, median, satisfied_pct, dissatisfied_pct) in which one group clearly
# stands out; the share who skipped the question in each group; a stacked bar chart saved as
# price_satisfaction_by_age.png in OUTPUT; and one sentence that includes an n.
# No plt.show(): open the saved file to look at the chart.

# %% Load the survey (done for you)
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

survey = pd.read_csv(DATA / "survey.csv")
price = survey["sat_price"]
print("responses:", len(price), "| answered the price question:", price.count())

# %% Step 1: the whole distribution first
# TODO 1: build a table with a "count" column (value_counts().sort_index()) and a "percent"
#         column (value_counts(normalize=True) * 100, rounded to 1). Print it, then the median.

# %% Step 2: by age group, as ordered categories, with n
def top_two(values):
    """Percent of the answers that are 4 or 5 (satisfied)."""
    return (values.dropna() >= 4).mean() * 100

def bottom_two(values):
    """Percent of the answers that are 1 or 2 (dissatisfied)."""
    # TODO 2: write this one yourself, modeled on top_two.
    return np.nan

# TODO 3: group by "age_group" and aggregate "sat_price" with named aggregation:
#         n="count", rows="size", median="median", satisfied_pct=top_two, dissatisfied_pct=bottom_two
by_age = None
print(by_age if by_age is not None else "TODO 3 not done yet: `by_age` is still None.")

# %% Step 3: who did not answer?
# TODO 4: for each age group, the percent of rows where sat_price is missing.
#         Is any group far more likely to have skipped the question?

# %% Step 4: the picture. One stacked bar per age group, saved to OUTPUT (done for you)
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
# TODO 5: give the chart a title, then save it as OUTPUT / "price_satisfaction_by_age.png"
#         (dpi=110, facecolor="white") and close the figure.
fig.legend(loc="outside lower center", ncols=5, fontsize=8, frameon=False)
plt.close(fig)

# %% Step 5: the finding, as one sentence with its n
# TODO 6: print one sentence, built from by_age, that names the group that stands out and
#         gives its n, its satisfied share and its dissatisfied share.
