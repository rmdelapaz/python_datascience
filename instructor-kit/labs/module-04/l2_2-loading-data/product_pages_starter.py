# --- lab bootstrap: find labs_paths.py (the same three lines open every lab; see labs/README.md) ---
import pathlib, sys
sys.path[:0] = [str(p) for p in pathlib.Path(globals().get("__file__", "lab.py")).resolve().parents if (p / "labs_paths.py").is_file()]
from labs_paths import DATA, OUTPUT
# %% [markdown]
# # Lab 2.2-B · Which product pages get looked at? (STARTER)
# Question: in November 2025, which product pages were viewed most on the website,
# and do visitors stay longer on product pages than on the other pages?
#
# The answer is two levels down in web_sessions.json: each session has a LIST of pages.
# Expected when you finish: 9,348 page views, the number of product-page views, the five
# most viewed SKUs, two average times in seconds, and a Parquet file that still knows
# its dates when you read it back.

# %% Load the tree with the json module (done for you)
import json

import pandas as pd

with open(DATA / "web_sessions.json", encoding="utf-8") as f:
    web = json.load(f)
print(list(web), len(web["sessions"]))

# %% Step 1: one row per page view
# TODO 1: views = pd.json_normalize(web["sessions"], record_path=..., meta=[...])
#         record_path is the key that holds the list; copy "session_id" and "converted"
#         onto every row with meta. Print views.shape and views.dtypes.
views = None

# %% Step 2: fix the types the file could not carry
# TODO 2: views["at"] is text: convert it with pd.to_datetime.
#         views["converted"] came through meta as dtype object: .astype(bool).

# %% Step 3: product pages
# TODO 3: product = views[views["path"].str.startswith("/product/")]
#         Add a column sku to it: the path with "/product/" removed (.str.replace).
#         Print the number of rows, the five most viewed SKUs (value_counts().head(5)),
#         and the mean of seconds for product pages and for all pages.
product = None

# %% Step 4: save it, and read it back
# TODO 4: product.to_parquet(OUTPUT / "product_views.parquet")
#         back = pd.read_parquet(OUTPUT / "product_views.parquet")
#         Print back["at"].dtype and back.equals(product).
if views is None or product is None:
    print("TODO 1-4 not done yet: `views` or `product` is still None.")
