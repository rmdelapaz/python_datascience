# --- lab bootstrap: find labs_paths.py (the same three lines open every lab; see labs/README.md) ---
import pathlib, sys
sys.path[:0] = [str(p) for p in pathlib.Path(globals().get("__file__", "lab.py")).resolve().parents if (p / "labs_paths.py").is_file()]
from labs_paths import DATA, OUTPUT, OFFLINE

# %% [markdown]
# # Lab 7.3-A · Brush the catalog (SOLUTION)
# Question: are Pinecrest's high-margin products also the well-reviewed ones?
# Two scatter plots look at ONE table from two sides. Select products in one plot and the same
# rows light up in the other. Practices: ColumnDataSource, column names as glyph arguments,
# a formatted hover, selection tools, a row layout, output_file + save (never show() here).

# %% Load and prepare a minimal table (done for you in the starter)
import pandas as pd
from bokeh.layouts import row
from bokeh.models import ColumnDataSource, HoverTool, NumeralTickFormatter
from bokeh.plotting import figure, output_file, save

products = pd.read_csv(DATA / "products.csv")
products["margin"] = (products["price"] - products["cost"]) / products["price"]
table = products.dropna(subset=["rating"])[["name", "category", "price", "margin", "rating", "review_count"]]
print("products with a rating:", len(table), "| margin from", f"{table['margin'].min():.0%}", "to", f"{table['margin'].max():.0%}")

# %% Step 1: ONE source for the whole page
source = ColumnDataSource(table)
print("columns in the source:", source.column_names)
print("cost travels in the file:", "cost" in source.column_names)

# %% Step 2: two plots, the same source, selection tools
TOOLS = "box_select,lasso_select,tap,wheel_zoom,pan,reset"
tips = [("Product", "@name"), ("Category", "@category"), ("Price", "@price{$0,0.00}"),
        ("Margin", "@margin{0%}"), ("Rating", "@rating{0.0}"), ("Reviews", "@review_count{0,0}")]
style = dict(source=source, size=7, color="#667eea", alpha=0.6,
             nonselection_alpha=0.1, selection_color="#d97706")

left = figure(width=460, height=400, tools=TOOLS, active_drag="box_select", x_axis_type="log",
              title="Select a band of margins here...",
              x_axis_label="list price ($, log scale)", y_axis_label="margin (share of price)")
left_dots = left.scatter("price", "margin", **style)
left.yaxis.formatter = NumeralTickFormatter(format="0%")
left.add_tools(HoverTool(tooltips=tips))

right = figure(width=460, height=400, tools=TOOLS, active_drag="box_select",
               title="...and see how those products are rated",
               x_axis_label="number of reviews", y_axis_label="rating (1 to 5)")
right_dots = right.scatter("review_count", "rating", **style)
right.add_tools(HoverTool(tooltips=tips))

print("renderers:", len(left.renderers), "+", len(right.renderers),
      "| same source:", left_dots.data_source is right_dots.data_source)
print("left tools:", [type(t).__name__ for t in left.toolbar.tools])

# %% Step 3: save one HTML file to OUTPUT (save, not show)
target = OUTPUT / "margin_brush.html"
output_file(target, title="Brush the catalog", mode="cdn")
save(row(left, right))
text = target.read_text(encoding="utf-8")
print("saved:", target.name, f"| {len(text) / 1024:,.0f} KB", "| a product name is inside:", table["name"].iloc[0] in text)

# %% Step 4: what the brush shows, checked with pandas
high = table["margin"] >= 0.50
print(f"margin 50% or more: {int(high.sum())} products, mean rating {table.loc[high, 'rating'].mean():.2f}")
print(f"margin under 50%:   {int((~high).sum())} products, mean rating {table.loc[~high, 'rating'].mean():.2f}")
print(f"Spearman correlation of margin and rating: {table['margin'].corr(table['rating'], method='spearman'):+.2f}")
if not OFFLINE:
    print("Open output/margin_brush.html and drag a box in the left plot.")
