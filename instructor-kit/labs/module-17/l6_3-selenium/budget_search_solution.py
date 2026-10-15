# --- lab bootstrap: find labs_paths.py (the same three lines open every lab; see labs/README.md) ---
import pathlib, sys
sys.path[:0] = [str(p) for p in pathlib.Path(globals().get("__file__", "lab.py")).resolve().parents if (p / "labs_paths.py").is_file()]
from labs_paths import OFFLINE, OUTPUT, fixtures

# %% [markdown]
# # Lab 6.3-A · The budget shelf: what the search page shows, and what it holds (SOLUTION)
# Question: marketing wants a "Gear under $50" shelf. Which products cost $50 or less and
# can be bought today, and how many are there in each category?
#
# The shop's Search page can answer that, but its results are filled in by JavaScript. You
# will get them with a browser, parse the finished page with Beautiful Soup, check the
# result against the page's own count, and then ask the data file behind the page.
#
# Practices: seeing what requests receives from a dynamic page, building a search URL with
# urlencode, headless Chrome with Selenium 4, an explicit wait (never time.sleep), handing
# driver.page_source to Beautiful Soup, quitting the browser in finally, and the habit that
# matters most: look for the data file first.
#
# Three modes, one function (rendered):
#   online, Chrome works : a headless browser opens the page at BASE_URL and runs your steps.
#   online, no browser   : a clear message, then the saved copy of the finished page is used.
#   offline              : LABS_OFFLINE=1 -> no browser and no network. The saved copy of the
#                          finished page in labs/module-17/_fixtures/ is parsed instead.

# %% Setup (done for you)
import json
import os
import re
import time
from urllib.parse import urlencode, urljoin

import pandas as pd
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

pd.set_option("display.width", 150)
pd.set_option("display.max_columns", 20)

# The practice shop. Teaching from the unzipped copy? Use "http://127.0.0.1:8001/practice/shop/".
BASE_URL = os.environ.get("PINECREST_BASE_URL", "https://rays-python-datascience.netlify.app/practice/shop/")
USER_AGENT = "pinecrest-course-bot/1.0 (learning project; contact: you@example.com)"
HEADERS = {"User-Agent": USER_AGENT}
DELAY = 1                                           # the Crawl-delay in the shop's robots.txt


def get(path):
    """GET one file of the practice shop with requests and return the Response."""
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


def make_driver():
    """Start headless Chrome with this course's settings. Whoever calls this must quit it."""
    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("--window-size=1000,800")
    options.add_argument(f"--user-agent={USER_AGENT}")
    chrome = os.environ.get("PINECREST_CHROME")     # optional: the path of a Chrome or Chromium program
    if chrome:
        options.binary_location = os.path.expanduser(chrome)
        options.add_argument("--no-sandbox")
    return webdriver.Chrome(options=options)


def rendered(name, url, steps):
    """Return the HTML of a page AFTER its JavaScript has run.

    steps(driver, wait) is your browser work (waits, clicks). The browser is always quit.
    With LABS_OFFLINE=1, or when no browser can start, the saved copy of the finished page
    (_fixtures/rendered_<name>.html) is returned instead, and a line says so.
    """
    saved = fixtures(__file__) / f"rendered_{name}.html"
    if OFFLINE:
        print(f"   [offline] no browser started; reading the saved finished page {saved.name}")
        return saved.read_text(encoding="utf-8")
    try:
        driver = make_driver()
    except Exception as err:                        # no Chrome, or the driver download was blocked
        print(f"   [no browser] Chrome could not be started ({type(err).__name__}).")
        print(f"   Reading the saved finished page {saved.name} instead. See the README for what to do.")
        return saved.read_text(encoding="utf-8")
    try:
        driver.get(url)
        steps(driver, WebDriverWait(driver, 10))
        return driver.page_source
    except WebDriverException as err:               # a wait that timed out, a locator that found nothing
        first_line = (err.msg or "").splitlines()[0] if err.msg else ""
        print(f"   [browser step failed] {type(err).__name__}: {first_line}")
        print(f"   Reading the saved finished page {saved.name} instead.")
        return saved.read_text(encoding="utf-8")
    finally:
        driver.quit()


print("mode:", "offline (saved pages in _fixtures/, no browser)" if OFFLINE else f"online ({BASE_URL})")

# %% Step 1: what does requests receive from the search page?
shell = BeautifulSoup(get("search.html").content, "html.parser")
print("1. through requests:", len(shell.select("#search-results li")), "results |",
      "count line:", repr(shell.select_one("#search-count").get_text()))

# %% Step 2: the form uses GET, so the search is just a URL
query = urlencode({"max_price": 50, "in_stock": 1})
search_url = urljoin(BASE_URL, "search.html") + "?" + query
print("2. query string:", query)

# %% Step 3: let a browser run the page, and wait for the signal that it has finished
def wait_for_results(driver, wait):
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#search-results[data-loaded="true"]')),
               message="the search results never finished loading")


print("3. rendering the search page:")
html = rendered("search_budget", search_url, wait_for_results)

# %% Step 4: parse the finished page with Beautiful Soup
def parse_results(html):
    """Parse the result cards of a rendered search page into a DataFrame."""
    soup = BeautifulSoup(html, "html.parser")
    rows = []
    for li in soup.select("#search-results li"):
        rows.append({
            "sku": li["data-sku"],
            "name": li.select_one("h2 a").get_text(strip=True),
            "category": li.select_one("p.product-category").get_text(strip=True),
            "price": float(li.select_one("p.price").get_text().lstrip("$")),
        })
    return pd.DataFrame(rows, columns=["sku", "name", "category", "price"])


on_page = parse_results(html)
count_text = BeautifulSoup(html, "html.parser").select_one("#search-count").get_text()
claimed = int(re.search(r"\d+", count_text).group())
print("4. parsed from the finished page:", on_page.shape, "| highest price:", on_page["price"].max())
print(on_page.head(3).to_string(index=False))

# %% Step 5: check the scrape against the page's own count
status = "match" if claimed == len(on_page) else "MISMATCH"
print(f"5. the page says: {count_text!r} | rows parsed: {len(on_page)} | {status}")

# %% Step 6: look for the data. Which file feeds this page?
script = get("shop.js")
script.raise_for_status()
print("6. files the page's script fetches:", re.findall(r"fetch\('(.+?)'\)", script.text))

resp = get("products.json")
resp.raise_for_status()
shop = pd.DataFrame(resp.json()["products"])
budget = shop[(shop["price"] <= 50) & (shop["stock_status"] != "out_of_stock")]
print("   products.json:", shop.shape, "| $50 or less and available:", len(budget))
print("   the page shows the first", len(on_page), "of them:",
      on_page["sku"].tolist() == budget["sku"].head(len(on_page)).tolist())

# %% Step 7: the answer, and what the page alone would have told you
compare = pd.DataFrame({"on_the_page": on_page["category"].value_counts(),
                        "in_the_data": budget["category"].value_counts()}).fillna(0).astype(int)
compare["not_shown"] = compare["in_the_data"] - compare["on_the_page"]
print("7. budget products by category:")
print(compare.sort_values("in_the_data", ascending=False).to_string())
missing = budget[~budget["sku"].isin(on_page["sku"])]
print(f"   {len(missing)} products are in the data but not on the page, all in:",
      missing["category"].unique().tolist())
budget[["sku", "name", "category", "price", "stock_status"]].to_csv(OUTPUT / "budget_shelf.csv", index=False)
print("   saved budget_shelf.csv in the output folder:", len(pd.read_csv(OUTPUT / "budget_shelf.csv")), "rows")
