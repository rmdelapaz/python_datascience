# --- lab bootstrap: find labs_paths.py (the same three lines open every lab; see labs/README.md) ---
import pathlib, sys
sys.path[:0] = [str(p) for p in pathlib.Path(globals().get("__file__", "lab.py")).resolve().parents if (p / "labs_paths.py").is_file()]
from labs_paths import DATA, OUTPUT, OFFLINE

# %% [markdown]
# # Lab 7.2-A · A product map a buyer can question (STARTER)
# Question: do pricier products get better ratings? And which products are the odd ones out?
# Practices: one Plotly Express call, a designed hover, a finished layout, write_html, and
# checking what data travels inside the file. Write the chart to OUTPUT; do not call fig.show() here.
#
# Expected when you finish: "Figure with 9 traces of type scatter", the hover template, the Spearman
# correlation, the lowest-rated product, "saved: product_map.html" with its size, and two True/False
# lines about what is inside the file.

# %% Load, and keep only the columns the chart needs (done for you)
import math

import pandas as pd
import plotly.express as px

products = pd.read_csv(DATA / "products.csv")
print("products:", len(products), "| no rating yet:", int(products["rating"].isna().sum()))
chart_table = products.dropna(subset=["rating"])[["name", "category", "price", "rating", "review_count"]]
print("rows going into the chart:", len(chart_table), "| columns:", list(chart_table.columns))

# %% Step 1: the Express call
# TODO 1: fig = px.scatter(chart_table, x="price", y="rating", color="category", size="review_count",
#         size_max=28, log_x=True, opacity=0.7, template="plotly_white", ...)
#         Add hover_name="name" and a hover_data dictionary that formats price as dollars (":$,.2f"),
#         rating with one decimal and review_count with a thousands separator. Add labels={...}.
#         Print len(fig.data), fig.data[0].type and fig.data[0].hovertemplate.
fig = None

# %% Step 2: finish the layout
# TODO 2: compute the Spearman correlation of price and rating and print it.
# TODO 3: fig.update_layout(title_text=<a title that states what you found>, height=520),
#         fig.update_xaxes(tickprefix="$"), fig.update_yaxes(range=[2.5, 5.2]).

# %% Step 3: point at the outlier a reader will ask about
# TODO 4: find the lowest-rated product and print its name, price, rating and review count.
#         Stretch: fig.add_annotation(...) pointing at it (on a log axis, x=math.log10(price)).

# %% Step 4: write one HTML file and look inside it
# TODO 5: fig.write_html(OUTPUT / "product_map.html", include_plotlyjs="cdn"), then read the file
#         back as text and print its size in KB, whether a product name is inside it,
#         and whether the word "cost" is inside it. Why does the second answer matter?

if fig is None:
    print("TODO 1-5 not done yet: `fig` is still None and no HTML file has been written.")
