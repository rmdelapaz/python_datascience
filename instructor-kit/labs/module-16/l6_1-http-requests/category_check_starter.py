# --- lab bootstrap: find labs_paths.py (the same three lines open every lab; see labs/README.md) ---
import pathlib, sys
sys.path[:0] = [str(p) for p in pathlib.Path(globals().get("__file__", "lab.py")).resolve().parents if (p / "labs_paths.py").is_file()]
from labs_paths import OFFLINE, fixtures

# %% [markdown]
# # Lab 6.1-A · Three category pages, one of them missing (STARTER)
# Question: how many products do the Footwear, Snow and Skis category pages list, and how
# many of those products show a rating star? (One of the three pages does not exist.)
#
# Practices: robots.txt in code, a User-Agent that says who you are, timeout,
# status codes and raise_for_status(), bytes versus text, and a wrong encoding.
#
# Two modes, one function (get):
#   online  : requests go to BASE_URL (the practice shop).
#   offline : LABS_OFFLINE=1 -> the saved responses in labs/module-16/_fixtures/ are used
#             and nothing touches the network.
#
# Expected when you finish: a five-row list of what robots.txt allows, a report table with
# one row per page (status, type, bytes, cards, stars), a line showing that the 404 page
# has a body with zero product cards, two lines showing the stars vanish under the wrong
# encoding and come back under utf-8, and a one-line answer for each page that exists.

# %% Setup (done for you)
import json
import os
import time
from urllib.parse import urljoin
from urllib.robotparser import RobotFileParser

import pandas as pd
import requests

# The practice shop. Teaching from the unzipped copy? Use "http://127.0.0.1:8001/practice/shop/".
BASE_URL = os.environ.get("PINECREST_BASE_URL", "https://rays-python-datascience.netlify.app/practice/shop/")
USER_AGENT = "pinecrest-course-bot/1.0 (learning project; contact: you@example.com)"
HEADERS = {"User-Agent": USER_AGENT}


def get(path):
    """GET one page of the practice shop and return the Response (no status check here)."""
    url = urljoin(BASE_URL, path)
    if OFFLINE:
        return saved_response("shop_" + path.replace("../", "").replace("/", "_"), url)
    resp = requests.get(url, headers=HEADERS, timeout=10)
    time.sleep(1)                                   # the Crawl-delay from robots.txt
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


print("mode:", "offline (saved responses in _fixtures/)" if OFFLINE else f"online ({BASE_URL})")

# %% Step 1: read the rules before fetching anything
robots_resp = get("../robots.txt")
robots_resp.raise_for_status()
robots = RobotFileParser()
robots.parse(robots_resp.text.splitlines())

pages = ["category-footwear.html", "category-snow.html", "category-skis.html"]
for path in pages + ["staff/"]:
    # TODO 1: replace None with robots.can_fetch(USER_AGENT, <the full URL of this path>).
    #         Build the full URL with urljoin(BASE_URL, path).
    allowed = None
    print(f"1. may fetch {path:<24}", allowed)
# TODO 1b: replace None with the crawl delay the file asks for: robots.crawl_delay(USER_AGENT)
print("   crawl delay:", None, "second(s)")

# %% Step 2: fetch each page, check the status, count what is on it
rows = []
for path in pages:
    resp = get(path)
    row = {"page": path, "status": resp.status_code, "type": resp.headers.get("Content-Type"),
           "bytes": len(resp.content), "cards": None, "stars": None}
    # TODO 2: check the status BEFORE using the body.
    #   try:
    #       resp.raise_for_status()
    #   except requests.exceptions.HTTPError:
    #       row["note"] = "http error: body not used"
    #   else:
    #       resp.encoding = "utf-8"     # the shop's pages are UTF-8; a local copy's server does not say so
    #       row["cards"] = resp.text.count('class="product-card"')
    #       row["stars"] = resp.text.count("★")
    #       row["note"] = "ok"
    row["note"] = "TODO 2: status not checked yet"
    rows.append(row)

report = pd.DataFrame(rows)
report[["cards", "stars"]] = report[["cards", "stars"]].astype("Int64")
print("2. report:")
print(report.to_string(index=False))

# %% Step 3: what would have happened without the status check?
missing = get("category-skis.html")
print("3. the 404 page still has a body:", len(missing.content), "bytes of", missing.headers.get("Content-Type"))
print("   product cards counted in it:", missing.text.count('class="product-card"'), "(a quiet zero, not an error)")

# %% Step 4: bytes, text and the wrong encoding
snow = get("category-snow.html")
print("4. encoding from the header:", snow.encoding, "| Content-Type:", snow.headers.get("Content-Type"))
print("  ", len(snow.content), "bytes became", len(snow.text), "characters")
# TODO 4: set snow.encoding = "cp1252" (the wrong table) and print how many "★" and how many
#         "â˜…" are in snow.text. Then set it to "utf-8" and print the two counts again.
print("   TODO 4 not done yet: compare the counts under cp1252 and under utf-8.")

# %% Step 5: the answer
ok = report[report["note"] == "ok"]
if ok.empty:
    print("5. No page has been checked and counted yet (TODO 2).")
for _, r in ok.iterrows():
    print(f"5. {r['page']}: {r['cards']} products, {r['stars']} with a rating star, "
          f"{r['cards'] - r['stars']} not rated yet")
print("   Which of the three pages must not get a count, and why? Say it in one sentence.")
