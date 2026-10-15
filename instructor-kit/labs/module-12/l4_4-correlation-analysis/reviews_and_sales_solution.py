# --- lab bootstrap: find labs_paths.py (the same three lines open every lab; see labs/README.md) ---
import pathlib, sys
sys.path[:0] = [str(p) for p in pathlib.Path(globals().get("__file__", "lab.py")).resolve().parents if (p / "labs_paths.py").is_file()]
from labs_paths import DATA, OUTPUT

# %% [markdown]
# # Lab 4.4-A · Do reviews sell products? (SOLUTION)
# The marketing team wants to push customers to write more reviews, "because products with
# more reviews sell more". Look first, measure two ways, build a correlation matrix and a
# heatmap, then ask which way the arrow could run and what else could drive both.

# %% Build one row per product that has sold
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
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 4), layout="constrained")
ax1.scatter(catalog["review_count"], catalog["units_sold"], s=12, alpha=0.5, color="#667eea")
ax1.set_xlabel("Reviews")
ax1.set_ylabel("Units sold")
ax1.set_title("Reviews and units sold", loc="left")
ax2.scatter(catalog["rating"], catalog["units_sold"], s=12, alpha=0.5, color="#667eea")
ax2.set_xlabel("Star rating")
ax2.set_title("Rating and units sold", loc="left")
fig.savefig(OUTPUT / "reviews_scatter.png", dpi=110, facecolor="white")
plt.close(fig)

# %% Step 2: measure, two ways
for column in ["review_count", "rating", "price"]:
    pearson = catalog[column].corr(catalog["units_sold"])
    spearman = catalog[column].corr(catalog["units_sold"], method="spearman")
    print(f"{column:<12} vs units sold: Pearson {pearson:6.3f}   Spearman {spearman:6.3f}")

# %% Step 3: the whole matrix, and a heatmap with the scale fixed at -1 to 1
columns = ["price", "rating", "review_count", "units_sold"]
corr = catalog[columns].corr(method="spearman")
print(corr.round(2))
fig, ax = plt.subplots(figsize=(6, 5), layout="constrained")
image = ax.imshow(corr, cmap="RdBu_r", vmin=-1, vmax=1)
for i in range(len(columns)):
    for j in range(len(columns)):
        ax.text(j, i, f"{corr.iloc[i, j]:.2f}", ha="center", va="center")
ax.set_xticks(range(len(columns)), columns, rotation=30)
ax.set_yticks(range(len(columns)), columns)
fig.colorbar(image)
fig.savefig(OUTPUT / "catalog_heatmap.png", dpi=110, facecolor="white")
plt.close(fig)

# %% Step 4: what else could drive both? Price. Hold it constant (partial correlation)
def residuals(target, predictor):
    fit = stats.linregress(predictor, target)
    return target - (fit.intercept + fit.slope * predictor)

partial = residuals(catalog["review_count"], catalog["price"]).corr(
    residuals(catalog["units_sold"], catalog["price"]))
print("reviews and units sold, controlling for price:", round(partial, 3))

# %% Step 5: the answer for marketing
print("Products with more reviews have sold more units (r about 0.46), and the link")
print(f"survives holding price constant ({partial:.2f}). But the arrow can run backward:")
print("every sale is a chance for a review. These data cannot say that more reviews")
print("would cause more sales; a test (reviews requested for some products, not others)")
print("could. Star ratings show no link with units sold (Spearman about 0.01).")
