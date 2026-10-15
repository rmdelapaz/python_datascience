# --- lab bootstrap: find labs_paths.py (the same three lines open every lab; see labs/README.md) ---
import pathlib, sys
sys.path[:0] = [str(p) for p in pathlib.Path(globals().get("__file__", "lab.py")).resolve().parents if (p / "labs_paths.py").is_file()]
from labs_paths import DATA, OUTPUT

# %% [markdown]
# # Lab 4.4-A · Do reviews sell products? (STARTER)
# The marketing team wants to push customers to write more reviews, "because products with
# more reviews sell more". Look first, measure two ways, build a correlation matrix and a
# heatmap, then ask which way the arrow could run and what else could drive both.
#
# Expected when you finish: two scatter plots and a heatmap saved in OUTPUT (no plt.show());
# three lines of Pearson and Spearman against units sold (reviews about 0.45, rating near 0,
# price negative); a 4 x 4 Spearman matrix; a partial correlation; and an answer for
# marketing that does not claim more than the data shows.

# %% Build one row per product that has sold (done for you)
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy import stats

products = pd.read_csv(DATA / "products.csv")
items = pd.read_csv(DATA / "order_items.csv")
units_sold = items.groupby("sku")["quantity"].sum().rename("units_sold")
catalog = products.merge(units_sold, on="sku")
print("products that have sold:", len(catalog))

# %% Step 1: look first. Two scatter plots, saved to OUTPUT
# TODO 1: one figure, two panels: review_count against units_sold, and rating against
#         units_sold. Label the axes, save it as OUTPUT / "reviews_scatter.png", close it.
#         Before measuring anything, write one sentence about each panel here: ______

# %% Step 2: measure, two ways
# TODO 2: for "review_count", "rating" and "price", print the Pearson and the Spearman
#         correlation with units_sold.  (.corr(other) and .corr(other, method="spearman"))

# %% Step 3: the whole matrix, and a heatmap with the scale fixed at -1 to 1
columns = ["price", "rating", "review_count", "units_sold"]
# TODO 3: corr = catalog[columns].corr(method="spearman"); print it rounded to 2.
#         Then draw it with ax.imshow(corr, cmap="RdBu_r", vmin=-1, vmax=1), write each value
#         in its cell with ax.text, and save it as OUTPUT / "catalog_heatmap.png".

# %% Step 4: what else could drive both? Price. Hold it constant (partial correlation)
def residuals(target, predictor):
    """What is left of target after removing its straight-line relationship with predictor."""
    fit = stats.linregress(predictor, target)
    return target - (fit.intercept + fit.slope * predictor)

# TODO 4: correlate residuals(review_count, price) with residuals(units_sold, price).
partial = None

# %% Step 5: the answer for marketing
# TODO 5: print three or four sentences: how strong the link is, whether it survives holding
#         price constant, which way the arrow could run, and what would settle the question.
if partial is None:
    print("TODO 1-5 not done yet: `partial` is still None.")
