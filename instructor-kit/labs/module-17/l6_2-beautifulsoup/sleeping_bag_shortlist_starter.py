# --- lab bootstrap: find labs_paths.py (the same three lines open every lab; see labs/README.md) ---
import pathlib, sys
sys.path[:0] = [str(p) for p in pathlib.Path(globals().get("__file__", "lab.py")).resolve().parents if (p / "labs_paths.py").is_file()]
from labs_paths import OFFLINE, OUTPUT, fixtures

# %% [markdown]
# # Lab 6.2-A · The sleeping-bag shortlist (STARTER)
# Question: a customer wants a sleeping bag that costs $260 or less and can be bought today.
# Which one is the lightest, and what warranty does each candidate carry?
#
# The category page lists name, price, rating and stock. Weight and warranty are only on each
# product's own page, so the job is: parse the listing, narrow it down, and fetch detail
# pages only for the products that matter.
#
# Practices: select() and select_one(), one card -> one dictionary, reading attributes
# (data-price, data-rating, class), a missing value that stays missing, a specifications
# table turned into a dictionary, counting requests before looping, cleaning text into numbers.
#
# Two modes, one function (get):
#   online  : requests go to BASE_URL (the practice shop), one second apart.
#   offline : LABS_OFFLINE=1 -> the saved pages in labs/module-17/_fixtures/ are used
#             and nothing touches the network.
#
# Expected when you finish: 24 cards that match the page's own count; a 24-row listing with
# prices, ratings and stock; a shortlist of 6 sleeping bags (so 6 detail pages, not 24); a
# details table with type, weight and warranty; the shortlist sorted lightest first; and a
# one-line answer that also names the bag whose weight is not listed.

# %% Setup (done for you)
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

# %% Step 1: one request for the listing; does it hold what the page says it holds?
listing_page = get_soup("category-sleeping.html")
cards = listing_page.select("li.product-card")
claimed = int(re.search(r"\d+", listing_page.select_one("p.result-count").get_text()).group())
print(f"1. cards on the page: {len(cards)} | the page claims: {claimed} | match: {len(cards) == claimed}")

# %% Step 2: one card -> one dictionary
def parse_card(card):
    """Turn one product card into a flat dictionary."""
    link = card.select_one("h2.product-name a")
    # TODO 2a: price. Read the data-price attribute of p.price inside this card and convert
    #          it with float():  float(card.select_one("p.price")["data-price"])
    price = None
    # TODO 2b: rating. Ask safely, because some products have no rating:
    #          rating = card.select_one("p.rating").get("data-rating")
    #          then store float(rating) if rating else None
    rating = None
    # TODO 2c: stock status. The second class of p.stock is "in-stock", "low-stock" or
    #          "out-of-stock":  card.select_one("p.stock")["class"][1].replace("-", "_")
    stock_status = None
    return {
        "sku": card["data-sku"],
        "name": link.get_text(strip=True),
        "price": price,
        "rating": rating,
        "stock_status": stock_status,
        "href": link["href"],
    }


listing = pd.DataFrame([parse_card(c) for c in cards])
print("2. listing:", listing.shape, "| unique SKUs:", listing["sku"].is_unique)
print(listing[["sku", "name", "price", "rating", "stock_status"]].head(4).to_string(index=False))
print("   stock:", listing["stock_status"].value_counts().to_dict())

# %% Step 3: narrow it down BEFORE visiting any detail page
is_bag = listing["name"].str.contains("Sleeping Bag")
if listing["price"].isna().all() or listing["stock_status"].isna().all():
    shortlist = listing.head(0)
    print(f"3. sleeping bags on the page: {is_bag.sum()} | TODO 2 not done yet: no prices or stock, so no shortlist.")
else:
    # TODO 3: keep the rows that are sleeping bags (is_bag), cost 260 or less, and are not
    #         "out_of_stock". Combine the three conditions with & (each in parentheses).
    shortlist = listing.head(0)
    print(f"3. sleeping bags on the page: {is_bag.sum()} | at $260 or less and available: {len(shortlist)}")
print(f"   detail pages to fetch: {len(shortlist)} (not {len(listing)})")

# %% Step 4: one detail page -> one dictionary
def parse_product_page(soup):
    """Turn one product detail page into a flat dictionary."""
    # TODO 4: turn the specifications table into a dictionary, label -> value.
    #         Each row (table.specs tr) has the label in a th and the value in a td:
    #         specs = {tr.th.get_text(strip=True): tr.td.get_text(strip=True)
    #                  for tr in soup.select("table.specs tr")}
    specs = {}
    return {
        "sku": soup.select_one("span.sku-value").get_text(strip=True),
        "type": specs.get("Type"),
        "weight": specs.get("Weight"),
        "warranty": specs.get("Warranty"),
    }


details = pd.DataFrame([parse_product_page(get_soup(href)) for href in shortlist["href"]],
                       columns=["sku", "type", "weight", "warranty"])
print("4. details as scraped:")
print(details.to_string(index=False) if len(details) else "   (nothing yet: the shortlist is empty until TODO 2 and TODO 3 are done)")

# %% Step 5: clean the text, join on the key
# TODO 5a: weight arrives as text such as "0.81 kg" or "Not listed". Make a numeric column:
#          details["weight_kg"] = pd.to_numeric(details["weight"].str.replace(" kg", ""), errors="coerce")
details["weight_kg"] = float("nan")
# TODO 5b: the temperature rating is inside the type ("30F Sleeping Bag"). Pull out the digits:
#          details["rated_to_f"] = details["type"].str.extract(r"(\d+)F")[0].astype(int)
details["rated_to_f"] = None

answer = (shortlist[["sku", "name", "price", "rating", "stock_status"]]
          .merge(details[["sku", "rated_to_f", "weight_kg", "warranty"]], on="sku", how="left")
          .sort_values("weight_kg"))
print("5. the shortlist, lightest first:")
print(answer[["sku", "name", "price", "rated_to_f", "weight_kg", "warranty"]].to_string(index=False))

# %% Step 6: the answer, and what we cannot say
if answer["weight_kg"].notna().any():
    lightest = answer.iloc[0]
    unknown = answer[answer["weight_kg"].isna()]
    print(f"6. Lightest: {lightest['name']} ({lightest['sku']}), {lightest['weight_kg']} kg, "
          f"${lightest['price']}, {lightest['warranty']} warranty.")
    print(f"   No weight listed for: {', '.join(unknown['sku'])}.")
    print("   Warranties:", answer["warranty"].value_counts().to_dict())
    print("   In one sentence: where should the bag with no listed weight go in a 'lightest first' list, and why?")
else:
    print("6. No answer yet. Expected when the TODOs are done: one lightest bag, and one bag whose weight is not listed.")
answer.to_csv(OUTPUT / "sleeping_bag_shortlist.csv", index=False)
print("   saved:", "sleeping_bag_shortlist.csv in the output folder,",
      len(pd.read_csv(OUTPUT / "sleeping_bag_shortlist.csv")), "rows")
