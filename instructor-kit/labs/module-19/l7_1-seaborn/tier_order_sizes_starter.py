# --- lab bootstrap: find labs_paths.py (the same three lines open every lab; see labs/README.md) ---
import pathlib, sys
sys.path[:0] = [str(p) for p in pathlib.Path(globals().get("__file__", "lab.py")).resolve().parents if (p / "labs_paths.py").is_file()]
from labs_paths import DATA, OUTPUT

# %% [markdown]
# # Lab 7.1-A · Bigger orders, or more of them? (STARTER)
# Question: Gold members have spent the most by definition. Do they get there with bigger
# orders, or with more orders? You will draw two axes-level seaborn charts in one figure.
#
# Expected when you finish: a merge check line, the number of customers, "saved: tier_orders.png",
# two small tables (median order total and mean orders per customer, by tier) and one line that
# compares Gold with Basic as two multipliers.

# %% Load and merge (done for you)
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

sns.set_theme(style="whitegrid", palette="colorblind")
tiers = ["Basic", "Silver", "Gold"]

orders = pd.read_csv(DATA / "orders.csv", parse_dates=["order_date"])
customers = pd.read_csv(DATA / "customers.csv")
completed = orders[orders["status"] == "completed"]
table = completed.merge(customers[["customer_id", "loyalty_tier"]], on="customer_id", validate="many_to_one")
print(f"completed orders: {len(completed):,} | with a customer row: {len(table):,} "
      f"| dropped (closed accounts): {len(completed) - len(table):,}")

# %% Step 1: one row per customer, with the number of completed orders
# TODO 1: group `table` by customer_id and loyalty_tier (as_index=False) and aggregate
#         orders=("order_id", "count"). Store it in per_customer and print how many customers it has.
per_customer = None

# %% Step 2: the figure
fig, axes = plt.subplots(1, 2, figsize=(10, 4), layout="constrained")

# TODO 2: on axes[0], draw sns.ecdfplot of order_total from `table`, one curve per tier
#         (hue=, hue_order=tiers), with log_scale=True. Add a dashed gray line at 0.5.

# TODO 3: on axes[1], draw sns.pointplot from `per_customer`: x = loyalty_tier, y = orders,
#         order=tiers, errorbar=("ci", 95), seed=42, linestyle="none", capsize=0.2.

# TODO 4: finish with Matplotlib: a title on each panel that states what it shows (loc="left"),
#         axis labels with units, and say in the right-hand y label what the bars are.

# TODO 5: fig.savefig(OUTPUT / "tier_orders.png", dpi=150) and print "saved: tier_orders.png"
plt.close(fig)

# %% Step 3: the numbers behind the two titles
# TODO 6: print the median order_total by tier (from `table`) and the mean number of orders
#         per customer by tier (from `per_customer`), tiers in the order Basic, Silver, Gold.
#         Then print the two Gold / Basic ratios.

if per_customer is None:
    print("TODO 1-6 not done yet: `per_customer` is still None and no chart has been saved.")
