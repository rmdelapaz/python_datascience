# --- lab bootstrap: find labs_paths.py (the same three lines open every lab; see labs/README.md) ---
import pathlib, sys
sys.path[:0] = [str(p) for p in pathlib.Path(globals().get("__file__", "lab.py")).resolve().parents if (p / "labs_paths.py").is_file()]
from labs_paths import DATA

# %% [markdown]
# # Find the bug · five broken filters (2.1)
# This file is broken ON PURPOSE. Run it, read the LAST line of the error, fix that one
# line, run again. There are five bugs. Three stop the program; two are silent, and you
# will only find them by checking the printed numbers against the "should print" notes.

# %%
import numpy as np
import pandas as pd

products = pd.read_csv(DATA / "products.csv")

# %% Bug 1 (stops the program)
print("median price:", products["Price"].median())                      # should print 82.95

# %% Bug 2 (stops the program)
pricey_and_loved = products[products["price"] > 100 and products["rating"] > 4.5]
print("over $100 and rated above 4.5:", len(pricey_and_loved))           # should print 14

# %% Bug 3 (stops the program)
cheap_tents = products[products["category"] == "Tents" & products["price"] < 200]
print("tents under $200:", len(cheap_tents))                             # should print 7

# %% Bug 4 (silent: wrong number)
print("products with no rating:", (products["rating"] == np.nan).sum())   # should print 8

# %% Bug 5 (silent: a warning, and nothing changes)
products["on_sale"] = False
products[products["stock_status"] == "low_stock"]["on_sale"] = True
print("products on sale:", products["on_sale"].sum())                    # should print 29
