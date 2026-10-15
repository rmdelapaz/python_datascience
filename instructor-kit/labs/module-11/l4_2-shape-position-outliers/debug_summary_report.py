# --- lab bootstrap: find labs_paths.py (the same three lines open every lab; see labs/README.md) ---
import pathlib, sys
sys.path[:0] = [str(p) for p in pathlib.Path(globals().get("__file__", "lab.py")).resolve().parents if (p / "labs_paths.py").is_file()]
from labs_paths import DATA, OUTPUT

# %% [markdown]
# # Lab 4.2 · Find the bugs: a summary report that is quietly wrong (DEBUG HANDOUT)
# Nothing here raises an error. Four results below are wrong or misleading. For each one:
# say what went wrong and change the code so the printed line is true.
# There is no solution file: the lesson's Common Mistakes 1, 2, 3 and 5 are the answer.

# %%
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

orders = pd.read_csv(DATA / "orders.csv", parse_dates=["order_date"])
daily = pd.read_csv(DATA / "daily_sales.csv", parse_dates=["date"])
survey = pd.read_csv(DATA / "survey.csv")
totals = orders["order_total"]

# %% Result 1: "90% of orders are below $..."
print("Result 1: 90% of orders are below $", round(np.percentile(totals, 0.90), 2))
print("          (compare with totals.quantile(0.90))")

# %% Result 2: a box plot of daily revenue for the report
fig, ax = plt.subplots(figsize=(7, 2.5), layout="constrained")
box = ax.boxplot(daily["revenue"], orientation="horizontal")
fig.savefig(OUTPUT / "daily_revenue_box.png", dpi=110)
plt.close(fig)
print("Result 2: the median line of the box is drawn at x =", box["medians"][0].get_xdata())

# %% Result 3: "the three numeric columns of the orders table, summarized"
print("Result 3:")
print(orders[["order_id", "customer_id", "order_total"]].describe().loc[["mean", "std"]].round(1))

# %% Result 4: "Online shoppers rate our staff about the same as store shoppers"
print("Result 4:")
print(survey.groupby("store")["sat_staff"].mean().round(2))
print("          (how many people is each of those means based on?)")
