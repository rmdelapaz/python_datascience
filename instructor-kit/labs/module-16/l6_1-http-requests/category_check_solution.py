# --- lab bootstrap: find labs_paths.py (the same three lines open every lab; see labs/README.md) ---
import pathlib, sys
sys.path[:0] = [str(p) for p in pathlib.Path(globals().get("__file__", "lab.py")).resolve().parents if (p / "labs_paths.py").is_file()]
from labs_paths import OFFLINE, fixtures

# %% [markdown]
# # Lab 6.1-A · Three category pages, one of them missing (SOLUTION)
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
    print(f"1. may fetch {path:<24}", robots.can_fetch(USER_AGENT, urljoin(BASE_URL, path)))
print("   crawl delay:", robots.crawl_delay(USER_AGENT), "second(s)")

# %% Step 2: fetch each page, check the status, count what is on it
rows = []
for path in pages:
    resp = get(path)
    row = {"page": path, "status": resp.status_code, "type": resp.headers.get("Content-Type"),
           "bytes": len(resp.content), "cards": None, "stars": None}
    try:
        resp.raise_for_status()
    except requests.exceptions.HTTPError:
        row["note"] = "http error: body not used"
    else:
        resp.encoding = "utf-8"       # the shop's pages are UTF-8; a local copy's server does not say so
        row["cards"] = resp.text.count('class="product-card"')
        row["stars"] = resp.text.count("★")
        row["note"] = "ok"
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
snow.encoding = "cp1252"                            # decode the same bytes with the wrong table
print("   as cp1252: stars", snow.text.count("★"), "| junk 'â˜…'", snow.text.count("â˜…"))
snow.encoding = "utf-8"                             # the table that matches the bytes
print("   as utf-8 : stars", snow.text.count("★"), "| junk 'â˜…'", snow.text.count("â˜…"))

# %% Step 5: the answer
ok = report[report["note"] == "ok"]
for _, r in ok.iterrows():
    print(f"5. {r['page']}: {r['cards']} products, {r['stars']} with a rating star, "
          f"{r['cards'] - r['stars']} not rated yet")
print("   category-skis.html: no such page (404), so no count is reported for it.")
