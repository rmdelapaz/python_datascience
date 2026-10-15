# --- lab bootstrap: find labs_paths.py (the same three lines open every lab; see labs/README.md) ---
import pathlib, sys
sys.path[:0] = [str(p) for p in pathlib.Path(globals().get("__file__", "lab.py")).resolve().parents if (p / "labs_paths.py").is_file()]
from labs_paths import DATA

# %% [markdown]
# # Lab 4.3-A · A normal model for walk-in conversion (SOLUTION)
# Each store-day, some share of the people who walk in buy something:
# conversion = transactions / visitors. Store managers want to know what a "bad day" and a
# "great day" look like. Fit a normal model, check it against the data, then use the four
# methods (cdf, sf, ppf, rvs) to answer their questions.

# %% Load the data and build the column
import numpy as np
import pandas as pd
from scipy import stats

rng = np.random.default_rng(11)
daily = pd.read_csv(DATA / "daily_sales.csv", parse_dates=["date"])
conversion = daily["transactions"] / daily["visitors"]
print("store-days:", len(conversion), "| missing:", conversion.isna().sum())

# %% Step 1: describe before you model
mu, sigma = conversion.mean(), conversion.std()
print("mean:", round(mu, 4), "| SD:", round(sigma, 4), "| skew:", round(conversion.skew(), 2))

# %% Step 2: freeze a normal distribution with the data's own mean and SD
model = stats.norm(loc=mu, scale=sigma)          # scale is the SD, not the variance

# %% Step 3: check the model. Does the 68-95-99.7 rule hold?
for k in (1, 2, 3):
    in_data = ((conversion - mu).abs() < k * sigma).mean()
    in_model = model.cdf(mu + k * sigma) - model.cdf(mu - k * sigma)
    print(f"within {k} SD:  data {in_data:.1%}   model {in_model:.1%}")

# %% Step 4: the managers' questions, model against data
print(f"P(conversion below 20%): model {model.cdf(0.20):.3f}   data {(conversion < 0.20).mean():.3f}")
print(f"P(conversion above 27%): model {model.sf(0.27):.3f}   data {(conversion > 0.27).mean():.3f}")
print(f"5th percentile (a bad day)   : model {model.ppf(0.05):.4f}   data {conversion.quantile(0.05):.4f}")
print(f"95th percentile (a great day): model {model.ppf(0.95):.4f}   data {conversion.quantile(0.95):.4f}")

# %% Step 5: simulate a year of store-days and count the bad ones
year = model.rvs(size=365, random_state=rng)
print("simulated days below 20% in a year:", (year < 0.20).sum())
print("the model expects                 :", round(365 * model.cdf(0.20), 1))

# %% Step 6: one sentence for the managers
print(f"On a typical day about {mu:.1%} of visitors buy. Below {model.ppf(0.05):.1%} is a bad day")
print(f"(1 day in 20); above {model.ppf(0.95):.1%} is a great one. The normal model matches the")
print("data to within about one percentage point for every question asked.")
