# --- lab bootstrap: find labs_paths.py (the same three lines open every lab; see labs/README.md) ---
import pathlib, sys
sys.path[:0] = [str(p) for p in pathlib.Path(globals().get("__file__", "lab.py")).resolve().parents if (p / "labs_paths.py").is_file()]
from labs_paths import DATA, OUTPUT

# %% [markdown]
# # Checkpoint 1 · Do December shoppers buy pricier things? (MODEL ANSWER)
# Instructor copy: the model answer for the 30-minute checkpoint in Session 13.
# Do not hand out before the checkpoint.
#
# ## 1. Plan (written before any code)
# Decision it informs: how Finance values the December stock for the stores.
# Data: daily_sales.csv, one row per store per day.
# Measure: price per unit = revenue / units, one value per store-day.
# Comparison: December days against all other days; then by store and by year, and the
#   month-by-month profile, to see whether "December against the rest" is a fair split.
# Method: means with a 95% confidence interval for the difference (Welch), Cohen's d.
# Checks first: grain, missing revenue, zero units.

# %% 2. Load and check
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy import stats

daily = pd.read_csv(DATA / "daily_sales.csv", parse_dates=["date"])
print("rows:", len(daily), "| one row per store-day:", not daily.duplicated(["date", "store"]).any())
print("missing revenue:", daily["revenue"].isna().sum(), "| days with zero units:", (daily["units"] == 0).sum())

daily["price_per_unit"] = daily["revenue"] / daily["units"]
use = daily.dropna(subset=["price_per_unit"]).copy()        # the 6 store-days with no revenue cannot be used
use["december"] = use["date"].dt.month == 12
print("store-days used:", len(use), "| December:", use["december"].sum(), "| other:", (~use["december"]).sum())
print(use["price_per_unit"].describe().round(2).to_string())

# %% 3. The comparison: estimate, interval, test, effect size
def cohens_d(x, y):
    """Difference in means divided by the pooled standard deviation (Lesson 4.5)."""
    nx, ny = len(x), len(y)
    pooled_var = ((nx - 1) * np.var(x, ddof=1) + (ny - 1) * np.var(y, ddof=1)) / (nx + ny - 2)
    return (np.mean(x) - np.mean(y)) / np.sqrt(pooled_var)


dec = use.loc[use["december"], "price_per_unit"]
rest = use.loc[~use["december"], "price_per_unit"]
res = stats.ttest_ind(dec, rest, equal_var=False)
ci = res.confidence_interval()
print()
print(f"December: mean ${dec.mean():.2f} (median ${dec.median():.2f}, n = {len(dec)})")
print(f"Other months: mean ${rest.mean():.2f} (median ${rest.median():.2f}, n = {len(rest)})")
print(f"Difference: ${dec.mean() - rest.mean():.2f} per unit ({dec.mean() / rest.mean() - 1:+.1%}), "
      f"95% CI ${ci.low:.2f} to ${ci.high:.2f}")
print(f"Welch t-test p = {res.pvalue:.1e}, Cohen's d = {cohens_d(dec, rest):.2f}")

# %% 4. Is it the same in every store and in both years?
print()
by_store = use.pivot_table(index="store", columns="december", values="price_per_unit", aggfunc="mean")
by_store["gap"] = by_store[True] - by_store[False]
print(by_store.round(2).to_string())
by_year = use.pivot_table(index=use["date"].dt.year, columns="december", values="price_per_unit", aggfunc="mean")
by_year["gap"] = by_year[True] - by_year[False]
print(by_year.round(2).to_string())

# %% 5. Is "December against the rest" the right split? Look at every month.
print()
monthly = use.groupby(use["date"].dt.month)["price_per_unit"].mean()
print(monthly.round(2).to_string())
mar_oct = use.loc[use["date"].dt.month.between(3, 10), "price_per_unit"]
print(f"March to October: mean ${mar_oct.mean():.2f}. December against those months: "
      f"${dec.mean() - mar_oct.mean():.2f} ({dec.mean() / mar_oct.mean() - 1:+.1%})")

# %% 6. One figure that states the finding
by_month_store = use.pivot_table(index=use["date"].dt.month, columns="store", values="price_per_unit", aggfunc="mean")
fig, ax = plt.subplots(figsize=(9, 4.5), layout="constrained")
for store in by_month_store.columns:
    ax.plot(by_month_store.index, by_month_store[store], marker="o", markersize=3, label=store)
ax.axhline(mar_oct.mean(), color="gray", linestyle="--", linewidth=1)
ax.text(6.5, mar_oct.mean() - 0.15, f"March to October average: ${mar_oct.mean():.2f}", ha="center", va="top", color="gray")
ax.set_xticks(range(1, 13), labels=["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"])
ax.set_ylabel("Mean revenue per unit sold ($)")
ax.set_title("Store shoppers pay about $4 more per unit in December, in every store")
ax.legend(title="Store", ncols=4, loc="upper center")
fig.savefig(OUTPUT / "checkpoint1_price_per_unit.png", dpi=150)
print("\nfigure saved:", "checkpoint1_price_per_unit.png")

# %% 7. The note
d = cohens_d(dec, rest)
above = (rest < dec.median()).mean()
print(f"""
FINDINGS
- Yes. In December a unit sold in the stores brings in ${dec.mean():.2f} on average against ${rest.mean():.2f} in the
  other eleven months: ${dec.mean() - rest.mean():.2f} more ({dec.mean() / rest.mean() - 1:+.1%}; 95% CI ${ci.low:.2f} to ${ci.high:.2f}; Welch p < 0.001;
  Cohen's d = {d:.2f}, a large effect: the middle December day is above {above:.0%} of the other days).
- It is the same story in all four stores (gaps of ${by_store['gap'].min():.2f} to ${by_store['gap'].max():.2f}) and in both years
  (${by_year['gap'].iloc[0]:.2f} and ${by_year['gap'].iloc[1]:.2f}).
- December is the peak of a winter season, not a one-month jump: November (${monthly[11]:.2f}), January
  (${monthly[1]:.2f}) and February (${monthly[2]:.2f}) are also above the March-to-October level of ${mar_oct.mean():.2f}.
  Against those months the December gap is ${dec.mean() - mar_oct.mean():.2f} ({dec.mean() / mar_oct.mean() - 1:+.1%}).
CAVEATS
- Revenue per unit rises if shoppers choose pricier items OR if prices are higher: this file cannot
  tell the two apart (it has no products). "Buy pricier things" is one reading, not a proven one.
- The unit is a store-day, and neighboring days are alike, so the p-value overstates the evidence.
  With an effect this large and this consistent, the conclusion does not depend on it.
- Only two Decembers ({len(dec)} store-days); {daily['revenue'].isna().sum()} store-days had no revenue and were left out.
NEXT QUESTION
- Is it the mix? Compare the categories sold in December with other months using order_items and products.
""")
