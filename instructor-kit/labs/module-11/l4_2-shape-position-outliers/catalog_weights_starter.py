# --- lab bootstrap: find labs_paths.py (the same three lines open every lab; see labs/README.md) ---
import pathlib, sys
sys.path[:0] = [str(p) for p in pathlib.Path(globals().get("__file__", "lab.py")).resolve().parents if (p / "labs_paths.py").is_file()]
from labs_paths import DATA

# %% [markdown]
# # Lab 4.2-A · "Take the outlier weights out of the catalog" (STARTER)
# The shipping team is setting a standard box size and wants a typical product weight.
# Their request: "remove the outlier weights first". Describe the shape of weight_kg, locate
# values in it, run both outlier rules, and find out what the flagged products are before
# anything is removed.
#
# Expected when you finish: a strongly positive skew; six percentiles; two rules that flag
# very different numbers of products (one flags more than six times as many as the other);
# a list showing which category most flagged products belong to; and a short answer to the
# shipping team that says what you did NOT remove, and why.

# %% Load the catalog (done for you)
import numpy as np
import pandas as pd

products = pd.read_csv(DATA / "products.csv")
weight = products["weight_kg"]
print("rows:", len(weight), "| weights present:", weight.count(), "| missing:", weight.isna().sum())

# %% Step 1: shape
# Write your guess first: is the mean above or below the median? ________
# TODO 1: print the mean, the median and weight.skew(). Then print the skew of np.log(weight).

# %% Step 2: position
# TODO 2: print the 10th, 25th, 50th, 75th, 90th and 95th percentiles with weight.quantile([...]).
#         Then: what share of the products that HAVE a weight are at or below 2 kg?
#         (The mean of a boolean is a proportion. Decide what to do about the missing values.)

# %% Step 3: two outlier rules
# TODO 3: build the IQR fences (q1 - 1.5 * iqr, q3 + 1.5 * iqr) and a boolean Series flag_iqr.
#         Build z-scores and a boolean Series flag_z for |z| > 3. Print both fences and both counts.
flag_iqr = pd.Series(False, index=products.index)     # placeholder: nothing flagged yet
flag_z = pd.Series(False, index=products.index)       # placeholder: nothing flagged yet
print("flagged by the IQR rule:", flag_iqr.sum(), "| flagged by |z| > 3:", flag_z.sum())

# %% Step 4: a flag is a question. What ARE these products?
# TODO 4: count the IQR-flagged products by category, and print the name, category and weight
#         of the products flagged by the z-score rule. Are they errors?

# %% Step 5: the grouped summary the shipping team actually needs (always with n)
# TODO 5: group by category and aggregate weight_kg with n="count", rows="size", median="median".
#         Which categories have missing weights? Which is the heaviest category by median?

# %% Step 6: the answer to send back
# TODO 6: print two or three sentences built from your variables: the typical weight (which
#         center?), how many products it is based on, and what you decided about the flags.
if flag_iqr.sum() == 0:
    print("TODO 3-6 not done yet. Expected: two different flag counts, then your answer.")
