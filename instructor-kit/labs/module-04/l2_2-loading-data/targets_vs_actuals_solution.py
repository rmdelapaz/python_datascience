# --- lab bootstrap: find labs_paths.py (the same three lines open every lab; see labs/README.md) ---
import pathlib, sys
sys.path[:0] = [str(p) for p in pathlib.Path(globals().get("__file__", "lab.py")).resolve().parents if (p / "labs_paths.py").is_file()]
from labs_paths import DATA, OUTPUT
# %% [markdown]
# # Lab 2.2-C · Did the stores hit their targets? (SOLUTION)
# Question: which of the four stores beat its 2025 revenue target, and by how much?

# %% Find the sheets
import pandas as pd

BOOK = DATA / "sales_2025.xlsx"
print(pd.ExcelFile(BOOK).sheet_names)
print(pd.read_excel(BOOK, header=None, nrows=5).iloc[:, :3])     # the top of the first sheet, as it is

# %% Step 1: load each sheet with its own options
monthly = pd.read_excel(BOOK, sheet_name="Monthly Sales", header=3)   # the header is the row at position 3
targets = pd.read_excel(BOOK, sheet_name="Targets")
print(monthly.shape, targets.shape)
print(monthly.columns.tolist())

# %% Step 2: one row per store
rows = []
for store in ["Boise", "Bend", "Flagstaff", "Asheville"]:
    actual = monthly[store].sum()
    target = targets.loc[targets["store"] == store, "target_revenue"].sum()
    rows.append({"store": store, "actual": actual, "target": target})

result = pd.DataFrame(rows)
result["pct_of_target"] = (result["actual"] / result["target"] * 100).round(1)
result = result.sort_values("pct_of_target", ascending=False).reset_index(drop=True)
print(result)
print("stores at or above target:", (result["pct_of_target"] >= 100).sum())

# %% Step 3: hand it to a colleague
result.to_excel(OUTPUT / "targets_vs_actuals.xlsx", sheet_name="2025", index=False)
back = pd.read_excel(OUTPUT / "targets_vs_actuals.xlsx")
print("read back:", back.shape, back.columns.tolist())
