# --- lab bootstrap: find labs_paths.py (the same three lines open every lab; see labs/README.md) ---
import pathlib, sys
sys.path[:0] = [str(p) for p in pathlib.Path(globals().get("__file__", "lab.py")).resolve().parents if (p / "labs_paths.py").is_file()]
from labs_paths import DATA, OUTPUT, OFFLINE

# %% [markdown]
# # Lab 7.2-B · When do promo codes get used? (SOLUTION)
# Question: what share of each week's orders used a promo code, online and in store, and do the
# six sale weekends explain the spikes?
# Practices: aggregate with pandas BEFORE Plotly, a unified hover, shaded regions, a range slider,
# write_html to OUTPUT, and an optional static image that is skipped cleanly when Chrome is missing.

# %% Load (done for you in the starter)
import os
import shutil

import pandas as pd
import plotly.express as px

orders = pd.read_csv(DATA / "orders.csv", parse_dates=["order_date"])
sales = pd.read_csv(DATA / "daily_sales.csv", parse_dates=["date"])
orders["used_code"] = orders["promo_code"].notna()
print("orders:", len(orders), "| with a promo code:", int(orders["used_code"].sum()))

# %% Step 1: aggregate first. One row per week and channel.
orders["week"] = orders["order_date"].dt.to_period("W-SUN").dt.start_time
weekly = (orders.groupby(["week", "channel"], as_index=False)
                .agg(orders=("order_id", "count"), share=("used_code", "mean")))
print("weekly table:", weekly.shape, "| typical week (median share):",
      {k: f"{v:.1%}" for k, v in weekly.groupby("channel")["share"].median().items()})

# %% Step 2: the line chart, with a hover written for a reader
fig = px.line(weekly, x="week", y="share", color="channel", custom_data=["orders"],
              category_orders={"channel": ["online", "store"]}, template="plotly_white",
              labels={"week": "", "share": "Orders using a promo code", "channel": ""})
fig.update_traces(hovertemplate="%{y:.1%} of %{customdata[0]:,} orders")
fig.update_layout(title_text="Promo-code use jumps on the six sale weekends",
                  hovermode="x unified", height=480,
                  legend=dict(orientation="h", y=1.0, yanchor="bottom", x=0))
fig.update_yaxes(tickformat=".0%", rangemode="tozero")
fig.update_xaxes(rangeslider_visible=True)
print(len(fig.data), "traces |", fig.layout.hovermode, "|", fig.data[0].hovertemplate)

# %% Step 3: shade the sale weekends (found from the data, not typed by hand)
promo_dates = sales.loc[sales["promo_day"] == 1, "date"].drop_duplicates().sort_values()
blocks = (promo_dates.diff().dt.days != 1).cumsum()
weekends = promo_dates.groupby(blocks).agg(["min", "max"])
for start, end in weekends.itertuples(index=False):
    fig.add_vrect(x0=start, x1=end + pd.Timedelta(days=1), fillcolor="orange", opacity=0.25, line_width=0)
print("sale weekends shaded:", len(fig.layout.shapes))
print(weekends.assign(days=(weekends["max"] - weekends["min"]).dt.days + 1).to_string(index=False))

# %% Step 4: back the title with a number
on_sale = orders["order_date"].isin(promo_dates)
print(f"share of orders using a code: sale-weekend days {orders.loc[on_sale, 'used_code'].mean():.1%}, "
      f"all other days {orders.loc[~on_sale, 'used_code'].mean():.1%}")

early = orders["order_date"] < "2024-02-01"
print(f"January 2024 (no sale): {orders.loc[early, 'used_code'].mean():.1%}. The data starts here, and WELCOME10 marks "
      "a customer's first order IN THE DATA, so the first weeks look busier with codes than they were.")

# %% Step 5: save. HTML always; a PNG only if Kaleido can find Chrome.
target = OUTPUT / "promo_share.html"
fig.write_html(target, include_plotlyjs="cdn")
print("saved:", target.name, f"| {target.stat().st_size / 1024:,.0f} KB")

chrome = os.environ.get("BROWSER_PATH") or shutil.which("google-chrome") or shutil.which("chromium") \
    or shutil.which("chromium-browser") or shutil.which("chrome")
if chrome is None:
    print("static image skipped: no Chrome found (run plotly_get_chrome, or set BROWSER_PATH to a Chrome binary)")
else:
    try:
        png = OUTPUT / "promo_share.png"
        fig.write_image(png, width=900, height=480, scale=2)
        print("saved:", png.name, "| exists:", png.exists())
    except Exception as error:   # Kaleido reports many different problems; none should stop the lab
        print("static image skipped:", type(error).__name__, str(error).splitlines()[0][:80])
