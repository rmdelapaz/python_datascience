# --- lab bootstrap: find labs_paths.py (the same three lines open every lab; see labs/README.md) ---
import pathlib, sys
sys.path[:0] = [str(p) for p in pathlib.Path(globals().get("__file__", "lab.py")).resolve().parents if (p / "labs_paths.py").is_file()]
from labs_paths import DATA

# %% [markdown]
# # Handout 0.1 · Read the traceback (three bugs, one at a time)
# This script is BROKEN ON PURPOSE. Run it, read the LAST line of the traceback first,
# then find the line number in THIS file, fix that one thing, and run it again.
# There are three bugs. Each one is a mistake from the lesson's Common Mistakes section.
#
# When all three are fixed it prints:
#     Orders: 20302
#     Returned orders: 1143
#     Largest returned order: $1,168.75

# %%
import pandas as pd

orders = pd.read_csv(DATA / "order.csv")

returned = orders[orders["Status"] == "returned"]

print("Orders:", len(orders))
print("Returned orders:", len(returned))
print(f"Largest returned order: ${retuned['order_total'].max():,.2f}")
