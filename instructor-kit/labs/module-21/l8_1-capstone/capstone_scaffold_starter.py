# --- lab bootstrap: find labs_paths.py (the same three lines open every lab; see labs/README.md) ---
import pathlib, sys
sys.path[:0] = [str(p) for p in pathlib.Path(globals().get("__file__", "lab.py")).resolve().parents if (p / "labs_paths.py").is_file()]
from labs_paths import DATA, OUTPUT

# %% [markdown]
# # Lab 8.1 · The capstone scaffold, filled in on a practice question (STARTER)
# The same eight sections as the Lesson 8.1 notebook outline, worked on a SMALL question that is not one
# of the four capstone questions:
#   "Online, are orders paid with a digital wallet returned more often than orders paid by card?"
# Decision it informs: whether the returns team should treat wallet orders differently.
# Sections 1 to 4 are done for you, with the helpers you will reuse in your own capstone notebook.
# Your job: sections 5 to 9. Then copy this skeleton (not its question) into pinecrest_report.ipynb.
#
# Expected when you finish: three comparison lines (all orders, without footwear, with footwear), each with
# two rates, a difference in points with a 95% CI, a p-value and Cohen's h; "saved: figure_1.png";
# and three sentences: the answer, one caveat, one next question.

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

# %% 5. Explore
# TODO 1: print the return rate and the share of footwear orders for each payment method,
#         and the median order total for each. Does anything differ that could make the comparison unfair?

# %% 6. Main comparison
# TODO 2: result = compare_rates(table, "all online orders")
result = None

# %% 7. Does it hold up?
# TODO 3: run compare_rates once for the orders with footwear and once for those without
#         (hint: for flag, part in table.groupby("footwear"): ...)

# %% 8. One figure that states the finding, saved from code
# TODO 4: return rate with 95% error bars, card vs wallet, for orders with and without footwear.
#         The title states the finding. Save with fig.savefig(OUTPUT / "figure_1.png", dpi=150).

# %% 9. Findings, caveats, next questions
# TODO 5: three printed sentences: the answer with its interval, one specific caveat, one next question.

if result is None:
    print("TODO 1-5 not done yet: the analysis table is built; the comparison, figure and findings are yours.")
