# --- lab bootstrap: find labs_paths.py (the same three lines open every lab; see labs/README.md) ---
import pathlib, sys
sys.path[:0] = [str(p) for p in pathlib.Path(globals().get("__file__", "lab.py")).resolve().parents if (p / "labs_paths.py").is_file()]
from labs_paths import DATA

# %% [markdown]
# # Lab 4.3 · Find the bugs: four model answers that are quietly wrong (DEBUG HANDOUT)
# Nothing here raises an error, and every printed "answer" is wrong. For each one: say which
# argument means something different from what the author assumed, and fix it.
# There is no solution file: the lesson's Common Mistakes 1, 2 and 5, and its warning about
# sf() and "or more", are the answer.

# %%
import numpy as np
import pandas as pd
from scipy import stats

daily = pd.read_csv(DATA / "daily_sales.csv", parse_dates=["date"])
orders = pd.read_csv(DATA / "orders.csv", parse_dates=["order_date"])
spend = (daily["revenue"] / daily["visitors"]).dropna()
mu, sigma = spend.mean(), spend.std()

# %% Answer 1: "On 26% of days a store takes less than $15 per visitor"
model = stats.norm(mu, sigma ** 2)
print("Answer 1: P(spend below $15) =", round(model.cdf(15), 3),
      "| the data says", round((spend < 15).mean(), 3))

# %% Answer 2: "A delivery takes between 10 and 20 minutes, any time equally likely,
#               so the chance it takes more than 18 minutes is 60%"
delivery = stats.uniform(10, 20)
print("Answer 2: P(more than 18 minutes) =", round(delivery.sf(18), 3),
      "| this model's range is", delivery.ppf([0, 1]))

# %% Answer 3: "The chance of 5 or more returns in a batch of 40 orders is 2.4%"
p_return = (orders["status"] == "returned").mean()
batch = stats.binom(n=40, p=p_return)
print("Answer 3: P(5 or more returns) =", round(batch.sf(5), 3))

# %% Answer 4: "I simulated 1,000 batches and EVERY batch had the same number of returns"
counts = []
for _ in range(1_000):
    rng = np.random.default_rng(42)
    counts.append(rng.binomial(n=40, p=p_return))
print("Answer 4: distinct simulated counts:", sorted(set(counts)))
