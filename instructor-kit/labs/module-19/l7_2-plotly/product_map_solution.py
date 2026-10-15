# --- lab bootstrap: find labs_paths.py (the same three lines open every lab; see labs/README.md) ---
import pathlib, sys
sys.path[:0] = [str(p) for p in pathlib.Path(globals().get("__file__", "lab.py")).resolve().parents if (p / "labs_paths.py").is_file()]
from labs_paths import DATA, OUTPUT, OFFLINE

# %% [markdown]
# # Lab 7.2-A · A product map a buyer can question (SOLUTION)
# Question: do pricier products get better ratings? And which products are the odd ones out?
# Practices: one Plotly Express call, a designed hover, a finished layout, write_html, and
# checking what data travels inside the file. The chart is written to OUTPUT, never opened here.

# %% Load, and keep only the columns the chart needs (done for you in the starter)
import math

import pandas as pd
import plotly.express as px

products = pd.read_csv(DATA / "products.csv")
print("products:", len(products), "| no rating yet:", int(products["rating"].isna().sum()))
chart_table = products.dropna(subset=["rating"])[["name", "category", "price", "rating", "review_count"]]
print("rows going into the chart:", len(chart_table), "| columns:", list(chart_table.columns))

# %% Step 1: the Express call
fig = px.scatter(chart_table, x="price", y="rating", color="category", size="review_count", size_max=28,
                 log_x=True, opacity=0.7, template="plotly_white",
                 category_orders={"category": sorted(chart_table["category"].unique())},
                 hover_name="name",
                 hover_data={"category": True, "price": ":$,.2f", "rating": ":.1f", "review_count": ":,"},
                 labels={"price": "List price", "rating": "Rating", "review_count": "Reviews",
                         "category": "Category"})
print(type(fig).__name__, "with", len(fig.data), "traces of type", fig.data[0].type)
print("hover:", fig.data[0].hovertemplate)

# %% Step 2: finish the layout (the title states the finding)
rho = chart_table["price"].corr(chart_table["rating"], method="spearman")
fig.update_layout(title_text="Price tells you almost nothing about rating", height=520,
                  legend=dict(title_text="", orientation="h", y=-0.2))
fig.update_xaxes(tickprefix="$")
fig.update_yaxes(range=[2.5, 5.2])
print(f"Spearman correlation of price and rating: {rho:+.2f}")

# %% Step 3: point at the outlier a reader will ask about
worst = chart_table.sort_values("rating").iloc[0]
# On a log axis an annotation's x is the log10 of the value.
fig.add_annotation(x=math.log10(worst["price"]), y=worst["rating"], text="lowest rated",
                   showarrow=True, arrowhead=2, ax=60, ay=-30)
print(f"lowest rated: {worst['name']} | ${worst['price']:.2f} | rating {worst['rating']} | {worst['review_count']} reviews")

# %% Step 4: write one HTML file (library linked from the CDN) and look inside it
target = OUTPUT / "product_map.html"
fig.write_html(target, include_plotlyjs="cdn")
text = target.read_text(encoding="utf-8")
print("saved:", target.name, f"| {len(text) / 1024:,.0f} KB")
print("product name inside the file:", worst["name"] in text)
print("cost column inside the file:", '"cost"' in text or "cost=" in text)
if not OFFLINE:
    print("Open it from your file manager (or add fig.show() in a notebook).")
