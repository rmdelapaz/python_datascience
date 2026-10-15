# --- lab bootstrap: find labs_paths.py (the same three lines open every lab; see labs/README.md) ---
import pathlib, sys
sys.path[:0] = [str(p) for p in pathlib.Path(globals().get("__file__", "lab.py")).resolve().parents if (p / "labs_paths.py").is_file()]
from labs_paths import OFFLINE, OUTPUT, fixtures

# %% [markdown]
# # Lab 6.2-B · The price list: two tables, three questions (STARTER)
# Questions for the merchandising lead, all from one page (price-list.html):
#   a) Which category has the most products that are out of stock?
#   b) How many products have no rating yet, and in which categories?
#   c) Which store is open the most hours a day?
# Then one cross-check: does the price list agree with the Accessories category page?
#
# Practices: pandas.read_html() on bytes you fetched yourself, choosing a table by its id
# (not its position), cleaning what a person would see ("$299.95", "9 am to 8 pm") into
# numbers, missing values that stay missing, and checking one route against another
# (read_html against Beautiful Soup).
#
# Two modes, one function (get):
#   online  : requests go to BASE_URL (the practice shop), one second apart.
#   offline : LABS_OFFLINE=1 -> the saved pages in labs/module-17/_fixtures/ are used
#             and nothing touches the network.
#
# Expected when you finish: 2 tables, each chosen by its id; a Price column that is float64;
# a 9-row availability table and the category with the most out-of-stock products; the
# number of unrated products and their categories; hours open for each of the 4 stores and
# the store open longest; and a cross-check line in which every comparison says True.

# %% Setup (done for you)
import io
import json
import os
import re
import time
from urllib.parse import urljoin

import pandas as pd
import requests
from bs4 import BeautifulSoup

pd.set_option("display.width", 150)
pd.set_option("display.max_columns", 20)

# The practice shop. Teaching from the unzipped copy? Use "http://127.0.0.1:8001/practice/shop/".
BASE_URL = os.environ.get("PINECREST_BASE_URL", "https://rays-python-datascience.netlify.app/practice/shop/")
USER_AGENT = "pinecrest-course-bot/1.0 (learning project; contact: you@example.com)"
HEADERS = {"User-Agent": USER_AGENT}
DELAY = 1                                           # the Crawl-delay in the shop's robots.txt


def get(path):
    """GET one page of the practice shop and return the Response (no status check here)."""
    url = urljoin(BASE_URL, path)
    if OFFLINE:
        return saved_response("shop_" + path.replace("../", "").replace("/", "_"), url)
    resp = requests.get(url, headers=HEADERS, timeout=10)
    time.sleep(DELAY)
    return resp


def saved_response(name, url):
    """Rebuild a real requests.Response from a saved body and its saved status and headers."""
    folder = fixtures(__file__)
    meta = json.loads((folder / (name + ".meta.json")).read_text(encoding="utf-8"))
    resp = requests.Response()
    resp.status_code, resp.reason, resp.url = meta["status"], meta["reason"], url
    resp.headers.update(meta["headers"])
    resp._content = (folder / name).read_bytes()
    resp.encoding = requests.utils.get_encoding_from_headers(resp.headers)
    return resp


def get_soup(path):
    """Fetch one page, check the status, and parse the BYTES (never resp.text)."""
    resp = get(path)
    resp.raise_for_status()
    return BeautifulSoup(resp.content, "html.parser")


print("mode:", "offline (saved pages in _fixtures/)" if OFFLINE else f"online ({BASE_URL})")

# %% Step 1: fetch the page yourself, hand pandas the bytes
resp = get("price-list.html")
resp.raise_for_status()

tables = pd.read_html(io.BytesIO(resp.content), encoding="utf-8")
print("1. tables on the page:", len(tables), "| shapes:", [t.shape for t in tables])

# TODO 1: choosing tables[0] and tables[1] works today and breaks the day the page gains a
#         table. Choose each table by its id instead: add  attrs={"id": "price-list"}  to the
#         first call and  attrs={"id": "store-hours"}  to the second (keep the [0]: read_html
#         always returns a list).
prices = pd.read_html(io.BytesIO(resp.content), encoding="utf-8")[0]
stores = pd.read_html(io.BytesIO(resp.content), encoding="utf-8")[1]
print("   tables in use:", prices.shape, list(prices.columns), "|", stores.shape, list(stores.columns))

# %% Step 2: read_html reads what a person sees, so clean it
print("2. Price arrives as:", prices["Price"].dtype, "| first value:", repr(prices["Price"].iloc[0]))
# TODO 2: turn the Price text into numbers: remove "$" and "," and convert to float.
#         prices["Price"] = prices["Price"].str.replace("[$,]", "", regex=True).astype(float)
if pd.api.types.is_float_dtype(prices["Price"]):
    print("   after cleaning:", prices["Price"].dtype, "| total of all list prices:", prices["Price"].sum().round(2))
else:
    print("   TODO 2 not done yet: Price is still text, so it cannot be added up or compared.")

# %% Step 3 (question a): availability by category
# TODO 3: count products per Category and Availability:
#         availability = pd.crosstab(prices["Category"], prices["Availability"])
#         then  most_out = availability["Out of stock"].idxmax()
availability = None
print("3. availability by category:")
if availability is None:
    print("   TODO 3 not done yet. Expected: 9 rows (categories), 3 columns (In stock, Low stock, Out of stock).")
else:
    print(availability.to_string())
    most_out = availability["Out of stock"].idxmax()
    print(f"   a) most out of stock: {most_out} ({availability.loc[most_out, 'Out of stock']} products)")

# %% Step 4 (question b): products with no rating yet
# TODO 4: keep the rows whose Rating is missing:  prices[prices["Rating"].isna()]
unrated = prices.head(0)
print("4. b) products with no rating:", len(unrated), "|", unrated["Category"].value_counts().to_dict())
print("   mean rating, missing left missing:", prices["Rating"].mean().round(3),
      "| if they had been stored as 0:", prices["Rating"].fillna(0).mean().round(3))

# %% Step 5 (question c): store hours
# TODO 5: "9 am to 8 pm" is text. Pull out the two numbers and compute the hours open:
#         hours = stores["Open daily"].str.extract(r"(\d+) am to (\d+) pm").astype(int)
#         stores["hours_open"] = (hours[1] + 12) - hours[0]
stores["hours_open"] = None
print("5. store hours:")
print(stores[["City", "State", "Open daily", "hours_open"]].to_string(index=False))
if stores["hours_open"].notna().any():
    longest = stores.loc[stores["hours_open"].astype(int).idxmax()]
    print(f"   c) open longest: {longest['City']} ({longest['hours_open']} hours a day)")
else:
    print("   TODO 5 not done yet: no hours computed.")

# %% Step 6: cross-check the table against a category page, card by card
page = get_soup("category-accessories.html")
# TODO 6: for every card, read the price from the data-price attribute and record whether
#         the card has a rating. Replace the two None values:
#           "price_card": float(card.select_one("p.price")["data-price"]),
#           "rated_card": card.select_one("p.rating").get("data-rating") is not None,
web = pd.DataFrame([{"SKU": card["data-sku"],
                     "price_card": None,
                     "rated_card": None}
                    for card in page.select("li.product-card")])
both = prices[prices["Category"] == "Accessories"].merge(web, on="SKU", how="outer", indicator=True)
print("6. Accessories: rows in the price list", (prices["Category"] == "Accessories").sum(),
      "| cards on the category page", len(web), "| matched", (both["_merge"] == "both").sum())
if web["price_card"].isna().all():
    print("   TODO 6 not done yet. Expected: prices agree: True | 'has a rating' agrees: True")
else:
    print("   prices agree:", (both["Price"] == both["price_card"]).all(),
          "| 'has a rating' agrees:", (both["Rating"].notna() == both["rated_card"]).all())
    print("   unrated on the category page:", sorted(web.loc[~web["rated_card"].astype(bool), "SKU"]))
print("   Which route would you use to get each product's link, read_html or Beautiful Soup, and why?")

# %% Step 7: save the cleaned table
prices.to_csv(OUTPUT / "price_list_clean.csv", index=False)
print("7. saved price_list_clean.csv in the output folder:", pd.read_csv(OUTPUT / "price_list_clean.csv").shape)
