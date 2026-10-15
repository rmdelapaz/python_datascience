# --- lab bootstrap: find labs_paths.py (the same three lines open every lab; see labs/README.md) ---
import pathlib, sys
sys.path[:0] = [str(p) for p in pathlib.Path(globals().get("__file__", "lab.py")).resolve().parents if (p / "labs_paths.py").is_file()]
from labs_paths import DATA

# %% [markdown]
# # Lab 4.1 · Find the bugs: three summaries that are quietly wrong (DEBUG HANDOUT)
# Nothing here raises an error. Each of the three "findings" below is wrong or misleading.
# For each one: say what went wrong, and change the code so the printed sentence is true.
# There is no solution file: the lesson's Common Mistakes 1, 3 and 4 are the answer.

# %%
import numpy as np
import pandas as pd

orders = pd.read_csv(DATA / "orders.csv", parse_dates=["order_date"])
daily = pd.read_csv(DATA / "daily_sales.csv", parse_dates=["date"])

# %% Finding 1: "The average order, across our four payment methods, is $..."
by_method = orders.groupby("payment_method")["order_total"].mean()
print(by_method.round(2))
print("Finding 1: the average order is $", round(by_method.mean(), 2))
print("           (check it against orders['order_total'].mean())")

# %% Finding 2: "Average daily store revenue is $..."
revenue = daily["revenue"].to_numpy()
print("Finding 2: average daily store revenue is $", np.mean(revenue))

# %% Finding 3: "Two analysts, same seven days, same store. Their SDs must match."
week = daily.loc[daily["store"] == "Flagstaff", "visitors"].head(7)
analyst_a = np.std(week.to_numpy())
analyst_b = week.std()
print("Finding 3: analyst A says", round(analyst_a, 2), "and analyst B says", round(analyst_b, 2))
print("           Same data. Who divided by what? Which one would you report, and why?")
