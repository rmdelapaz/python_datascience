# --- lab bootstrap: find labs_paths.py (the same three lines open every lab; see labs/README.md) ---
import pathlib, sys
sys.path[:0] = [str(p) for p in pathlib.Path(globals().get("__file__", "lab.py")).resolve().parents if (p / "labs_paths.py").is_file()]
from labs_paths import DATA

# %% [markdown]
# # Lab 2.7-B · Is the online return rate getting worse? (SOLUTION)

# %% Load the online orders with real dates
import pandas as pd

orders = pd.read_csv(DATA / "orders.csv", parse_dates=["order_date"])
online = orders[orders["channel"] == "online"].copy()
online["returned"] = online["status"] == "returned"
print("online orders:", len(online), "| returned:", int(online["returned"].sum()))

# %% Step 1: monthly rate, with the counts behind it
monthly = online.resample("ME", on="order_date")["returned"].agg(["mean", "sum", "count"])
monthly["rate_pct"] = (monthly["mean"] * 100).round(2)
print(monthly[["rate_pct", "sum", "count"]])

# %% Step 2: highest and lowest month
hi, lo = monthly["rate_pct"].idxmax(), monthly["rate_pct"].idxmin()
print(f"highest: {hi:%Y-%m} at {monthly.loc[hi, 'rate_pct']}% ({monthly.loc[hi, 'sum']} of {monthly.loc[hi, 'count']} orders)")
print(f"lowest:  {lo:%Y-%m} at {monthly.loc[lo, 'rate_pct']}% ({monthly.loc[lo, 'sum']} of {monthly.loc[lo, 'count']} orders)")

# %% Step 3: a calmer view
quarterly = (online.resample("QE", on="order_date")["returned"].mean() * 100).round(2)
yearly = (online.resample("YE", on="order_date")["returned"].mean() * 100).round(2)
print("by quarter (%):")
print(quarterly.to_string())
print("by year (%):")
print(yearly.to_string())

# %% Step 4: year over year, in percentage points
yoy = monthly["rate_pct"].diff(12).round(2)
print("2025 minus the same month of 2024, in percentage points:")
print(yoy.loc["2025"].to_string())
print("months of 2025 with a higher rate than a year earlier:", int((yoy.loc["2025"] > 0).sum()), "of 12")

# %% Step 5: conclusion
worse = int((yoy.loc["2025"] > 0).sum())
print(f"Conclusion: no trend. Monthly rates bounce between about 5.7% and 9.1% because each month has only")
print(f"24 to 51 returns. 2025 was worse in {worse} months and better in {12 - worse}, and the yearly rate went DOWN slightly,")
print(f"from {yearly.iloc[0]}% to {yearly.iloc[1]}%. 'Returns feel worse' is not supported by the data.")
