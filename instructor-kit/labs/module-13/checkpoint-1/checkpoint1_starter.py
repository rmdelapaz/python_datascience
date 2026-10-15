# --- lab bootstrap: find labs_paths.py (the same three lines open every lab; see labs/README.md) ---
import pathlib, sys
sys.path[:0] = [str(p) for p in pathlib.Path(globals().get("__file__", "lab.py")).resolve().parents if (p / "labs_paths.py").is_file()]
from labs_paths import DATA, OUTPUT

# %% [markdown]
# # Checkpoint 1 · Do December shoppers buy pricier things? (your notebook)
# 30 minutes, open notebook, your own work. The full task sheet is in your workbook.
#
# Pinecrest's store buyers believe that December shoppers buy more expensive things.
# Finance wants a number before it plans next December's stock.
# Using daily_sales.csv: is the average price per unit sold (revenue / units) higher in
# December than in the rest of the year? By how much, how sure are you, and is it the same
# in all four stores?
#
# Expected when you finish: your checks, one comparison with an estimate, a 95% confidence
# interval, a test and an effect size, one labeled figure saved to OUTPUT, and a short note
# (findings with numbers, caveats, one next question).

# %% 1. Plan: fill these in BEFORE you write any code (about 3 minutes)
plan = {
    "measure": "TODO: what exactly will you compute for each row?",
    "comparison": "TODO: which rows against which rows?",
    "checks": "TODO: what will you check before trusting the numbers?",
}

# %% 2. Load and check (done for you: the load; the checks are yours)
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy import stats

daily = pd.read_csv(DATA / "daily_sales.csv", parse_dates=["date"])
print("rows:", len(daily))

# %% 3. The comparison: estimate, interval, test, effect size

# %% 4. Does it hold in every store? Is "December against the rest" a fair split?

# %% 5. One figure with a title that states the finding
# fig.savefig(OUTPUT / "checkpoint1.png", dpi=150)

# %% 6. Your note: two findings with numbers, two caveats, one next question
note = """
FINDINGS
- TODO
CAVEATS
- TODO
NEXT QUESTION
- TODO
"""
print(plan)
print(note)
