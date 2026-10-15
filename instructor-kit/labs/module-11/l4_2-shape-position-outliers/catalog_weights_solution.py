# --- lab bootstrap: find labs_paths.py (the same three lines open every lab; see labs/README.md) ---
import pathlib, sys
sys.path[:0] = [str(p) for p in pathlib.Path(globals().get("__file__", "lab.py")).resolve().parents if (p / "labs_paths.py").is_file()]
from labs_paths import DATA

# %% [markdown]
# # Lab 4.2-A · "Take the outlier weights out of the catalog" (SOLUTION)
# The shipping team is setting a standard box size and wants a typical product weight.
# Their request: "remove the outlier weights first". Describe the shape of weight_kg, locate
# values in it, run both outlier rules, and find out what the flagged products are before
# anything is removed.

# %% Load the catalog
import numpy as np
import pandas as pd

products = pd.read_csv(DATA / "products.csv")
weight = products["weight_kg"]
print("rows:", len(weight), "| weights present:", weight.count(), "| missing:", weight.isna().sum())

# %% Step 1: shape
print("mean:", round(weight.mean(), 3), "| median:", weight.median())
print("skew:", round(weight.skew(), 2), "| skew of log(weight):", round(np.log(weight).skew(), 2))

# %% Step 2: position
print(weight.quantile([0.10, 0.25, 0.50, 0.75, 0.90, 0.95]).round(3).to_string())
have = weight.dropna()
print(f"share of weighed products at or below 2 kg: {(have <= 2).mean():.1%}")

# %% Step 3: two outlier rules
q1, q3 = weight.quantile(0.25), weight.quantile(0.75)
iqr = q3 - q1
lower, upper = q1 - 1.5 * iqr, q3 + 1.5 * iqr
flag_iqr = (weight < lower) | (weight > upper)
z = (weight - weight.mean()) / weight.std()
flag_z = z.abs() > 3
print("IQR fences:", round(lower, 3), "to", round(upper, 3), "kg")
print("flagged by the IQR rule:", flag_iqr.sum(), "| flagged by |z| > 3:", flag_z.sum())

# %% Step 4: a flag is a question. What ARE these products?
print(products[flag_iqr].groupby("category").size().sort_values(ascending=False).to_string())
print()
print(products.loc[flag_z, ["name", "category", "weight_kg"]].sort_values("weight_kg").to_string(index=False))

# %% Step 5: the grouped summary the shipping team actually needs (always with n)
by_category = products.groupby("category")["weight_kg"].agg(n="count", rows="size", median="median")
by_category["q3"] = products.groupby("category")["weight_kg"].quantile(0.75)
print(by_category.sort_values("median").round(2))

# %% Step 6: the answer to send back
print(f"Typical product weight: {weight.median():.2f} kg (median of {weight.count()} weighed products;")
print(f"{weight.isna().sum()} have no weight recorded). Middle half: {q1:.2f} to {q3:.2f} kg.")
print(f"Nothing removed: the {flag_iqr.sum()} flagged products are real (mostly tents). They need")
print("their own box size, not deletion.")
