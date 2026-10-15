# --- lab bootstrap: find labs_paths.py (the same three lines open every lab; see labs/README.md) ---
import pathlib, sys
sys.path[:0] = [str(p) for p in pathlib.Path(globals().get("__file__", "lab.py")).resolve().parents if (p / "labs_paths.py").is_file()]
from labs_paths import DATA
# %% [markdown]
# # Lab 2.3-B · What is each flaw worth? (STARTER)
# The lesson told you to keep the number in the TOTAL row of orders_messy.csv
# ("you can use it as a check later") and never used it. Use it now.
# Question: if someone simply added up the Order Total column of the messy file, how far
# off would they be, and which flaw moves the sum the most?
#
# Expected when you finish: a five-line table (the careless sum, then the sum after each
# of three repairs), the stated total from the TOTAL row, and the gap that is left,
# explained to the cent by the 40 orders whose total is blank.

# %% Load and tidy the headers (done for you)
import pandas as pd

pd.set_option("display.width", 150)
pd.set_option("display.max_columns", 20)
raw = pd.read_csv(DATA / "orders_messy.csv")
df = raw.copy()
df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_")
print(df.columns.tolist())

# %% Step 1: set the TOTAL row aside
# TODO 1: stated_total = the order_total of the row whose order_id is "TOTAL", as a float.
#         Then keep only the other rows in `df` and make order_id an int64 column.
stated_total = None

# %% Step 2: the careless sum
# TODO 2: turn order_total into numbers (remove "$" and ",", then pd.to_numeric).
#         careless = df["order_total"].sum()   <- duplicates, negatives and lost decimals all in.
careless = None

# %% Step 3: one repair at a time, recording the sum after each
# TODO 3a: drop exact duplicate rows                         -> after_duplicates
# TODO 3b: negative totals become positive (.abs())           -> after_negatives
# TODO 3c: totals 100 times too large: divide by 100 where
#          order_total / (the order's item subtotal) > 50     -> after_decimals
#          (item subtotal: order_items.csv, quantity * unit_price summed per order_id, then .map)
after_duplicates = after_negatives = after_decimals = None

# %% Step 4: explain what is left
# TODO 4: gap = stated_total - after_decimals. Load orders.csv (the answer key) and add up
#         the order_total of the orders whose total is blank in `df`. Is that the gap?
if None in (stated_total, careless, after_duplicates, after_negatives, after_decimals):
    print("TODO 1-4 not done yet: one of the sums is still None.")
