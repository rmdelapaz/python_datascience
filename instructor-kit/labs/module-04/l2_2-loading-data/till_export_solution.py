# --- lab bootstrap: find labs_paths.py (the same three lines open every lab; see labs/README.md) ---
import pathlib, sys
sys.path[:0] = [str(p) for p in pathlib.Path(globals().get("__file__", "lab.py")).resolve().parents if (p / "labs_paths.py").is_file()]
from labs_paths import DATA
# %% [markdown]
# # Lab 2.2-A · Brief the interpreter (SOLUTION)
# Load the till system's export with the right options, then prove the load is right.

# %% Look at the raw text first
import pathlib

import numpy as np
import pandas as pd

EXPORT = pathlib.Path(globals().get("__file__", "lab.py")).resolve().parent / "till_export_week08.txt"
with open(EXPORT, encoding="utf-8") as f:
    for _ in range(6):
        print(f.readline().rstrip())

# %% Step 1: read it with no options and see what goes wrong
naive = pd.read_csv(EXPORT)
print("no options:", naive.shape, naive.columns.tolist())

# %% Step 2: brief the reader
week = pd.read_csv(
    EXPORT,
    sep=";",                  # semicolons between values
    skiprows=3,               # three lines of notes above the header
    decimal=",",              # 3.536,91 has a decimal comma...
    thousands=".",            # ...and a dot for thousands
    na_values=["n/a"],        # this file's word for "missing"
    parse_dates=["date"],
    date_format="%d.%m.%Y",   # 17.02.2025 is day.month.year
)

# %% Step 3: check the translation
print(week.dtypes.to_string())
print("shape:", week.shape)
print(week[week["revenue"].isna()].to_string())

# %% Step 4: prove it against the clean file
daily = pd.read_csv(DATA / "daily_sales.csv", parse_dates=["date"])
same_week = daily[daily["date"].between("2025-02-17", "2025-02-23")]
print("export revenue :", round(week["revenue"].sum(), 2))
print("clean revenue  :", round(same_week["revenue"].sum(), 2))
print("totals match:", bool(np.isclose(week["revenue"].sum(), same_week["revenue"].sum())))
print("visitors match:", bool(week["visitors"].sum() == same_week["visitors"].sum()), "|", week["visitors"].sum())
