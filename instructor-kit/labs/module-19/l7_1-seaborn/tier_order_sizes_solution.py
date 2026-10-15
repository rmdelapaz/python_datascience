# --- lab bootstrap: find labs_paths.py (the same three lines open every lab; see labs/README.md) ---
import pathlib, sys
sys.path[:0] = [str(p) for p in pathlib.Path(globals().get("__file__", "lab.py")).resolve().parents if (p / "labs_paths.py").is_file()]
from labs_paths import DATA, OUTPUT

# %% [markdown]
# # Lab 7.1-A · Bigger orders, or more of them? (SOLUTION)
# Question: Gold members have spent the most by definition. Do they get there with bigger
# orders, or with more orders? Two axes-level seaborn charts in one Matplotlib figure.

# %% Load and merge (done for you in the starter)
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
per_customer = (table.groupby(["customer_id", "loyalty_tier"], as_index=False)
                     .agg(orders=("order_id", "count"), spend=("order_total", "sum")))
print("customers with at least one completed order:", len(per_customer))

# %% Step 2: the figure. Left: ECDF of order size. Right: mean orders per customer.
fig, axes = plt.subplots(1, 2, figsize=(10, 4), layout="constrained")

sns.ecdfplot(data=table, x="order_total", hue="loyalty_tier", hue_order=tiers, log_scale=True, ax=axes[0])
axes[0].axhline(0.5, color="gray", linewidth=1, linestyle="--")
axes[0].set_title("Gold orders are somewhat larger...", loc="left")
axes[0].set(xlabel="order total ($, log scale)", ylabel="share of orders at or below")
sns.move_legend(axes[0], "lower right", title="Tier")

sns.pointplot(data=per_customer, x="loyalty_tier", y="orders", order=tiers,
              errorbar=("ci", 95), seed=42, linestyle="none", capsize=0.2, ax=axes[1])
axes[1].set_title("...but mostly there are many more of them", loc="left")
axes[1].set(xlabel="", ylabel="completed orders per customer (mean, 95% CI)", ylim=(0, None))

target = OUTPUT / "tier_orders.png"
fig.savefig(target, dpi=150)
plt.close(fig)
print("saved:", target.name, "| panels:", len(fig.axes))

# %% Step 3: the numbers behind the two titles
sizes = table.groupby("loyalty_tier")["order_total"].median().loc[tiers]
counts = per_customer.groupby("loyalty_tier")["orders"].mean().loc[tiers]
print("median order total by tier:")
print(sizes.round(2).to_string())
print("mean completed orders per customer by tier:")
print(counts.round(2).to_string())
print(f"Gold vs Basic: order size x{sizes['Gold'] / sizes['Basic']:.2f}, "
      f"orders per customer x{counts['Gold'] / counts['Basic']:.2f}")
