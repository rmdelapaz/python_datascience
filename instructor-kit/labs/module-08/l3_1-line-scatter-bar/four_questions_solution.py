# --- lab bootstrap: find labs_paths.py (the same three lines open every lab; see labs/README.md) ---
import pathlib, sys
sys.path[:0] = [str(p) for p in pathlib.Path(globals().get("__file__", "lab.py")).resolve().parents if (p / "labs_paths.py").is_file()]
from labs_paths import DATA, OUTPUT

# %% [markdown]
# # Lab 3.1-A · Four questions, four charts (SOLUTION)

# %% Load
import matplotlib.pyplot as plt
import pandas as pd

customers = pd.read_csv(DATA / "customers.csv", parse_dates=["signup_date"])
products = pd.read_csv(DATA / "products.csv")
print("customers:", customers.shape, "| products:", products.shape)

# %% Question 1: change over time -> a line
per_year = customers.groupby(customers["signup_date"].dt.year)["customer_id"].count()
print(per_year.to_string())
fig, ax = plt.subplots(figsize=(7, 3.5), layout="constrained")
ax.plot(per_year.index, per_year.values, marker="o", color="#667eea")
ax.set_title("New customer accounts per year")
ax.set_ylabel("Accounts opened")
ax.set_ylim(bottom=0)
fig.savefig(OUTPUT / "q1_signups.png")
print("Q1 line:", len(ax.lines), "line with", len(ax.lines[0].get_xdata()), "points; best year", per_year.idxmax(), "with", per_year.max())

# %% Question 2: comparing groups -> bars, horizontal and sorted
per_channel = customers["acquisition_channel"].value_counts().sort_values()
fig, ax = plt.subplots(figsize=(7, 3.5), layout="constrained")
bars = ax.barh(per_channel.index, per_channel.values, color="#667eea")
ax.bar_label(bars, padding=3)
ax.set_title("Customers by acquisition channel")
ax.set_xlabel("Number of customers")
fig.savefig(OUTPUT / "q2_channels.png")
print("Q2 bars:", len(bars), "bars; top bar is", per_channel.index[-1], "with", per_channel.iloc[-1])

# %% Question 3: two numbers -> a scatter
missing = int(products["weight_kg"].isna().sum())
fig, ax = plt.subplots(figsize=(7, 4.2), layout="constrained")
ax.scatter(products["weight_kg"], products["price"], s=18, alpha=0.5, color="#667eea")
ax.set_title(f"Heavier products cost more ({missing} products with no weight not shown)")
ax.set_xlabel("Weight (kg)")
ax.set_ylabel("Price (USD)")
fig.savefig(OUTPUT / "q3_weight_price.png")
print("Q3 scatter:", len(products) - missing, "dots,", missing, "products without a weight; correlation",
      round(products["weight_kg"].corr(products["price"]), 2))

# %% Question 4: one column, many rows -> a histogram
price = products["price"]
fig, ax = plt.subplots(figsize=(7, 3.5), layout="constrained")
counts, edges, patches = ax.hist(price, bins=30, color="#667eea", edgecolor="white")
ax.axvline(price.median(), color="black", linestyle="--", label=f"Median ${price.median():.2f}")
ax.set_title("List prices of the 242 products")
ax.set_xlabel("Price (USD)")
ax.set_ylabel("Number of products")
ax.legend()
fig.savefig(OUTPUT / "q4_prices.png")
print("Q4 histogram:", len(patches), "bins, each", round(edges[1] - edges[0], 2), "dollars wide; median",
      price.median(), "| products above $300:", int((price > 300).sum()))

# %% Close the figures and list what was saved
plt.close("all")
print("saved:", sorted(p.name for p in OUTPUT.glob("q*.png")))
