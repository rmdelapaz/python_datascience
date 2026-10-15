# --- lab bootstrap: find labs_paths.py (the same three lines open every lab; see labs/README.md) ---
import pathlib, sys
sys.path[:0] = [str(p) for p in pathlib.Path(globals().get("__file__", "lab.py")).resolve().parents if (p / "labs_paths.py").is_file()]
from labs_paths import DATA

# %% [markdown]
# # Lab 1.5-B · What is one purchase worth at Flagstaff? (SOLUTION)
# The lesson fitted revenue against VISITORS. Here you fit it against TRANSACTIONS
# (purchases rung up), for Flagstaff. The slope should then be "dollars per purchase",
# and you already know another route to that number: revenue / transactions.
#
# Expected when you finish: 724 complete days; a two-number fit you can read as a sentence;
# its typical miss (RMSE) and R squared; the same slope reached a second way; a three-column
# model with a sale-day column and its RMSE; and forecasts for three scenarios, each quoted
# with a "give or take".

# %% Load Flagstaff's complete days (done for you)
import numpy as np


def load(col, dtype=float):
    """Read one column of daily_sales.csv into an array (the helper from Lesson 1.2)."""
    return np.genfromtxt(DATA / "daily_sales.csv", delimiter=",", skip_header=1, usecols=col, dtype=dtype)

stores = load(1, dtype=str)
transactions, revenue, promo = load(3), load(5), load(7)

keep = (stores == "Flagstaff") & ~np.isnan(revenue)     # one mask, applied to every column
x = transactions[keep]
y = revenue[keep]
is_promo = promo[keep]
print(y.size, "days | mean transactions", x.mean().round(1), "| mean revenue", y.mean().round(2))


def score(A, coef, y):
    """Typical miss (RMSE) and R squared of a fitted model, as in the lesson project."""
    residuals = y - A @ coef
    rmse = np.linalg.norm(residuals) / np.sqrt(y.size)
    r_squared = 1 - (residuals ** 2).sum() / ((y - y.mean()) ** 2).sum()
    return rmse, r_squared


# %% Step 1: build the matrix: a column of ones (for the intercept) and a column of transactions
A1 = np.column_stack([np.ones(x.size), x])
print("A1 shape:", A1.shape)

# %% Step 2: fit
coef1, *_ = np.linalg.lstsq(A1, y)
print(f"revenue = {coef1[0]:.2f} + {coef1[1]:.2f} * transactions")

# %% Step 3: score it
rmse1, r2_1 = score(A1, coef1, y)
print(f"transactions only: RMSE ${rmse1:,.2f}, R squared {r2_1:.3f}")

# %% Step 4: a second route to the slope
print("average dollars per purchase (revenue / transactions):", np.mean(y / x).round(2))
# Two routes, nearly the same number: each additional purchase goes with about that much revenue.

# %% Step 5: more information is more columns
A2 = np.column_stack([np.ones(x.size), x, is_promo])
coef2, *_ = np.linalg.lstsq(A2, y)
for name, value in zip(["intercept", "per purchase", "sale day"], coef2):
    print(f"{name:<13}{value:>10.2f}")
rmse2, r2_2 = score(A2, coef2, y)
print(f"with sale days   : RMSE ${rmse2:,.2f}, R squared {r2_2:.3f}")

# %% Step 6: predict three days with one @
scenarios = np.array([[1,  60, 0],       # a quiet day, 60 purchases
                      [1, 100, 0],       # a busy ordinary day
                      [1, 150, 1]])      # a sale day
forecast = scenarios @ coef2
for label, value in zip(["quiet day", "busy ordinary day", "sale day"], forecast):
    print(f"{label:<18} ${value:>10,.2f}   (give or take about ${rmse2:,.0f})")
