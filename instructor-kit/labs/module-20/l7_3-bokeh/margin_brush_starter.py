# --- lab bootstrap: find labs_paths.py (the same three lines open every lab; see labs/README.md) ---
import pathlib, sys
sys.path[:0] = [str(p) for p in pathlib.Path(globals().get("__file__", "lab.py")).resolve().parents if (p / "labs_paths.py").is_file()]
from labs_paths import DATA, OUTPUT, OFFLINE

# %% [markdown]
# # Lab 7.3-A · Brush the catalog (STARTER)
# Question: are Pinecrest's high-margin products also the well-reviewed ones?
# Two scatter plots look at ONE table from two sides. Select products in one plot and the same
# rows light up in the other. Use output_file + save: do not call show() in this file.
#
# Expected when you finish: the source's column names (no "cost"), "renderers: 1 + 1 | same source: True",
# the left plot's tools, "saved: margin_brush.html" with its size, two lines comparing the mean rating
# of high-margin and other products, and the Spearman correlation.

# %% Load and prepare a minimal table (done for you)
import pandas as pd
from bokeh.layouts import row
from bokeh.models import ColumnDataSource, HoverTool, NumeralTickFormatter
from bokeh.plotting import figure, output_file, save

products = pd.read_csv(DATA / "products.csv")
products["margin"] = (products["price"] - products["cost"]) / products["price"]
table = products.dropna(subset=["rating"])[["name", "category", "price", "margin", "rating", "review_count"]]
print("products with a rating:", len(table), "| margin from", f"{table['margin'].min():.0%}", "to", f"{table['margin'].max():.0%}")

# %% Step 1: ONE source for the whole page
# TODO 1: source = ColumnDataSource(table). Print source.column_names.
#         Is "cost" in it? Why did the starter leave cost out of `table`?
source = None

# %% Step 2: two plots, the same source, selection tools
TOOLS = "box_select,lasso_select,tap,wheel_zoom,pan,reset"
# TODO 2: left = figure(width=460, height=400, tools=TOOLS, active_drag="box_select", x_axis_type="log", ...)
#         left.scatter("price", "margin", source=source, size=7, color="#667eea", alpha=0.6,
#                      nonselection_alpha=0.1, selection_color="#d97706")
# TODO 3: right = figure(...) with right.scatter("review_count", "rating", ...) from the SAME source.
# TODO 4: a hover on both plots: HoverTool(tooltips=[("Product", "@name"), ("Price", "@price{$0,0.00}"),
#         ("Margin", "@margin{0%}"), ...]) and fig.add_tools(...). Format the left y axis as a percentage.

# %% Step 3: save one HTML file to OUTPUT
# TODO 5: output_file(OUTPUT / "margin_brush.html", title="Brush the catalog"); save(row(left, right))
#         Then open the file from your file manager and drag a box around the highest margins.

# %% Step 4: what the brush shows, checked with pandas
# TODO 6: compare the mean rating of products with a margin of 50% or more with the rest,
#         and print the Spearman correlation of margin and rating.

if source is None:
    print("TODO 1-6 not done yet: `source` is still None and no HTML file has been written.")
