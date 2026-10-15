# --- lab bootstrap: find labs_paths.py (the same three lines open every lab; see labs/README.md) ---
import pathlib, sys
sys.path[:0] = [str(p) for p in pathlib.Path(globals().get("__file__", "lab.py")).resolve().parents if (p / "labs_paths.py").is_file()]
from labs_paths import DATA, OUTPUT, OFFLINE

# %% [markdown]
# # Lab 7.2-B · When do promo codes get used? (STARTER)
# Question: what share of each week's orders used a promo code, online and in store, and do the
# six sale weekends explain the spikes?
# Practices: aggregate with pandas BEFORE Plotly, a unified hover, shaded regions, a range slider,
# write_html to OUTPUT. Do not call fig.show() in this file: write the HTML and open it yourself.
#
# Expected when you finish: the weekly table's shape (210, 4), "2 traces | x unified | ...",
# "sale weekends shaded: 6" with their dates, one line comparing sale-weekend days with all other
# days, and "saved: promo_share.html".

# %% Load (done for you)
import pandas as pd
import plotly.express as px

orders = pd.read_csv(DATA / "orders.csv", parse_dates=["order_date"])
sales = pd.read_csv(DATA / "daily_sales.csv", parse_dates=["date"])
orders["used_code"] = orders["promo_code"].notna()
print("orders:", len(orders), "| with a promo code:", int(orders["used_code"].sum()))

# %% Step 1: aggregate first. One row per week and channel.
orders["week"] = orders["order_date"].dt.to_period("W-SUN").dt.start_time
# TODO 1: weekly = orders.groupby(["week", "channel"], as_index=False).agg(
#             orders=("order_id", "count"), share=("used_code", "mean"))   then print weekly.shape
weekly = None

# %% Step 2: the line chart, with a hover written for a reader
# TODO 2: fig = px.line(weekly, x="week", y="share", color="channel", custom_data=["orders"], ...)
# TODO 3: fig.update_traces(hovertemplate="%{y:.1%} of %{customdata[0]:,} orders")
#         fig.update_layout(title_text=..., hovermode="x unified", height=480)
#         fig.update_yaxes(tickformat=".0%", rangemode="tozero"); fig.update_xaxes(rangeslider_visible=True)
#         Print len(fig.data), fig.layout.hovermode and fig.data[0].hovertemplate.
fig = None

# %% Step 3: shade the sale weekends
promo_dates = sales.loc[sales["promo_day"] == 1, "date"].drop_duplicates().sort_values()
print("promotion dates in daily_sales:", len(promo_dates))
# TODO 4: group consecutive dates into weekends (hint: (promo_dates.diff().dt.days != 1).cumsum()),
#         take each block's min and max, and call fig.add_vrect(x0=..., x1=..., fillcolor="orange",
#         opacity=0.25, line_width=0) once per weekend. Print len(fig.layout.shapes).

# %% Step 4: back the title with a number
# TODO 5: what share of orders used a code on sale-weekend days, and on all other days?
#         Stretch: the left edge of the chart (January 2024) is high with no sale on. Why? (See data/README.md on WELCOME10.)

# %% Step 5: save
# TODO 6: fig.write_html(OUTPUT / "promo_share.html", include_plotlyjs="cdn") and print the file size in KB.

if weekly is None or fig is None:
    print("TODO 1-6 not done yet: `weekly` or `fig` is still None and no HTML file has been written.")
