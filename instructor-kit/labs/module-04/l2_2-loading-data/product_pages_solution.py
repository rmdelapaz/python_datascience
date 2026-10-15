# --- lab bootstrap: find labs_paths.py (the same three lines open every lab; see labs/README.md) ---
import pathlib, sys
sys.path[:0] = [str(p) for p in pathlib.Path(globals().get("__file__", "lab.py")).resolve().parents if (p / "labs_paths.py").is_file()]
from labs_paths import DATA, OUTPUT
# %% [markdown]
# # Lab 2.2-B · Which product pages get looked at? (SOLUTION)
# Question: in November 2025, which product pages were viewed most on the website,
# and do visitors stay longer on product pages than on the other pages?

# %% Load the tree with the json module
import json

import pandas as pd

with open(DATA / "web_sessions.json", encoding="utf-8") as f:
    web = json.load(f)
print(list(web), len(web["sessions"]))

# %% Step 1: one row per page view
views = pd.json_normalize(web["sessions"], record_path="pages", meta=["session_id", "converted"])
print("page views:", views.shape)
print(views.dtypes.to_string())

# %% Step 2: fix the types the file could not carry
views["at"] = pd.to_datetime(views["at"])
views["converted"] = views["converted"].astype(bool)
print("after the fix:", views["at"].dtype, views["converted"].dtype)

# %% Step 3: product pages
product = views[views["path"].str.startswith("/product/")]
product = product.assign(sku=product["path"].str.replace("/product/", ""))
print("product-page views:", len(product), "in", product["session_id"].nunique(), "sessions")
print(product["sku"].value_counts().head(5).to_string())
print("mean seconds, product pages:", round(product["seconds"].mean(), 1))
print("mean seconds, all pages    :", round(views["seconds"].mean(), 1))

# %% Step 4: save it, and read it back
product.to_parquet(OUTPUT / "product_views.parquet")
product.to_csv(OUTPUT / "product_views.csv", index=False)
back = pd.read_parquet(OUTPUT / "product_views.parquet")
back_csv = pd.read_csv(OUTPUT / "product_views.csv")
print("Parquet:", back["at"].dtype, "| equal to the original:", back.equals(product))
print("CSV    :", back_csv["at"].dtype, "| equal to the original:", back_csv.equals(product))
