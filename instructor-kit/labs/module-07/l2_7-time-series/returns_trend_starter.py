# --- lab bootstrap: find labs_paths.py (the same three lines open every lab; see labs/README.md) ---
import pathlib, sys
sys.path[:0] = [str(p) for p in pathlib.Path(globals().get("__file__", "lab.py")).resolve().parents if (p / "labs_paths.py").is_file()]
from labs_paths import DATA

# %% [markdown]
# # Lab 2.7-B · Is the online return rate getting worse? (STARTER)
# The support team says "returns feel worse this year". Check it with the calendar.
# Questions: What share of online orders is returned each month? Each quarter? Each year?
#            Compared with the same month a year earlier, how many months of 2025 were worse?
#
# Expected when you finish:
#   - a 24-row monthly table: return rate in percent, returned orders, all orders
#   - the highest and the lowest month
#   - 8 quarterly rates and 2 yearly rates
#   - 12 year-over-year changes in percentage points, and a count of the months that got worse
#   - one sentence: is there a trend?

# %% Load the online orders with real dates (done for you)
import pandas as pd

orders = pd.read_csv(DATA / "orders.csv", parse_dates=["order_date"])
online = orders[orders["channel"] == "online"].copy()
online["returned"] = online["status"] == "returned"      # True/False: its mean is the return rate
print("online orders:", len(online), "| returned:", int(online["returned"].sum()))

# %% Step 1: monthly rate, with the counts behind it
# TODO 1: resample `online` by month END on the order_date column (on="order_date"), take the
#         "returned" column and aggregate with ["mean", "sum", "count"]. Store it in `monthly`.
#         Then add a column "rate_pct" = mean * 100, rounded to 2 decimals.
monthly = None

if monthly is None:
    print("TODO 1 not done yet: `monthly` is still None.")
else:
    print(monthly[["rate_pct", "sum", "count"]])

# %% Step 2: highest and lowest month
# TODO 2: use .idxmax() and .idxmin() on monthly["rate_pct"] and print both months with their rates.

# %% Step 3: a calmer view
# TODO 3: the same rate by quarter ("QE") and by year ("YE"). Print both, in percent.

# %% Step 4: year over year, in percentage points
# TODO 4: yoy = monthly["rate_pct"].diff(12)   (12 rows back = the same month last year)
#         Print the 2025 rows and count how many are greater than 0.

# %% Step 5: your conclusion
# TODO 5: replace the text with one honest sentence.
print("My conclusion: (write it here)")
