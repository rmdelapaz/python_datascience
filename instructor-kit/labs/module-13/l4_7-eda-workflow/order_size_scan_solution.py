# --- lab bootstrap: find labs_paths.py (the same three lines open every lab; see labs/README.md) ---
import pathlib, sys
sys.path[:0] = [str(p) for p in pathlib.Path(globals().get("__file__", "lab.py")).resolve().parents if (p / "labs_paths.py").is_file()]
from labs_paths import DATA

# %% [markdown]
# # Lab 4.7-B · When are online orders bigger? (SOLUTION)
# The e-commerce team asks: "Are there days, months or payment methods where people place
# bigger online orders? We would like to time our 'add one more item' banner."
# That is step 6 of the routine, a segment scan, and a scan needs the two disciplines:
#   1. count every comparison and correct for them (Holm);
#   2. for whatever survives, check the obvious competing explanation.
#
# Reference solution. Do not hand out before the lab.

# %% Setup (done for you)
import pandas as pd
from scipy import stats
from statsmodels.stats.multitest import multipletests

orders = pd.read_csv(DATA / "orders.csv", parse_dates=["order_date"])
online = orders[orders["channel"] == "online"].copy()
online["weekday"] = online["order_date"].dt.day_name()
online["month"] = online["order_date"].dt.month_name()
print("online orders:", len(online), "| median order total:", online["order_total"].median())
print("order_total is right-skewed (mean", round(online["order_total"].mean(), 2),
      "), so compare medians and use the Mann-Whitney test.")

# %% Step 1: the scan - each group against all other online orders
rows = []
for seg in ["weekday", "payment_method", "month"]:
    for level in online[seg].unique():
        inside = online[seg] == level
        x = online.loc[inside, "order_total"]
        y = online.loc[~inside, "order_total"]
        rows.append({"segment": seg, "group": level, "n": len(x), "median": x.median(),
                     "median_rest": y.median(), "p": stats.mannwhitneyu(x, y).pvalue})
scan = pd.DataFrame(rows)

# %% Step 2: discipline 1 - count the comparisons and correct
scan["p_holm"] = multipletests(scan["p"], method="holm")[1]
print()
print(f"{len(scan)} tests, {(scan['p'] < 0.05).sum()} below 0.05 before correction, "
      f"{(scan['p_holm'] < 0.05).sum()} after")
top = scan.sort_values("p").head(5).copy()
top["p"] = top["p"].map("{:.5f}".format)
top["p_holm"] = top["p_holm"].map("{:.3f}".format)
print(top.to_string(index=False))

# %% Step 3: discipline 2 - could something else explain June?
# June is tent season (Lesson 2.4), and tents are expensive. Flag orders that contain a tent.
order_items = pd.read_csv(DATA / "order_items.csv")
tent_orders = order_items.loc[order_items["sku"].str.startswith("TNT"), "order_id"].unique()
online["has_tent"] = online["order_id"].isin(tent_orders)
online["june"] = online["month"] == "June"
print()
print("Share of online orders that contain a tent:")
print((online.groupby("june")["has_tent"].mean() * 100).round(1).to_string())
print()
print("Median order total:")
print(online.pivot_table(index="has_tent", columns="june", values="order_total", aggfunc="median").round(2).to_string())
for flag, grp in online.groupby("has_tent"):
    p = stats.mannwhitneyu(grp.loc[grp["june"], "order_total"], grp.loc[~grp["june"], "order_total"]).pvalue
    print(f"has_tent = {flag}: June against other months, p = {p:.2f}")

# %% Step 4: the note
print()
print("FINDINGS")
print("- Scanned 22 groups (7 weekdays, 3 payment methods, 12 months). Four had p < 0.05 before")
print("  correction; one survives Holm: June, median $169.40 against $154.95 in other months.")
print("- June's gap is mostly product mix: 17.7% of June orders contain a tent against 10.4% in other")
print("  months, and a tent order is about $329 against $144. Within tent orders and within non-tent")
print("  orders, June is only $3 to $8 higher and neither gap is significant (p = 0.60 and 0.14).")
print("CAVEATS")
print("- Saturday (lower), gift cards (lower) and April (higher) did not survive the correction:")
print("  leads, not findings.")
print("- Exploratory scan on observational data. 'Has a tent' was chosen after seeing June stand out.")
print("NEXT QUESTION")
print("- If the banner is about basket size, the lever is what is in the basket, not the calendar.")
