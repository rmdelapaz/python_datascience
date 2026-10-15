# --- lab bootstrap: find labs_paths.py (the same three lines open every lab; see labs/README.md) ---
import pathlib, sys
sys.path[:0] = [str(p) for p in pathlib.Path(globals().get("__file__", "lab.py")).resolve().parents if (p / "labs_paths.py").is_file()]
from labs_paths import DATA

# %% [markdown]
# # Lab 4.5-B · Do orders with footwear come back more often? (SOLUTION)
# Lesson 3.3 drew the chart. Now test it: online orders that contain footwear against online
# orders that do not, then the same question for store orders. Two tests, so correct for both.

# %% Flag every order that contains a footwear line (SKU prefix FTW)
import numpy as np
import pandas as pd
from scipy import stats
from scipy.stats.contingency import association
from statsmodels.stats.multitest import multipletests

orders = pd.read_csv(DATA / "orders.csv", parse_dates=["order_date"])
items = pd.read_csv(DATA / "order_items.csv")
footwear_ids = items.loc[items["sku"].str.startswith("FTW"), "order_id"].unique()
orders["footwear"] = orders["order_id"].isin(footwear_ids)
orders["returned"] = orders["status"] == "returned"
print("orders with footwear:", orders["footwear"].sum(), "of", len(orders))

# H0 (per channel): containing footwear and being returned are unrelated.
# H1: they are related. alpha = 0.05, chi-square test, two tests -> Holm correction.

# %% Step 1: online orders. The table, the rates, the test
online = orders[orders["channel"] == "online"]
table = pd.crosstab(online["footwear"], online["returned"])
print(table)
rates = online.groupby("footwear")["returned"].mean()
print(f"returned: with footwear {rates[True]:.1%}, without {rates[False]:.1%}, "
      f"ratio {rates[True] / rates[False]:.1f}")
chi = stats.chi2_contingency(table)
print(f"chi-square = {chi.statistic:.1f}, df = {chi.dof}, p = {chi.pvalue:.1e}")
print("smallest expected count:", round(chi.expected_freq.min(), 1),
      "| Cramer's V:", round(association(table, method="cramer"), 3))

# %% Step 2: store orders, the same question
store = orders[orders["channel"] == "store"]
table_s = pd.crosstab(store["footwear"], store["returned"])
rates_s = store.groupby("footwear")["returned"].mean()
chi_s = stats.chi2_contingency(table_s)
print(f"store: with footwear {rates_s[True]:.1%}, without {rates_s[False]:.1%}")
print(f"       chi-square = {chi_s.statistic:.2f}, p = {chi_s.pvalue:.2f}")
print("smallest expected count:", round(chi_s.expected_freq.min(), 1))

# %% Step 3: two tests, so adjust
p_holm = multipletests([chi.pvalue, chi_s.pvalue], method="holm")[1]
print("Holm-adjusted p-values: online", f"{p_holm[0]:.1e}", "| store", round(p_holm[1], 2))

# %% Step 4: the report
print("Online orders that contain footwear were returned 14.4% of the time, against 4.8%")
print("for other online orders: three times as often (chi-square p far below 0.001 after")
print("Holm; V = 0.16). In stores the rates are 3.8% and 3.3% (p = 0.43): no difference")
print("was detected. That is not proof of none: the store gap could be small and real.")
