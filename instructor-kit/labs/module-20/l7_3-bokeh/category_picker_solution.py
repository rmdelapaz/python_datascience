# --- lab bootstrap: find labs_paths.py (the same three lines open every lab; see labs/README.md) ---
import pathlib, sys
sys.path[:0] = [str(p) for p in pathlib.Path(globals().get("__file__", "lab.py")).resolve().parents if (p / "labs_paths.py").is_file()]
from labs_paths import DATA, OUTPUT, OFFLINE

# %% [markdown]
# # Lab 7.3-B · A category picker that needs no server (SOLUTION)
# Question for the reader of the page: within one product category, how do price and rating relate?
# Practices: a CDSView with a GroupFilter, a Select widget with a CustomJS callback, js_link from a
# Slider to a reference line, a Div the callback rewrites, column/row layouts, cdn against inline files.

# %% Load (done for you in the starter)
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


def build_page():
    """Fresh objects every call: a Bokeh object can belong to only one saved page."""
    source = ColumnDataSource(table)

    # Step 1: a view that shows one category
    category_filter = GroupFilter(column_name="category", group=START)
    view = CDSView(filter=category_filter)
    p = figure(width=760, height=380, title=f"{START}: price and rating",
               x_axis_label="list price ($)", y_axis_label="rating (1 to 5)",
               y_range=(2.5, 5.2), tools="pan,wheel_zoom,reset")
    p.scatter("price", "rating", source=source, view=view, size=9, alpha=0.7, color="#667eea")
    p.add_tools(HoverTool(tooltips=[("Product", "@name"), ("Price", "@price{$0,0.00}"),
                                    ("Rating", "@rating{0.0}"), ("Reviews", "@review_count{0,0}")]))

    # Step 2: a reference line that a slider moves (no JavaScript written by you)
    line = Span(location=4.0, dimension="width", line_color="#d97706", line_width=2, line_dash="dashed")
    p.add_layout(line)
    slider = Slider(start=3.0, end=5.0, value=4.0, step=0.1, title="Reference rating", width=260)
    slider.js_link("value", line, "location")

    # Step 3: the picker, and a sentence that the callback rewrites
    start_count = int((table["category"] == START).sum())
    count = Div(text=f"<b>{start_count}</b> products in {START}", width=260)
    picker = Select(title="Category", value=START, options=categories, width=200)
    picker.js_on_change("value", CustomJS(args=dict(flt=category_filter, plot=p, source=source, count=count), code="""
        flt.group = cb_obj.value;
        plot.title.text = cb_obj.value + ": price and rating";
        let n = 0;
        for (const value of source.data["category"]) {
            if (value === cb_obj.value) { n += 1; }
        }
        count.text = "<b>" + n + "</b> products in " + cb_obj.value;
    """))
    return column(row(picker, slider, count), p), view, start_count


# %% Step 4: save twice, once per mode, and compare the files
page, view, start_count = build_page()
print("view shows:", view.filter.column_name, "=", view.filter.group, "|", start_count, "products to start with")
cdn = OUTPUT / "category_picker.html"
output_file(cdn, title="Category picker", mode="cdn")
save(page)

page_inline, _, _ = build_page()                  # a new page needs new objects
inline = OUTPUT / "category_picker_offline.html"
output_file(inline, title="Category picker", mode="inline")
save(page_inline)
for path in (cdn, inline):
    print(f"saved: {path.name:<30} {path.stat().st_size / 1024:8,.0f} KB")

# %% Step 5: the numbers the callback should show, computed in Python (test your page against these)
print(table["category"].value_counts().sort_index().to_string())
if not OFFLINE:
    print("Open output/category_picker.html, choose a category and compare the count with the table above.")
