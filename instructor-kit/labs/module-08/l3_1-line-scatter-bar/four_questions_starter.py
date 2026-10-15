# --- lab bootstrap: find labs_paths.py (the same three lines open every lab; see labs/README.md) ---
import pathlib, sys
sys.path[:0] = [str(p) for p in pathlib.Path(globals().get("__file__", "lab.py")).resolve().parents if (p / "labs_paths.py").is_file()]
from labs_paths import DATA, OUTPUT

# %% [markdown]
# # Lab 3.1-A · Four questions, four charts (STARTER)
# Each step starts with a question. Decide the chart type from the question BEFORE you read the TODO.
# Every chart: fig, ax = plt.subplots(figsize=..., layout="constrained"), methods on ax, a title,
# labeled axes, then fig.savefig(OUTPUT / "name.png"). Do not call plt.show() in a lab file.
#
# Expected when you finish: four PNG files in the output folder and four printed check lines:
#   - a line with 7 points (one per year)
#   - 5 horizontal bars, the longest on top
#   - a scatter of the products that have a weight (14 have none)
#   - a histogram with 30 bins and a dashed line at the median price

# %% Load (done for you)
import matplotlib.pyplot as plt
import pandas as pd

customers = pd.read_csv(DATA / "customers.csv", parse_dates=["signup_date"])
products = pd.read_csv(DATA / "products.csv")
print("customers:", customers.shape, "| products:", products.shape)
print("charts will be saved in:", OUTPUT)

# %% Question 1: how did the number of new accounts change from year to year?
per_year = customers.groupby(customers["signup_date"].dt.year)["customer_id"].count()   # one number per year
print(per_year.to_string())
# TODO 1: which chart shows change over time? Draw per_year (x = per_year.index, y = per_year.values)
#         with marker="o", a title and a y label. Save it as "q1_signups.png".
#         Then print len(ax.lines) and the number of points in the line.

# %% Question 2: which acquisition channel brought in the most customers?
per_channel = customers["acquisition_channel"].value_counts().sort_values()               # smallest first
# TODO 2: which chart compares groups? Use horizontal bars (ax.barh) so the names read easily,
#         write each value on its bar with ax.bar_label(bars, padding=3), label the x axis.
#         Save it as "q2_channels.png". Print how many bars were drawn.

# %% Question 3: do heavier products cost more?
print("products with no weight:", int(products["weight_kg"].isna().sum()))
# TODO 3: which chart shows whether two numbers move together? One dot per product:
#         x = weight_kg, y = price, with s=18 and alpha=0.5. Title, both axis labels (with units).
#         Save it as "q3_weight_price.png". Print the correlation: products["weight_kg"].corr(products["price"]).

# %% Question 4: what does a typical product cost, and how spread out are the prices?
# TODO 4: which chart shows a distribution? Draw products["price"] with bins=30 and edgecolor="white",
#         add ax.axvline at the median (linestyle="--", color="black", with a label) and ax.legend().
#         Save it as "q4_prices.png". Print the median and how many products cost more than $300.

# %% Last cell (done for you): close the figures and list what was saved
plt.close("all")
saved = sorted(p.name for p in OUTPUT.glob("q*.png"))
print("saved:", saved if saved else "nothing yet: the TODOs are still open")
