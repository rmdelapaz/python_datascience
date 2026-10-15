# --- lab bootstrap: find labs_paths.py (the same three lines open every lab; see labs/README.md) ---
import pathlib, sys
sys.path[:0] = [str(p) for p in pathlib.Path(globals().get("__file__", "lab.py")).resolve().parents if (p / "labs_paths.py").is_file()]
from labs_paths import DATA, OUTPUT, OFFLINE

# %% [markdown]
# # Lab 7.3-B · A category picker that needs no server (STARTER)
# Question for the reader of the page: within one product category, how do price and rating relate?
# You will build a dropdown that filters the chart inside a plain HTML file. Use save, not show().
#
# Expected when you finish: "view shows: category = Tents | 24 products to start with",
# two "saved:" lines (a small cdn file and a much larger offline file), and the number of rated
# products in each category, which your page's counter should match when you pick each one.

# %% Load (done for you)
import pandas as pd
from bokeh.layouts import column, row
from bokeh.models import (CDSView, ColumnDataSource, CustomJS, Div, GroupFilter, HoverTool,
                          Select, Slider, Span)
from bokeh.plotting import figure, output_file, save

products = pd.read_csv(DATA / "products.csv")
table = products.dropna(subset=["rating"])[["name", "category", "price", "rating", "review_count"]]
categories = sorted(table["category"].unique())
START = "Tents"
print(len(table), "rated products in", len(categories), "categories")

# %% Step 1: a view that shows one category
# TODO 1: source = ColumnDataSource(table)
#         category_filter = GroupFilter(column_name="category", group=START)
#         view = CDSView(filter=category_filter)
#         p = figure(width=760, height=380, y_range=(2.5, 5.2), tools="pan,wheel_zoom,reset", ...)
#         p.scatter("price", "rating", source=source, view=view, size=9, alpha=0.7, color="#667eea")
#         Add a HoverTool with the product name and a formatted price.
view = None

# %% Step 2: a reference line that a slider moves
# TODO 2: line = Span(location=4.0, dimension="width", line_dash="dashed"); p.add_layout(line)
#         slider = Slider(start=3.0, end=5.0, value=4.0, step=0.1, title="Reference rating")
#         slider.js_link("value", line, "location")

# %% Step 3: the picker, and a sentence that the callback rewrites
# TODO 3: picker = Select(title="Category", value=START, options=categories)
#         count = Div(text=...)   with the starting count computed in Python
#         picker.js_on_change("value", CustomJS(args=dict(flt=category_filter, plot=p, source=source, count=count),
#                                               code="""..."""))
#         In the JavaScript: set flt.group, set plot.title.text, loop over source.data["category"]
#         counting matches, and write the sentence into count.text.

# %% Step 4: save
# TODO 4: output_file(OUTPUT / "category_picker.html", title="Category picker", mode="cdn")
#         save(column(row(picker, slider, count), p))
#         Stretch: save a second copy with mode="inline" (build fresh objects first!) and compare sizes.

# %% Step 5: the numbers the callback should show, computed in Python
print(table["category"].value_counts().sort_index().to_string())

if view is None:
    print("TODO 1-4 not done yet: `view` is still None and no HTML file has been written.")
