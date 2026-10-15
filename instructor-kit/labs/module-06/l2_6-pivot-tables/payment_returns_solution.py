# --- lab bootstrap: find labs_paths.py (the same three lines open every lab; see labs/README.md) ---
import pathlib, sys
sys.path[:0] = [str(p) for p in pathlib.Path(globals().get("__file__", "lab.py")).resolve().parents if (p / "labs_paths.py").is_file()]
from labs_paths import DATA
# %% [markdown]
# # Lab 2.6-A · Returns by payment method: read the grid honestly (SOLUTION)
# Question: are orders paid one way returned more often than orders paid another way?

# %% Load
import pandas as pd

pd.set_option("display.width", 150)
pd.set_option("display.max_columns", 20)

orders = pd.read_csv(DATA / "orders.csv", parse_dates=["order_date"])
orders["returned"] = orders["status"] == "returned"
print(orders.shape)

# %% Step 1: how many orders are behind each cell?
counts = orders.pivot_table(index="payment_method", columns="store", values="order_id",
                            aggfunc="count", fill_value=0, margins=True, margins_name="Total")
print(counts)
print("corner equals the number of orders:", counts.loc["Total", "Total"] == len(orders))

# %% Step 2: the return rate in each cell (the mean of True/False, times 100)
# No fill_value here: "cash, Online" has no orders, so a return rate of 0% would be a false statement.
rate = orders.pivot_table(index="payment_method", columns="store", values="returned",
                          aggfunc="mean", margins=True) * 100
print(rate.round(1))

# %% Step 3: a mean without its count is half a fact
cell_rate = rate.loc["gift_card", "Bend"]
cell_orders = counts.loc["gift_card", "Bend"]
print(f"gift cards in Bend: {cell_rate:.1f}% of {cell_orders} orders = {round(cell_rate / 100 * cell_orders)} returned order")

# %% Step 4: two crosstabs, two questions
of_method = pd.crosstab(orders["payment_method"], orders["status"], normalize="index") * 100
of_status = pd.crosstab(orders["payment_method"], orders["status"], normalize="columns") * 100
print(of_method.round(1))
print(of_status.round(1))
print(f"Of digital-wallet orders, {of_method.loc['digital_wallet', 'returned']:.1f}% were returned.")
print(f"Of returned orders, {of_status.loc['digital_wallet', 'returned']:.1f}% were paid by digital wallet.")

# %% Step 5: does the total hide a difference inside it?
by_channel = orders.pivot_table(index="payment_method", columns="channel", values="returned",
                                aggfunc="mean", margins=True) * 100
print(by_channel.round(1))
