# --- lab bootstrap: find labs_paths.py (the same three lines open every lab; see labs/README.md) ---
import pathlib, sys
sys.path[:0] = [str(p) for p in pathlib.Path(globals().get("__file__", "lab.py")).resolve().parents if (p / "labs_paths.py").is_file()]
from labs_paths import DATA, OUTPUT

# %% [markdown]
# # Lab 8.1 · The capstone scaffold, filled in on a practice question (SOLUTION)
# The same eight sections as the Lesson 8.1 notebook outline, worked on a SMALL question that is not one
# of the four capstone questions:
#   "Online, are orders paid with a digital wallet returned more often than orders paid by card?"
# Decision it informs: whether the returns team should treat wallet orders differently.
# What this file shows is the SHAPE of the work: plan, checks, one fair comparison with an estimate,
# an interval, a test and an effect size, one robustness check, one figure, and three sentences.

# %% 1. Plan (in the notebook this is a Markdown cell, written before any code)
PLAN = """
Measure: return rate = returned orders / (completed + returned) orders. Cancelled orders never shipped, so they are left out.
Comparison: online orders paid by digital_wallet against online orders paid by card, 2024-2025.
Risk to fairness: payment method may go with order size or with footwear (which is returned far more often online).
Check: repeat the comparison within orders with and without footwear.
Would change my mind: a difference that vanishes inside both footwear groups.
"""
print(PLAN.strip())

# %% 2. Setup
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from statsmodels.stats.proportion import confint_proportions_2indep, proportions_ztest


def overview(df, name):
    """One line per table: shape, missing cells, duplicate keys (the Lesson 4.7 habit)."""
    print(f"{name:<12} {df.shape} | missing cells {int(df.isna().sum().sum())} | duplicate rows {int(df.duplicated().sum())}")


def cohens_h(p1, p2):
    """Effect size for two proportions."""
    return 2 * np.arcsin(np.sqrt(p1)) - 2 * np.arcsin(np.sqrt(p2))


def compare_rates(table, label):
    """Estimate, 95% CI, two-proportion z-test and Cohen's h for wallet against card."""
    g = table.groupby("payment_method")["returned"].agg(["sum", "count"])
    w, c = g.loc["digital_wallet"], g.loc["card"]
    pw, pc = w["sum"] / w["count"], c["sum"] / c["count"]
    z, p = proportions_ztest([w["sum"], c["sum"]], [w["count"], c["count"]])
    lo, hi = confint_proportions_2indep(w["sum"], w["count"], c["sum"], c["count"], compare="diff")
    print(f"{label:<28} wallet {pw:.1%} (n={int(w['count'])}) vs card {pc:.1%} (n={int(c['count'])}): "
          f"{(pw - pc) * 100:+.1f} pts (95% CI {lo * 100:+.1f} to {hi * 100:+.1f}), p={p:.2f}, h={cohens_h(pw, pc):+.3f}")
    return pw, pc, lo, hi


# %% 3. Load and check
orders = pd.read_csv(DATA / "orders.csv", parse_dates=["order_date"])
items = pd.read_csv(DATA / "order_items.csv")
overview(orders, "orders")
overview(items, "order_items")
print("order_id unique:", orders["order_id"].is_unique, "| statuses:", orders["status"].value_counts().to_dict())


# %% 4. Prepare: one function builds the analysis table, with row counts around each step
def build_table():
    online = orders[(orders["channel"] == "online") & (orders["status"] != "cancelled")]
    print("online, not cancelled:", len(online))
    two = online[online["payment_method"].isin(["card", "digital_wallet"])].copy()
    print("paid by card or wallet:", len(two), f"(dropped {len(online) - len(two)} gift-card orders)")
    footwear_orders = set(items.loc[items["sku"].str.startswith("FTW"), "order_id"])
    two["footwear"] = two["order_id"].isin(footwear_orders)
    two["returned"] = (two["status"] == "returned").astype(int)
    return two


table = build_table()

# %% 5. Explore (short here; longer in a real capstone)
print(table.groupby("payment_method")[["returned", "footwear"]].mean().round(3))
print("median order total:", table.groupby("payment_method")["order_total"].median().to_dict())

# %% 6. Main comparison
pw, pc, lo, hi = compare_rates(table, "all online orders")

# %% 7. Does it hold up? Within footwear and non-footwear orders
for flag, part in table.groupby("footwear"):
    compare_rates(part, "with footwear" if flag else "without footwear")

# %% 8. One figure that states the finding, saved from code
rates = table.groupby(["footwear", "payment_method"])["returned"].agg(["mean", "count"]).reset_index()
rates["half"] = 1.96 * np.sqrt(rates["mean"] * (1 - rates["mean"]) / rates["count"])
fig, ax = plt.subplots(figsize=(7, 3.6), layout="constrained")
for k, (method, color) in enumerate([("card", "#7f7f7f"), ("digital_wallet", "#d97706")]):
    part = rates[rates["payment_method"] == method]
    ax.errorbar(np.arange(2) + (k - 0.5) * 0.2, part["mean"] * 100, yerr=part["half"] * 100, fmt="o",
                capsize=4, color=color, label=method.replace("_", " "))
ax.set_xticks([0, 1], ["orders without footwear", "orders with footwear"])
ax.set(ylabel="returned (%)", title="Payment method makes no clear difference to returns; footwear does")
ax.legend(frameon=False)
fig.supxlabel("Online orders 2024-2025, cancelled excluded. Bars: 95% confidence intervals.", fontsize=8)
target = OUTPUT / "figure_1.png"
fig.savefig(target, dpi=150)
plt.close(fig)
print("saved:", target.name)

# %% 9. Findings, caveats, next questions (the draft of report.md)
print(f"Answer: wallet and card orders are returned at about the same rate ({pw:.1%} vs {pc:.1%}); "
      f"the difference could be anywhere from {lo * 100:+.1f} to {hi * 100:+.1f} points.")
print("Caveat: customers choose how to pay, so this describes orders, not what would happen if a customer switched.")
print("Next question: is the footwear effect about fit (sizes) or about particular products?")
