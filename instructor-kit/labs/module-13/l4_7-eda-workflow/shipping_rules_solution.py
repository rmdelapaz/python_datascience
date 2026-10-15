# --- lab bootstrap: find labs_paths.py (the same three lines open every lab; see labs/README.md) ---
import pathlib, sys
sys.path[:0] = [str(p) for p in pathlib.Path(globals().get("__file__", "lab.py")).resolve().parents if (p / "labs_paths.py").is_file()]
from labs_paths import DATA

# %% [markdown]
# # Lab 4.7-A · Who pays for shipping? (SOLUTION)
# Nobody at Pinecrest can find the document that says how shipping is charged. The data
# dictionary only says: shipping_cost is 0.00, 6.95 or 14.95.
# Run the routine on one column and work the rule out from the data.
#
# Step 1, the questions (written before loading anything):
#   1. Which orders are charged shipping at all?
#   2. What decides whether an order pays 0.00, 6.95 or 14.95?
#   3. What can the data not tell us about shipping?
#
# Reference solution. Do not hand out before the lab.

# %% Step 2: structure (done for you)
import pandas as pd

orders = pd.read_csv(DATA / "orders.csv", parse_dates=["order_date"])
print("rows:", len(orders), "| order_id unique:", orders["order_id"].is_unique)
print("grain: one row per order")

# %% Step 3: quality - anything missing or impossible in the columns we need?
cols = ["channel", "shipping_cost", "order_total"]
print()
print("missing values:", orders[cols].isna().sum().to_dict())
print("shipping values:", sorted(orders["shipping_cost"].unique().tolist()))
print(pd.crosstab(orders["channel"], orders["shipping_cost"]).to_string())
print("Store orders never pay shipping, so questions 2 and 3 are about ONLINE orders only.")

# %% Step 4: one variable - how common is each charge online?
online = orders[orders["channel"] == "online"].copy()
share = online["shipping_cost"].value_counts(normalize=True).sort_index()
print()
print((share * 100).round(1).to_string())

# %% Step 5: two variables - the charge against the value of the goods
# order_total includes the shipping, so take it out first.
online["goods"] = (online["order_total"] - online["shipping_cost"]).round(2)
print()
print(online.groupby("shipping_cost")["goods"].agg(["count", "min", "median", "max"]).round(2).to_string())

# %% Step 5b: the picture suggests a threshold - test the idea directly
online["goods_75_plus"] = online["goods"] >= 75
print()
print(pd.crosstab(online["goods_75_plus"], online["shipping_cost"]).to_string())

# %% Step 6: segments - is the 14.95 charge tied to order size?
bands = pd.cut(online["goods"], [0, 25, 50, 75, 100, 150, 300, 5000], right=False)
by_band = pd.crosstab(bands, online["shipping_cost"], normalize="index") * 100
print()
print(by_band.round(1).to_string())

# %% Step 7: findings, caveats, next questions
print()
print("FINDINGS")
print("- Store orders never pay shipping. Online: 71.4% ship free, 21.4% pay 6.95, 7.2% pay 14.95.")
print("- Among orders that did not pay 14.95, the rule is exact: goods of 75.00 or more ship free")
print("  (9,176 of 9,176), goods under 75.00 pay 6.95 (2,754 of 2,754). No exceptions in two years.")
print("- The 14.95 charge appears at every order size, on about 6% to 9% of orders in each band.")
print("CAVEATS")
print("- The rule is inferred from the data, not read from a policy. 14.95 looks like an option the")
print("  customer chooses (faster delivery?): a hypothesis. No column records the delivery method.")
print("- 'goods' is the total after any discount: the threshold applies to what the customer pays.")
print("NEXT QUESTIONS")
print("- Do customers add items to reach 75.00? (Look at the distribution of goods just above and below.)")
